/*
    Item de lista do tema Win98: igual ao do KDE (org.kde.desktop), mais uma linha fina
    separando os itens, pra lista não parecer um bloco branco antes do hover.
    A caixa do hover/seleção ocupa o item todo, de uma linha até a outra (no hover ela cobre
    as duas linhas, a de cima e a de baixo, e vira um campo afundado só); a linha usa a cor
    "dark" da paleta (segue o esquema de cores). Não aparece em menus e listas de
    caixa de seleção (popups), em tabelas, nem depois do último item.

    Baseado no ItemDelegate.qml do estilo QtQuick do KDE (qqc2-desktop-style,
    https://invent.kde.org/frameworks/qqc2-desktop-style), de Marco Martin e colaboradores.

    SPDX-FileCopyrightText: 2017 Marco Martin <mart@kde.org>
    SPDX-FileCopyrightText: 2017 The Qt Company Ltd.
    SPDX-FileCopyrightText: 2026 Leonardo Borges
    SPDX-License-Identifier: GPL-2.0-or-later
*/
import QtQuick
import org.kde.desktop as Desktop
import org.kde.desktop.private as Private

Desktop.ItemDelegate {
    id: control

    function win98InPopup(): bool {
        for (let p = control.parent; p; p = p.parent) {
            if (String(p).startsWith("QQuickPopupItem")) {
                return true;
            }
        }
        return false;
    }

    readonly property bool win98Separator: ListView.view !== null && !TableView.view
        && !(typeof index !== "undefined" && ListView.view.count === index + 1)
        && !win98InPopup()

    // a caixa do hover/seleção vai de uma linha até a outra: sem vão em cima,
    // e embaixo só o espaço da linha (o conteúdo continua no mesmo lugar, pelo padding)
    // no hover o afundado cobre a linha de cima (a do item anterior) e a de baixo (a dele):
    // fica um campo só entre os dois vizinhos, sem linha dobrada
    readonly property bool win98HoverBox: hovered && !highlighted && !down && ListView.view !== null
        && !TableView.view && !win98InPopup()
    z: win98HoverBox ? 1 : 0
    topInset: win98HoverBox && typeof index !== "undefined" && index > 0 ? -1 : 0
    bottomInset: win98Separator && !win98HoverBox ? 1 : 0

    background: Item {
        Private.DefaultListItemBackground {
            anchors.fill: parent
            control: control
        }
        // linha "dark" da paleta (a do separador dos menus do 98), logo abaixo da caixa
        Rectangle {
            visible: control.win98Separator && !control.win98HoverBox
            // mesma largura da caixa do hover/seleção (mesma conta das margens do
            // DefaultListItemBackground do org.kde.desktop)
            x: Math.min(0, -(control.leftPadding - control.leftInset))
            y: parent.height
            width: parent.width - x + (control.rightPadding - control.rightInset)
            height: 1
            color: control.palette.dark
        }
    }
}
