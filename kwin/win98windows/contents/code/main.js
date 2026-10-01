/*
    Win98 Windows: efeito do KWin do tema win98-desktop.

    Baseado nos efeitos padrão "Scale" e "Squash" do KWin, de Vlad Zahorodnii
    (lista de janelas ignoradas e estrutura dos eventos de janela).

    SPDX-FileCopyrightText: 2018, 2021 Vlad Zahorodnii <vlad.zahorodnii@kde.org>
    SPDX-FileCopyrightText: 2026 Leonardo Borges
    SPDX-License-Identifier: GPL-2.0-or-later
*/

"use strict";
// Win98 Windows
//
// Window animations in the spirit of Windows 98:
// - open / close: Windows 98 had none. Here the window unrolls down from its title bar
//   (like the 98 menus, see win98menuslide) and rolls back up into it when closed.
// - minimize / unminimize: Windows 9x zoomed the title bar into the taskbar button. A KWin
//   script can't show only the title bar away from the window's own place (Effect.Clip is
//   bound to the window geometry, and a shader sees the decoration and the contents as
//   separate textures), so the whole window zooms, straight and linear, into its taskbar
//   button and back. No fade, no genie.
// Maximize is left to the stock effect. Replaces scale, fade, squash and magic lamp.

var DEBUG = effect.readConfig("Debug", false);   // kwinrc [Effect-win98windows] Debug=true
var OPEN_MS = 150;         // unroll when a window opens
var CLOSE_MS = 150;        // roll up when it closes
var ZOOM_MS = 200;         // minimize / unminimize
var CAPTION_FALLBACK = 30; // px to start from when a window has no title bar of its own

var TOP = typeof Effect.Top == "number" ? Effect.Top : 2;

var blacklist = [
    "ksmserver ksmserver",
    "ksmserver-logout-greeter ksmserver-logout-greeter",
    "kscreenlocker_greet kscreenlocker_greet",
    "ksplashqml ksplashqml",
    "spectacle org.kde.spectacle",
    "spectacle spectacle",
];

function log(msg) {
    if (DEBUG) {
        print("win98windows: " + msg);
    }
}

// > 1 slows everything down, for testing (kwinrc [Effect-win98windows] SlowFactor=40)
function slow() {
    return effect.readConfig("SlowFactor", 1) || 1;
}

function isWin98Window(w) {
    if (blacklist.indexOf(w.windowClass) != -1) {
        return false;
    }
    if (w.windowClass == "plasmashell plasmashell" || w.windowClass == "plasmashell org.kde.plasmashell") {
        return w.hasDecoration;
    }
    if (w.hasDecoration) {
        return true;
    }
    if (w.popupWindow || w.lockScreen || w.outline || !w.managed) {
        return false;
    }
    return w.normalWindow || w.dialog;
}

// Height of the title bar: where the window contents start. Windows without a
// decoration of ours (client-side title bars) get a fixed strip.
function captionHeight(w) {
    var cr = w.contentsRect;
    var h = cr && cr.y > 0 ? cr.y : CAPTION_FALLBACK;
    return Math.min(h, w.geometry.height);
}

// Clip that shows the top `fraction` of the window (1 = all of it).
function topClip(fromFraction, toFraction) {
    return {
        type: Effect.Clip,
        sourceAnchor: TOP,
        targetAnchor: TOP,
        from: { value1: 1, value2: fromFraction },
        to: { value1: 1, value2: toFraction }
    };
}

// Where a minimized window goes: its taskbar button, or the bottom left corner of its
// screen if nothing tells us (no task manager).
function iconTarget(w) {
    var icon = w.iconGeometry;
    if (icon && icon.width > 0 && icon.height > 0) {
        return icon;
    }
    var area = w.screen && w.screen.geometry ? w.screen.geometry : w.geometry;
    var h = captionHeight(w);
    return { x: area.x, y: area.y + area.height - h, width: Math.min(160, w.geometry.width), height: h };
}

// Size + translation (Effect.Size scales around the window center) that put the
// window on the rectangle `r`.
function onto(win, r) {
    return {
        size: { value1: r.width, value2: r.height },
        offset: {
            value1: r.x - win.x - (win.width - r.width) / 2,
            value2: r.y - win.y - (win.height - r.height) / 2
        }
    };
}

function stop(w, name) {
    if (w[name]) {
        cancel(w[name]);
        delete w[name];
    }
}

function zoom(w, toIcon) {
    var win = w.geometry;
    var here = onto(win, win);
    var icon = onto(win, iconTarget(w));
    var a = toIcon ? here : icon;
    var b = toIcon ? icon : here;
    return animate({
        window: w,
        duration: animationTime(ZOOM_MS) * slow(),
        curve: QEasingCurve.Linear,
        keepAlive: false,
        animations: [
            { type: Effect.Size, from: a.size, to: b.size },
            { type: Effect.Translation, from: a.offset, to: b.offset }
        ]
    });
}

function minimizedChanged(w) {
    if (effects.hasActiveFullScreenEffect || !isWin98Window(w)) {
        return;
    }
    stop(w, "win98Minimize");
    stop(w, "win98Unminimize");
    log((w.minimized ? "minimize " : "unminimize ") + w.caption);
    if (w.minimized) {
        w.win98Minimize = zoom(w, true);
    } else {
        w.win98Unminimize = zoom(w, false);
    }
}

function manage(w) {
    w.minimizedChanged.connect(function () {
        minimizedChanged(w);
    });
}

function added(w) {
    manage(w);
    if (effects.hasActiveFullScreenEffect || !isWin98Window(w) || !w.visible) {
        return;
    }
    if (effect.isGrabbed(w, Effect.WindowAddedGrabRole)) {
        return;
    }
    effect.grab(w, Effect.WindowAddedGrabRole);
    var cap = captionHeight(w);
    log("open " + w.caption + " cap=" + cap + " h=" + w.geometry.height);
    w.win98Open = animate({
        window: w,
        duration: animationTime(OPEN_MS) * slow(),
        curve: QEasingCurve.Linear,
        animations: [topClip(cap / w.geometry.height, 1)]
    });
}

function closed(w) {
    if (effects.hasActiveFullScreenEffect || !isWin98Window(w) || !w.visible || w.skipsCloseAnimation) {
        return;
    }
    if (effect.isGrabbed(w, Effect.WindowClosedGrabRole)) {
        return;
    }
    effect.grab(w, Effect.WindowClosedGrabRole);
    stop(w, "win98Open");
    var cap = captionHeight(w);
    log("close " + w.caption + " cap=" + cap);
    animate({
        window: w,
        duration: animationTime(CLOSE_MS) * slow(),
        curve: QEasingCurve.Linear,
        animations: [topClip(1, cap / w.geometry.height)]
    });
}

effects.windowAdded.connect(added);
effects.windowClosed.connect(closed);
for (var i = 0; i < effects.stackingOrder.length; i++) {
    manage(effects.stackingOrder[i]);
}
