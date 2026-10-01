# Credits

*[Versão em português](CREDITOS.md)*

This theme exists because a lot of people made good things and let others use them. Below is
everyone whose work shows up in the theme or helped build it, with a link to where it came from
and its license. If you reuse any part of this project, please keep these credits.

## Who made it

- **Leonardo Borges** ([XxPregoxX](https://github.com/XxPregoxX)): project author. Came up with the
  idea, decided how everything should look, tested it all in daily use and pointed out every detail
  that was off.
- **Claude** ([Anthropic](https://www.anthropic.com)), through [Claude Code](https://claude.com/claude-code):
  AI assistant that wrote the code, scripts, code-generated artwork and documentation together with
  Leonardo and under his direction.

## Third-party artwork and icons

| What | By | Where | License | Used for |
|---|---|---|---|---|
| **Chicago95** | grassmunk, AdrianoML, EMH-Mark-I and [contributors](https://github.com/grassmunk/Chicago95/graphs/contributors) | https://github.com/grassmunk/Chicago95 | GPL-3.0-or-later / MIT | Main icon theme, white cursor (Chicago95_Cursor_White), the Start button flag and the ▶ ❚❚ ■ symbols of the media buttons |
| **SE98** | [nestoris](https://github.com/nestoris) | https://github.com/nestoris/Win98SE | GPL-2.0 | Windows 98 SE style icons that fill Chicago95's gaps (file types, special folders, menu categories, actions) |
| **Windows 95 +PLUS+ Icon Pack #1** | [aconfuseddragon](https://aconfuseddragon.itch.io) | https://aconfuseddragon.itch.io/windows-95-plus-1 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | Google Chrome and Discord icons |
| **FOXSCAPEuC** | Michael Walden (code with Aris) | https://mw.rat.bz/foxscapeuc/ | [CC BY-NC-SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/) | Netscape buttons and animated "N" in Firefox |
| **98.css** | [Jordan Scales](https://github.com/jdan) | https://github.com/jdan/98.css | MIT | Windows 98 measurements, colors and 3D bevels, the checkbox ✓ and the radio button, recreated by the generators in `ferramentas/` |

- **Chicago95** and **SE98** are not stored in the repository: `ferramentas/baixar_terceiros.sh`
  downloads both straight from the original repositories, at a fixed version. The theme modifies
  the downloaded copy (scripts in `ferramentas/`). The modified artwork that is stored in the
  repository lives in `temas/icones/chicago95-ajustes/`, under the original licenses.
- Only the 2 **Windows 95 +PLUS+** icons that are used are included, unmodified, in
  `terceiros/Win95PLUS/`. The full pack is free on itch.io.
- The **FOXSCAPEuC** artwork is included, cropped, in `extras/firefox/chrome/netscape/`, under the
  same license (CC BY-NC-SA 3.0: attribution, **non-commercial**, derivatives under the same
  license). According to its author, this artwork comes from Netscape Communicator/Navigator, the
  Mozilla Application Suite, SeaMonkey and Firefox, collected and edited by him.
- The icon theme looks in Chicago95 first, then SE98, then
  **[candy-icons](https://github.com/EliverLara/candy-icons)** (by EliverLara, GPL-3.0; not included,
  only used if installed) and KDE's **Breeze**.

## Third-party code

| What | By | Where | License | Used for |
|---|---|---|---|---|
| **Kickoff** (Plasma 6.7.5 application launcher) | Mikel Johnson, Noah Davis, Tanbir Jishan, Fushan Wen, Martin Gräßlin and the KDE community | https://invent.kde.org/plasma/plasma-desktop (`applets/kickoff`) | GPL-2.0-or-later | Base of the Start button (`plasmoides/org.kde.plasma.win98kickoff`, a copy with changes marked `Win98`) |
| **KWin effects**: Fading popups, Scale, Squash | Vlad Zahorodnii | https://invent.kde.org/plasma/kwin | GPL-2.0-or-later | Structure and window blacklist of the `kwin/win98menuslide` and `kwin/win98windows` effects |
| **qqc2-desktop-style** (KDE's QtQuick style) | Marco Martin, The Qt Company and contributors | https://invent.kde.org/frameworks/qqc2-desktop-style | LGPL-3.0-only OR GPL-2.0-or-later | Base of the QML controls in `qml/org/kde/win98` |

Each of these files keeps the original authors in its header (SPDX).

## Software and libraries used

Not included in the repository, but the theme would not exist without them:

- **[KDE Plasma, KWin and Aurorae](https://kde.org)**, by the KDE community: the desktop this theme
  dresses up.
- **[Kvantum](https://github.com/tsujan/Kvantum)**, by Pedram Pourang (tsujan), GPL-3.0: the engine
  that draws the 3D bevels in Qt apps.
- **[Qt](https://www.qt.io) and [PySide6](https://doc.qt.io/qtforpython-6/)**, by The Qt Company:
  render and test many of the generated icons and buttons.
- **[Pillow](https://python-pillow.org)**, by Jeffrey A. Clark and contributors: image work in the generators.
- **[ImageMagick](https://imagemagick.org)**: resizing and converting icons.
- **[SoX](https://sourceforge.net/projects/sox/)**: the theme sounds were synthesized with it
  (new sounds in the 98 style, not Microsoft's originals).
- **[Liberation Sans](https://github.com/liberationfonts/liberation-fonts)**, by Red Hat, SIL OFL 1.1:
  the theme font, standing in for MS Sans Serif.
- **[Mozilla Firefox](https://www.mozilla.org/firefox/)**: the Netscape theme is a `userChrome.css`.
- **[Python](https://www.python.org)**, **[Node.js](https://nodejs.org)** (tests) and
  **[Fedora Linux](https://fedoraproject.org)**, where everything was made and tested.

## In the screenshots

- The "before" screenshot shows KDE Plasma 6's default wallpaper, **Waterfall**, by Krystian Zajdel
  ([CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)).
- The Firefox screenshot shows the Portuguese Wikipedia article
  ["Netscape Navigator"](https://pt.wikipedia.org/wiki/Netscape_Navigator)
  ([CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)), including the Netscape logo.

## Trademarks

Windows and Windows 98 are trademarks of Microsoft. Netscape and Netscape Communicator are
trademarks of Netscape Communications / AOL. Google Chrome is a trademark of Google; Discord, of
Discord Inc. This is a fan project, not affiliated with any of these companies. No Windows files
are included: the look was recreated.

## Project license

Everything made here (scripts, themes, effects, code-generated artwork and documentation) is
**GPL-3.0-or-later** ([`LICENSE`](LICENSE)). The exceptions are the third-party parts above, which
keep their original license:

| Folder / files | License |
|---|---|
| `plasmoides/org.kde.plasma.win98kickoff/`, `kwin/*/contents/code/main.js`, `qml/org/kde/win98/` | GPL-2.0-or-later |
| `temas/icones/chicago95-ajustes/` | Chicago95 (GPL-3.0-or-later / MIT) and SE98 (GPL-2.0) |
| `temas/icones/botao-iniciar/` (the flag) | Chicago95 (GPL-3.0-or-later / MIT) |
| `terceiros/Win95PLUS/` | CC BY 4.0 |
| `extras/firefox/chrome/netscape/` | CC BY-NC-SA 3.0 |

License texts are in [`LICENSES/`](LICENSES/).
