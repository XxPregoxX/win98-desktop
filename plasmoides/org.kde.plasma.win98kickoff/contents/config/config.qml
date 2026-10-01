/*
    SPDX-FileCopyrightText: 2013 Marco Martin <mart@kde.org>

    SPDX-License-Identifier: GPL-2.0-or-later
*/

import QtQuick

import org.kde.plasma.configuration as PlasmaConfig

PlasmaConfig.ConfigModel {
    PlasmaConfig.ConfigCategory {
        name: i18ndc("plasma_applet_org.kde.plasma.kickoff", "@title:group for configuration dialog page", "General") // qmllint disable unqualified
        icon: "preferences-desktop-plasma"
        source: "ConfigGeneral.qml"
    }
}
