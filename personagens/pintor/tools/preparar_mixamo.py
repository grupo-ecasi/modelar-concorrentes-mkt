# Prepara o modelo para o upload no Mixamo: OBJ + MTL + textura num ZIP,
# com os pés em Y=0, centralizado e ~120 cm de altura.
# IMPORTANTE: o OBJ sai com as POSIÇÕES SOLDADAS (um "v" por ponto do espaço) e as UVs em índices
# separados ("vt"). Exportar direto pelo trimesh duplica os vértices nas emendas da textura e o
# Mixamo enxerga a malha como retalhos soltos: o auto-rigger falha sem mensagem.
# Uso: python preparar_mixamo.py <entrada.glb> <saida.zip>
import sys, os, zipfile, tempfile
import numpy as np, trimesh

ent, saida = sys.argv[1], sys.argv[2]
cena = trimesh.load(ent)
m = list(cena.geometry.values())[0]
v = m.vertices.astype(np.float64)
v = v - [(v[:, 0].max() + v[:, 0].min()) / 2, v[:, 1].min(), (v[:, 2].max() + v[:, 2].min()) / 2]
v *= 120.0 / v[:, 1].max()
uv = m.visual.uv
F = m.faces

# solda as posições: mesma coordenada (arredondada) => mesmo índice
chave = np.round(v, 5)
unicos, inv = np.unique(chave, axis=0, return_inverse=True)
inv = inv.ravel()
print("vértices:", len(v), "-> soldados:", len(unicos), "| faces:", len(F))

tmp = tempfile.mkdtemp()
tex = m.visual.material.baseColorTexture.convert("RGB")
tex.save(os.path.join(tmp, "pintor.png"))
with open(os.path.join(tmp, "pintor.mtl"), "w") as f:
    f.write("newmtl pintor\nKa 0 0 0\nKd 1 1 1\nKs 0 0 0\nNs 1\nmap_Kd pintor.png\n")
with open(os.path.join(tmp, "pintor.obj"), "w") as f:
    f.write("mtllib pintor.mtl\no pintor\n")
    f.write("".join("v %.5f %.5f %.5f\n" % tuple(p) for p in unicos))
    f.write("".join("vt %.6f %.6f\n" % tuple(t) for t in uv))
    f.write("usemtl pintor\n")
    for a, b, c in F:
        f.write("f %d/%d %d/%d %d/%d\n" % (inv[a] + 1, a + 1, inv[b] + 1, b + 1, inv[c] + 1, c + 1))
with zipfile.ZipFile(saida, "w", zipfile.ZIP_DEFLATED) as z:
    for nome in os.listdir(tmp):
        z.write(os.path.join(tmp, nome), nome)
print("salvo:", saida, os.path.getsize(saida))
