# Cópia SÓ PARA O UPLOAD no Mixamo: encolhe a cabeça (o auto-rigger recusa a proporção cartoon)
# e grava os parâmetros em JSON para desfazer depois, por posição, no GLB com esqueleto.
# Uso: python encolher_cabeca.py <entrada.glb> <saida.zip> <params.json> [fator=0.6]
import sys, os, json, zipfile, tempfile
import numpy as np, trimesh

ent, saida, pjson = sys.argv[1], sys.argv[2], sys.argv[3]
fator = float(sys.argv[4]) if len(sys.argv) > 4 else 0.6

cena = trimesh.load(ent)
m = list(cena.geometry.values())[0].copy()

# --- peças soltas (union-find sobre os vértices fundidos) ---
mf = m.copy(); mf.merge_vertices(merge_tex=True, merge_norm=True)
pai = np.arange(len(mf.vertices))
def raiz(i):
    while pai[i] != i:
        pai[i] = pai[pai[i]]; i = pai[i]
    return i
for a, b in mf.edges_unique:
    ra, rb = raiz(a), raiz(b)
    if ra != rb: pai[ra] = rb
r = np.array([raiz(i) for i in range(len(pai))])
ids, cont = np.unique(r[mf.faces[:, 0]], return_counts=True)
print("peças soltas:", len(ids), "| faces por peça:", sorted(cont.tolist(), reverse=True)[:8])

# --- normaliza como no preparar_mixamo: pés em 0, centrado, 120 de altura ---
v = m.vertices.copy()
alt0 = v[:, 1].max() - v[:, 1].min()
off = np.array([-(v[:, 0].max() + v[:, 0].min()) / 2, -v[:, 1].min(), -(v[:, 2].max() + v[:, 2].min()) / 2])
esc = 120.0 / alt0
v = (v + off) * esc

# --- encolhe a cabeça: pivô no queixo, centro do pescoço; transição suave na faixa do pescoço ---
H = 120.0
y_queixo = 0.655 * H
y_ini = 0.625 * H                     # abaixo disso (ombros, alças) nada muda
pesc = v[(v[:, 1] > y_ini) & (v[:, 1] < y_queixo)]
pesc = pesc[np.abs(pesc[:, 0]) < 0.12 * H]
piv = np.array([np.median(pesc[:, 0]), y_queixo, np.median(pesc[:, 2])])
t = np.clip((v[:, 1] - y_ini) / (y_queixo - y_ini), 0, 1)
t = t * t * (3 - 2 * t)
s = 1 - (1 - fator) * t
v2 = piv + (v - piv) * s[:, None]
m.vertices = v2
print("altura original 120 -> com cabeça encolhida:", round(v2[:, 1].max(), 1))

params = {"entrada": ent, "offset_normalizacao": off.tolist(), "escala_normalizacao": esc,
          "altura_normalizada": H, "fator_cabeca": fator, "pivo": piv.tolist(),
          "y_inicio_faixa": y_ini, "y_queixo": y_queixo,
          "como_desfazer": "para cada vértice (nas unidades normalizadas): t = smoothstep((y - y_ini)/(y_queixo - y_ini)) "
                           "calculado na posição ENCOLHIDA aproximada; s = 1 - (1-fator)*t; p_original = piv + (p - piv)/s. "
                           "Alinhar o GLB do Mixamo a estas unidades pela caixa do corpo (pés aos ombros) antes."}
json.dump(params, open(pjson, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

tmp = tempfile.mkdtemp()
m.export(os.path.join(tmp, "pintor.obj"), file_type="obj", include_texture=True, mtl_name="pintor.mtl")
with zipfile.ZipFile(saida, "w", zipfile.ZIP_DEFLATED) as z:
    for f in os.listdir(tmp):
        z.write(os.path.join(tmp, f), f)
print("salvo:", saida, os.path.getsize(saida))
