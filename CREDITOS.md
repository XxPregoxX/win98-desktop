# Créditos

*[English version](CREDITS.md)*

Este tema existe porque muita gente fez coisa boa e deixou os outros usarem. Aqui está todo
mundo cujo trabalho aparece no tema ou ajudou a construir ele, com o link de onde veio e a licença.
Se você usar alguma parte deste projeto, mantenha estes créditos.

## Quem fez

- **Leonardo Borges** ([XxPregoxX](https://github.com/XxPregoxX)): autor do projeto. Teve a ideia,
  decidiu o visual, testou tudo no dia a dia e apontou cada detalhe que estava fora do lugar.
- **Claude** ([Anthropic](https://www.anthropic.com)), pelo [Claude Code](https://claude.com/claude-code):
  assistente de IA que escreveu, junto com o Leonardo e sob a direção dele, o código, os scripts, os
  desenhos gerados por código e a documentação.

## Desenhos e ícones de terceiros

| O quê | De quem | Onde | Licença | Usado pra |
|---|---|---|---|---|
| **Chicago95** | grassmunk, AdrianoML, EMH-Mark-I e [colaboradores](https://github.com/grassmunk/Chicago95/graphs/contributors) | https://github.com/grassmunk/Chicago95 | GPL-3.0-or-later / MIT | Tema de ícones principal, cursor branco (Chicago95_Cursor_White), a bandeira do botão Iniciar e os símbolos ▶ ❚❚ ■ dos botões de mídia |
| **SE98** | [nestoris](https://github.com/nestoris) | https://github.com/nestoris/Win98SE | GPL-2.0 | Ícones no estilo Windows 98 SE que tapam os buracos do Chicago95 (tipos de arquivo, pastas especiais, categorias do menu, ações) |
| **Windows 95 +PLUS+ Icon Pack #1** | [aconfuseddragon](https://aconfuseddragon.itch.io) | https://aconfuseddragon.itch.io/windows-95-plus-1 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | Ícones do Google Chrome e do Discord |
| **FOXSCAPEuC** | Michael Walden (código com Aris) | https://mw.rat.bz/foxscapeuc/ | [CC BY-NC-SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/) | Botões e "N" animado do Netscape no Firefox |
| **Oldschool PC Font Pack** (fonte PxPlus IBM VGA 8x16) | [VileR](https://int10h.org) | https://int10h.org/oldschool-pc-fonts/ | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) | A fonte do modo texto do VGA da IBM, com acentos, no Prompt do MS-DOS (Konsole); vai sem alteração em `temas/fontes/` |
| **98.css** | [Jordan Scales](https://github.com/jdan) | https://github.com/jdan/98.css | MIT | Medidas, cores e relevo 3D do Windows 98, o ✓ da caixa de marcar e o botão de rádio, recriados pelos geradores de `ferramentas/` |

- O **Chicago95** e o **SE98** não vão no repositório: `ferramentas/baixar_terceiros.sh` baixa os
  dois direto dos repositórios originais, numa versão fixa. O tema altera a cópia baixada (scripts
  em `ferramentas/`). Os desenhos já alterados que vão no repositório ficam em
  `temas/icones/chicago95-ajustes/`, sob as licenças originais.
- Do **Windows 95 +PLUS+** só vão os 2 ícones usados, sem alteração, em `terceiros/Win95PLUS/`.
  O pacote inteiro é grátis no itch.io.
- Os desenhos do **FOXSCAPEuC** vão recortados em `extras/firefox/chrome/netscape/`, sob a mesma
  licença (CC BY-NC-SA 3.0: com crédito, **sem uso comercial**, e derivados com a mesma licença).
  Segundo o autor, esses desenhos vêm do Netscape Communicator/Navigator, do Mozilla Application
  Suite, do SeaMonkey e do Firefox, e foram juntados e tratados por ele.
- O tema de ícones procura primeiro no Chicago95, depois no SE98, no
  **[candy-icons](https://github.com/EliverLara/candy-icons)** (de EliverLara, GPL-3.0; não vem
  junto, só é usado se estiver instalado) e no **Breeze** do KDE.

## Código de terceiros

| O quê | De quem | Onde | Licença | Usado pra |
|---|---|---|---|---|
| **Kickoff** (menu de aplicativos do Plasma 6.7.5) | Mikel Johnson, Noah Davis, Tanbir Jishan, Fushan Wen, Martin Gräßlin e a comunidade KDE | https://invent.kde.org/plasma/plasma-desktop (`applets/kickoff`) | GPL-2.0-or-later | Base do botão Iniciar (`plasmoides/org.kde.plasma.win98kickoff`, cópia com alterações marcadas `Win98`) |
| **Efeitos do KWin**: Fading popups, Scale, Squash | Vlad Zahorodnii | https://invent.kde.org/plasma/kwin | GPL-2.0-or-later | Estrutura e lista de janelas ignoradas dos efeitos `kwin/win98menuslide` e `kwin/win98windows` |
| **Barras de ferramentas do Konsole** (`konsoleui.rc`, `sessionui.rc` da versão 26.08.0) | Comunidade KDE | https://invent.kde.org/utilities/konsole | GPL-2.0-or-later | Base da barra do Prompt do MS-DOS (`temas/konsole/kxmlgui/`) |
| **qqc2-desktop-style** (estilo QtQuick do KDE) | Marco Martin, The Qt Company e colaboradores | https://invent.kde.org/frameworks/qqc2-desktop-style | LGPL-3.0-only OR GPL-2.0-or-later | Base dos controles QML em `qml/org/kde/win98` |

Cada arquivo desses mantém no cabeçalho os nomes dos autores originais (SPDX).

## Programas e bibliotecas usados

Não vão no repositório, mas o tema não existiria sem eles:

- **[KDE Plasma, KWin e Aurorae](https://kde.org)**, da comunidade KDE: o ambiente de trabalho que o
  tema veste.
- **[Kvantum](https://github.com/tsujan/Kvantum)**, de Pedram Pourang (tsujan), GPL-3.0: o motor
  que desenha o relevo 3D nos apps Qt.
- **[Qt](https://www.qt.io) e [PySide6](https://doc.qt.io/qtforpython-6/)**, da The Qt Company:
  desenham e testam boa parte dos ícones e botões gerados.
- **[Pillow](https://python-pillow.org)**, de Jeffrey A. Clark e colaboradores: imagens nos geradores.
- **[ImageMagick](https://imagemagick.org)**: redimensionar e converter ícones.
- **[SoX](https://sourceforge.net/projects/sox/)**: os sons do tema foram sintetizados com ele
  (são sons novos no estilo do 98, não os originais da Microsoft).
- **[Liberation Sans](https://github.com/liberationfonts/liberation-fonts)**, da Red Hat, SIL OFL 1.1:
  a fonte do tema, no lugar da MS Sans Serif.
- **[Mozilla Firefox](https://www.mozilla.org/firefox/)**: o tema do Netscape é um `userChrome.css`.
- **[Python](https://www.python.org)**, **[Node.js](https://nodejs.org)** (testes) e o
  **[Fedora Linux](https://fedoraproject.org)**, onde tudo foi feito e testado.

## Nos prints

- O print "antes" mostra o papel de parede padrão do KDE Plasma 6, **Waterfall**, de Krystian Zajdel
  ([CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)).
- O print do Firefox mostra o artigo
  ["Netscape Navigator" da Wikipédia](https://pt.wikipedia.org/wiki/Netscape_Navigator)
  ([CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)), com o logo do Netscape.

## Marcas

Windows e Windows 98 são marcas da Microsoft. Netscape e Netscape Communicator são marcas da
Netscape Communications / AOL. Google Chrome é marca do Google; Discord, da Discord Inc. Este é um
projeto de fãs, sem ligação com nenhuma dessas empresas. Nenhum arquivo do Windows vem junto: o
visual foi recriado.

## Licença do projeto

O que foi feito aqui (scripts, temas, efeitos, desenhos gerados por código e documentação) é
**GPL-3.0-or-later** ([`LICENSE`](LICENSE)). As exceções são as partes de terceiros acima, que
mantêm a licença original:

| Pasta / arquivos | Licença |
|---|---|
| `plasmoides/org.kde.plasma.win98kickoff/`, `kwin/*/contents/code/main.js`, `qml/org/kde/win98/` | GPL-2.0-or-later |
| `temas/icones/chicago95-ajustes/` | Chicago95 (GPL-3.0-or-later / MIT) e SE98 (GPL-2.0) |
| `temas/icones/botao-iniciar/` (a bandeira) | Chicago95 (GPL-3.0-or-later / MIT) |
| `terceiros/Win95PLUS/` | CC BY 4.0 |
| `extras/firefox/chrome/netscape/` | CC BY-NC-SA 3.0 |
| `temas/fontes/` (fonte PxPlus IBM VGA 8x16) | CC BY-SA 4.0 |
| `temas/konsole/kxmlgui/` | GPL-2.0-or-later |

Os textos das licenças estão em [`LICENSES/`](LICENSES/).
