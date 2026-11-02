"""Copia a biblioteca componentes-3d (e os personagens pedidos) para dentro de um projeto HyperFrames.

O HyperFrames só serve arquivos de dentro da pasta do projeto, então cada vídeo leva uma cópia em
<projeto>/assets/c3d/. Rode de novo sempre que a biblioteca mudar (a cópia é sobrescrita).

Uso: python componentes-3d/instalar.py <pasta-do-projeto> [personagem ...]
Ex.: python componentes-3d/instalar.py house/videos/fachada-do-zero pintor
"""
import os
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)

if len(sys.argv) < 2:
    sys.exit(__doc__)
proj = os.path.abspath(sys.argv[1])
destino = os.path.join(proj, "assets", "c3d")
os.makedirs(destino, exist_ok=True)

n = 0
for pasta, _, arquivos in os.walk(AQUI):
    rel = os.path.relpath(pasta, AQUI)
    if rel.startswith("catalogo"):
        continue
    for a in arquivos:
        if a.endswith(".js"):
            alvo = os.path.join(destino, rel)
            os.makedirs(alvo, exist_ok=True)
            shutil.copy2(os.path.join(pasta, a), os.path.join(alvo, a))
            n += 1

for p in sys.argv[2:]:
    glb = os.path.join(RAIZ, "personagens", p, "final", p + ".glb")
    if not os.path.exists(glb):
        sys.exit(f"personagem não encontrado: {glb}")
    shutil.copy2(glb, os.path.join(destino, "personagens", p + ".glb"))
    n += 1

print(f"{n} arquivos em {os.path.relpath(destino, RAIZ)}")
