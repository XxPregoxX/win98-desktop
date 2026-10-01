/*
    Item de lista com chave (ex.: "Bluetooth" nas Configurações) no tema Win98: a chave vira a
    caixa de marcar do 98, como em Switch.qml. O resto é o SwitchDelegate do KDE.

    Baseado no SwitchDelegate.qml do estilo QtQuick do KDE (qqc2-desktop-style,
    https://invent.kde.org/frameworks/qqc2-desktop-style), de Marco Martin e colaboradores.

    SPDX-FileCopyrightText: 2017 Marco Martin <mart@kde.org>
    SPDX-FileCopyrightText: 2017 The Qt Company Ltd.
    SPDX-FileCopyrightText: 2026 Leonardo Borges
    SPDX-License-Identifier: GPL-2.0-or-later
*/
import QtQuick
import QtQuick.Templates as T
import org.kde.desktop as Desktop
import org.kde.desktop.private as Private

Desktop.SwitchDelegate {
    id: controlRoot

    indicator: Private.CheckIndicator {
        x: !controlRoot.mirrored ? controlRoot.horizontalPadding : controlRoot.width - width - controlRoot.horizontalPadding
        y: controlRoot.topPadding + (controlRoot.display === T.AbstractButton.TextUnderIcon ? 0 : ((controlRoot.availableHeight - height) / 2))
        control: controlRoot
        drawIcon: false
    }
}
