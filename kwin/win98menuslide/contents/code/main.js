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
var REDO_MS = 100;        // a popup redone this soon after the app closed one appears without sliding
                          // (e.g. LibreOffice's column width tooltip, recreated on every drag step)
var TOLERANCE = 4;        // px between pointer and popup edge that still counts as "touching"

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

var lastPopupClose = {};  // windowClass -> when that app last closed a sliding popup (ms)

var win98 = {
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
            // a popup closed mid-slide vanishes at once (like Windows 98 menus), instead of
            // being kept on screen until the slide ends
            keepAlive: false,
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
        if (slide && !panelDir) {
            var closedAt = lastPopupClose[w.windowClass];
            if (closedAt !== undefined && Date.now() - closedAt < REDO_MS) {
                if (DEBUG) {
                    console.warn("win98menuslide redone popup, no slide: " + w.windowClass);
                }
                return;
            }
        }
        if (slide) {
            win98.slideIn(w, panelDir);
            // A popup that moves while sliding (e.g. LibreOffice's column width tooltip, which
            // follows the drag) would leave stale slide frames behind: stop the slide and repaint.
            // KWin 6: this signal lives on each window, not on "effects".
            if (!w.win98Watched && w.windowFrameGeometryChanged && w.windowFrameGeometryChanged.connect) {
                w.win98Watched = true;
                w.windowFrameGeometryChanged.connect(function () {
                    if (w.win98Slide) {
                        if (DEBUG) {
                            console.warn("win98menuslide moved while sliding: " + w.windowClass);
                        }
                        cancel(w.win98Slide);
                        delete w.win98Slide;
                        effects.addRepaintFull();
                    }
                });
            }
        } else {
            win98.fadeIn(w);
        }
    },
    // Windows 98 menus vanish instantly; only the fading windows animate out.
    closed: function (w) {
        if (isSlidingWindow(w)) {
            lastPopupClose[w.windowClass] = Date.now();
        }
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
