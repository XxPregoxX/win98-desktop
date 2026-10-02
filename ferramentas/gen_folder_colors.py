#!/usr/bin/env python3
"""Pastas coloridas e temáticas do "Criar nova pasta" do Dolphin (e de Propriedades > ícone).

O KDE oferece folder-red, folder-blue... e pastas temáticas (folder-games, folder-cloud...). O
Chicago95 não tem nenhuma: o KDE corta o nome até "folder" e todos os botões viram a mesma pasta.
No Windows 98 não existia pasta colorida, então não há desenho original pra usar.

1) Cores: a própria pasta do Chicago95 (places/<tam>/folder.png), com os mesmos pixels, pontilhado,
   contorno e brilho, trocando só o amarelo (#ffff00) e o amarelo-escuro (#808000) pelo par claro/
   escuro da cor, na paleta do Windows 98.
2) Temáticas: as pastas que o SE98 tem (folder-bookmark com estrela, nuvem, jogos, importante),
   copiadas pra dentro do Chicago95. Elas existem no SE98, mas o KDE nunca chega lá: corta o nome
   dentro do Chicago95 antes de olhar o tema pai. As que não têm desenho 98 em lugar nenhum
   (development, mail, tar, temp) continuam a pasta comum.

Grava em terceiros/Chicago95/places/<tam>/. Rodar de novo se reinstalar o Chicago95
(refazer_icones.sh já chama).
"""
import shutil
from pathlib import Path
from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
C95 = RAIZ / "terceiros/Chicago95/places"
SE98 = RAIZ / "terceiros/SE98/places"
TAMANHOS = ("16", "22", "24", "32", "48")
AMARELO, AMARELO_ESCURO = (0xff, 0xff, 0x00), (0x80, 0x80, 0x00)

# nome -> (cor clara, cor escura); as do VGA do 98, mais laranja e marrom da paleta de 256 cores
CORES = {
    "red": ("#ff0000", "#800000"),
    "orange": ("#ff8000", "#804000"),
    "green": ("#00ff00", "#008000"),
    "cyan": ("#00ffff", "#008080"),
    "blue": ("#0000ff", "#000080"),
    "violet": ("#ff00ff", "#800080"),
    "brown": ("#c08040", "#804000"),
    "grey": ("#ffffff", "#808080"),
}
# nome pedido pelo KDE -> nome no SE98
TEMATICAS = {
    "folder-bookmark": "folder-bookmark",
    "folder-cloud": "folder-yandex-disk",
    "folder-games": "folder-games",
    "folder-important": "folder_important",
}


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def gravar(destino: Path):
    """tira o que estiver no lugar (link pra pasta genérica, hardlink) antes de gravar"""
    if destino.is_symlink() or destino.exists():
        destino.unlink()


feitos = []
for tam in TAMANHOS:
    base = Image.open(C95 / tam / "folder.png").convert("RGBA")
    for cor, (clara, escura) in CORES.items():
        troca = {AMARELO: rgb(clara), AMARELO_ESCURO: rgb(escura)}
        im = base.copy()
        im.putdata([(*troca.get(p[:3], p[:3]), p[3]) for p in base.getdata()])
        destino = C95 / tam / f"folder-{cor}.png"
        gravar(destino)
        im.save(destino)
    # folder-yellow = a própria pasta
    destino = C95 / tam / "folder-yellow.png"
    gravar(destino)
    destino.symlink_to("folder.png")
    for nome, nome_se98 in TEMATICAS.items():
        origem = SE98 / tam / f"{nome_se98}.png"
        if origem.exists():
            destino = C95 / tam / f"{nome}.png"
            gravar(destino)
            shutil.copyfile(origem.resolve(), destino)
    feitos.append(tam)

print(f"pastas coloridas ({len(CORES) + 1} cores) e temáticas ({len(TEMATICAS)}) em: {', '.join(feitos)}px")
