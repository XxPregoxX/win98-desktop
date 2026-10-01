/*
    Chave liga/desliga do tema Win98: no 98 não existia chave, então ela é desenhada como a
    caixa de marcar (a do Kvantum, com o ✓ do 98). O resto é o Switch do KDE (org.kde.desktop).

    Baseado no Switch.qml do estilo QtQuick do KDE (qqc2-desktop-style,
    https://invent.kde.org/frameworks/qqc2-desktop-style), de Marco Martin e colaboradores.

    SPDX-FileCopyrightText: 2017 Marco Martin <mart@kde.org>
    SPDX-FileCopyrightText: 2017 The Qt Company Ltd.
    SPDX-FileCopyrightText: 2026 Leonardo Borges
    SPDX-License-Identifier: GPL-2.0-or-later
*/
import QtQuick
import org.kde.desktop as Desktop
import org.kde.desktop.private as Private

Desktop.Switch {
    id: control

    // mesmo espaço entre a caixa e o texto da caixa de marcar
    spacing: indicator && typeof indicator.pixelMetric === "function" ? indicator.pixelMetric("checkboxlabelspacing") : 4

    indicator: Private.CheckIndicator {
        x: if (control.contentItem !== null && control.contentItem.width > 0) {
            return control.mirrored ? control.width - width - control.rightPadding : control.leftPadding
        } else {
            return control.leftPadding + (control.availableWidth - width) / 2
        }
        y: control.topPadding + Math.round((control.availableHeight - height) / 2)
        control: control
        drawIcon: false
    }
}
