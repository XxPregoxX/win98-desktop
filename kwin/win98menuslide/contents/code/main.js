/*
    Win98 Menu Slide: efeito do KWin do tema win98-desktop.

    Baseado no efeito padrão "Fading popups" do KWin (fadingpopups), de Vlad Zahorodnii
    (lista de janelas ignoradas, estrutura e o fade dos popups que não são menu).

    SPDX-FileCopyrightText: 2018 Vlad Zahorodnii <vlad.zahorodnii@kde.org>
    SPDX-FileCopyrightText: 2026 Leonardo Borges
    SPDX-License-Identifier: GPL-2.0-or-later
*/

"use strict";
// Win98 Menu Slide
//
// Menus, submenus, combo box lists and tooltips slide out of the point where
// they were opened, like the Windows 98 menu animation (the one Qt imitates in
// QRollEffect): the popup is revealed from the corner/edge next to the pointer
// and its contents slide along with the growing edge, so nothing is stretched.
//
// Everything else the stock "Fading popups" effect animated (notifications,
// OSDs, ...) keeps its fade, so this effect replaces it.

var DEBUG = false;        // log every decision (journalctl --user -f | grep js)
var SLOW = 1;             // > 1 slows the slide down, for testing
var CYCLE = false;        // test mode: ignore the pointer, cycle through all directions

var SLIDE_MS = 165;       // length of the Windows 9x menu animation
var TOLERANCE = 4;        // px between pointer and popup edge that still counts as "touching"

// Qt places a tooltip a whole cursor height below the pointer (QTipLabel::placeTip: pointer +
// (2, cursor size)), so with a 32px cursor whose arrow is only ~19px tall it floats far below
// the arrow. Windows 98 put it right under the arrow: such tooltips are drawn moved up so that
// their top sits TOOLTIP_GAP px below the pointer. Only the drawing moves (tooltips take no input).
var TOOLTIP_GAP = 21;     // arrow height (19px) + 2
var QT_TIP_MIN = 24;      // range of cursor sizes the Qt rule is recognised for
var QT_TIP_MAX = 48;

var LEFT = typeof Effect.Left == "number" ? Effect.Left : 1;
var TOP = typeof Effect.Top == "number" ? Effect.Top : 2;
var RIGHT = typeof Effect.Right == "number" ? Effect.Right : 4;
var BOTTOM = typeof Effect.Bottom == "number" ? Effect.Bottom : 8;

var blacklist = [
    "ksmserver ksmserver",
    "ksmserver-logout-greeter ksmserver-logout-greeter",
    "kscreenlocker_greet kscreenlocker_greet",
    "ksplashqml ksplashqml",
    "spectacle org.kde.spectacle",
    "spectacle spectacle",
];

// Which way a popup slides, given its frame and the pointer position.
// horiz/vert: animated axes; left/top: the popup grows away from its left/top edge.
function decide(frame, pointer) {
    var l = frame.x, t = frame.y, r = frame.x + frame.width, b = frame.y + frame.height;
    var x = pointer.x, y = pointer.y;
    var nearX = Math.abs(x - l) <= TOLERANCE || Math.abs(x - r) <= TOLERANCE;
    var nearY = Math.abs(y - t) <= TOLERANCE || Math.abs(y - b) <= TOLERANCE;

    // Context menu: opened with a corner under the pointer, slides out diagonally.
    if (nearX && nearY) {
        return { horiz: true, vert: true,
                 left: Math.abs(x - l) <= Math.abs(x - r),
                 top: Math.abs(y - t) <= Math.abs(y - b) };
    }

    var besideX = x >= l - TOLERANCE && x <= r + TOLERANCE;
    var besideY = y >= t - TOLERANCE && y <= b + TOLERANCE;
    // Pointer above/below: menu bar menus, combo box lists, tooltips.
    if (besideX && !besideY) {
        return { horiz: false, vert: true, left: true, top: y < t };
    }
    // Pointer to one side: submenus.
    if (besideY && !besideX) {
        return { horiz: true, vert: false, left: x < l, top: true };
    }
    // Pointer elsewhere (keyboard-opened menu, pointer inside): nearest corner.
    return { horiz: true, vert: true, left: x <= (l + r) / 2, top: y <= (t + b) / 2 };
}

var cycleDirections = [
    { horiz: true, vert: true, left: true, top: true },
    { horiz: true, vert: true, left: true, top: false },
    { horiz: true, vert: true, left: false, top: true },
    { horiz: true, vert: true, left: false, top: false },
    { horiz: true, vert: false, left: true, top: true },
    { horiz: false, vert: true, left: true, top: true },
];
var cycleIndex = 0;

// Panel popups (Start menu, tray, clock...) slide out of the panel they are attached to,
// whatever the pointer is doing (the Start menu can be opened with the Meta key).
function panelDirection(w) {
    if (!w.appletPopup) {
        return null;
    }
    var g = w.geometry, gap = 16;
    var windows = effects.stackingOrder;
    for (var i = 0; i < windows.length; i++) {
        if (!windows[i].dock) {
            continue;
        }
        var p = windows[i].geometry;
        var overlapX = g.x < p.x + p.width && g.x + g.width > p.x;
        var overlapY = g.y < p.y + p.height && g.y + g.height > p.y;
        if (overlapX && Math.abs(g.y + g.height - p.y) <= gap) {
            return { horiz: false, vert: true, left: true, top: false };   // above a bottom panel: slide up
        }
        if (overlapX && Math.abs(g.y - (p.y + p.height)) <= gap) {
            return { horiz: false, vert: true, left: true, top: true };    // below a top panel: slide down
        }
        if (overlapY && Math.abs(g.x - (p.x + p.width)) <= gap) {
            return { horiz: true, vert: false, left: true, top: true };    // right of a left panel
        }
        if (overlapY && Math.abs(g.x + g.width - p.x) <= gap) {
            return { horiz: true, vert: false, left: false, top: true };   // left of a right panel
        }
    }
    return null;
}

function isSlidingWindow(w) {
    return blacklist.indexOf(w.windowClass) == -1 && w.popupWindow;
}

// Same windows the stock "Fading popups" effect fades, minus the sliding ones.
function isFadingWindow(w) {
    if (blacklist.indexOf(w.windowClass) != -1 || w.popupWindow) {
        return false;
    }
    if (w.outline) {
        return true;
    }
    if (!w.managed) {
        return !w.utility;
    }
    return w.splash || w.toolbar || w.notification || w.onScreenDisplay
        || w.criticalNotification || w.appletPopup;
}

// How far up to draw a popup placed by Qt's tooltip rule (0 if it isn't one, or if it was
// flipped above the pointer). KWin gives Qt tooltips no window type (they are plain popups), so
// they are told apart by position: Qt puts their left edge 2px RIGHT of the pointer. A menu
// opened by a click can't be there (the pointer is inside the button, at or right of the menu's
// left edge), so menus are never moved, and moving them would misplace their clicks.
function tooltipLift(w) {
    var frame = w.geometry;
    var pointer = effects.cursorPos;
    var dx = frame.x - pointer.x;
    var dy = frame.y - pointer.y;
    if (dx < 1 || dx > 4 || dy < QT_TIP_MIN || dy > QT_TIP_MAX) {
        return 0;
    }
    return Math.max(0, dy - TOOLTIP_GAP);
}

var win98 = {
    // Keeps a Qt tooltip drawn right under the arrow; redone when Qt moves the tooltip.
    liftTooltip: function (w) {
        if (w.win98Lift) {
            cancel(w.win98Lift);
            delete w.win98Lift;
        }
        var lift = tooltipLift(w);
        if (DEBUG) {
            console.warn("win98menuslide tooltip " + w.windowClass + " lift=" + lift);
        }
        if (lift > 0) {
            w.win98Lift = set({
                window: w,
                duration: 1,
                animations: [{
                    type: Effect.Translation,
                    to: { value1: 0, value2: -lift }
                }]
            });
        }
    },
    geometryChanged: function (w) {
        if (isSlidingWindow(w) && w.visible) {
            win98.liftTooltip(w);
        }
    },
    slideIn: function (w, panelDir) {
        var frame = w.geometry;
        var dir = panelDir ? panelDir : CYCLE ? cycleDirections[cycleIndex++ % cycleDirections.length]
                        : decide(frame, effects.cursorPos);
        // The clip stays pinned to the edges the popup grows away from.
        var anchor = (dir.horiz && !dir.left ? RIGHT : LEFT) | (dir.vert && !dir.top ? BOTTOM : TOP);
        var area = w.expandedGeometry || frame;
        var duration = animationTime(SLIDE_MS) * SLOW;
        if (DEBUG) {
            console.warn("win98menuslide " + w.windowClass
                + " frame=" + [frame.x, frame.y, frame.width, frame.height]
                + " pointer=" + [effects.cursorPos.x, effects.cursorPos.y]
                + " dir=" + JSON.stringify(dir) + " anchor=" + anchor + " ms=" + duration);
        }
        w.win98Slide = animate({
            window: w,
            duration: duration,
            curve: QEasingCurve.Linear,
            animations: [{
                type: Effect.Clip,
                sourceAnchor: anchor,
                targetAnchor: anchor,
                from: { value1: dir.horiz ? 0 : 1, value2: dir.vert ? 0 : 1 },
                to: { value1: 1, value2: 1 }
            }, {
                // Contents enter from behind the anchored edge, keeping their far edge on the clip edge.
                type: Effect.Translation,
                from: { value1: dir.horiz ? (dir.left ? -area.width : area.width) : 0,
                        value2: dir.vert ? (dir.top ? -area.height : area.height) : 0 },
                to: { value1: 0, value2: 0 }
            }]
        });
    },
    fadeIn: function (w) {
        w.win98Fade = animate({
            window: w,
            curve: QEasingCurve.Linear,
            duration: animationTime(150),
            type: Effect.Opacity,
            from: 0.0,
            to: 1.0
        });
    },
    added: function (w) {
        if (effects.hasActiveFullScreenEffect || !w.visible) {
            return;
        }
        var panelDir = blacklist.indexOf(w.windowClass) == -1 ? panelDirection(w) : null;
        var slide = panelDir || isSlidingWindow(w);
        if (DEBUG && w.appletPopup) {
            var g = w.geometry;
            console.warn("win98menuslide appletPopup " + w.windowClass + " geo=" + [g.x, g.y, g.width, g.height]
                + " panelDir=" + JSON.stringify(panelDir));
        }
        if (!slide && !isFadingWindow(w)) {
            return;
        }
        if (!effect.grab(w, Effect.WindowAddedGrabRole)) {
            return;
        }
        if (slide) {
            if (!panelDir) {
                win98.liftTooltip(w);
                // KWin 6: the geometry signal lives on each window, not on "effects"
                if (!w.win98Watched && w.windowFrameGeometryChanged && w.windowFrameGeometryChanged.connect) {
                    w.win98Watched = true;
                    w.windowFrameGeometryChanged.connect(function () { win98.geometryChanged(w); });
                }
            }
            win98.slideIn(w, panelDir);
        } else {
            win98.fadeIn(w);
        }
    },
    // Windows 98 menus vanish instantly; only the fading windows animate out.
    closed: function (w) {
        if (effects.hasActiveFullScreenEffect || !isFadingWindow(w) || panelDirection(w)) {
            return;
        }
        if (!w.visible || w.skipsCloseAnimation) {
            return;
        }
        if (!effect.grab(w, Effect.WindowClosedGrabRole)) {
            return;
        }
        w.win98FadeOut = animate({
            window: w,
            curve: QEasingCurve.OutQuart,
            duration: animationTime(150) * 4,
            type: Effect.Opacity,
            from: 1.0,
            to: 0.0
        });
    },
    dataChanged: function (w, role) {
        if (!effect.isGrabbed(w, role)) {
            return;
        }
        if (role == Effect.WindowAddedGrabRole) {
            if (w.win98Slide) {
                cancel(w.win98Slide);
                delete w.win98Slide;
            }
            if (w.win98Fade) {
                cancel(w.win98Fade);
                delete w.win98Fade;
            }
        } else if (role == Effect.WindowClosedGrabRole && w.win98FadeOut) {
            cancel(w.win98FadeOut);
            delete w.win98FadeOut;
        }
    },
    init: function () {
        effects.windowAdded.connect(win98.added);
        effects.windowClosed.connect(win98.closed);
        effects.windowDataChanged.connect(win98.dataChanged);
    }
};

win98.init();
