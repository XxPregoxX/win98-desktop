# Carregado pelo Plasma ao entrar na sessão (~/.config/plasma-workspace/env/).
# Liga a camada de estilo QML do tema (qml/org/kde/win98), que por cima do estilo do KDE
# acrescenta a linha separando os itens de lista. Pra desligar: apagar este arquivo e sair
# e entrar na sessão de novo.
export QML_IMPORT_PATH="$HOME/.local/share/win98-qml${QML_IMPORT_PATH:+:$QML_IMPORT_PATH}"
export QT_QUICK_CONTROLS_STYLE=org.kde.win98
