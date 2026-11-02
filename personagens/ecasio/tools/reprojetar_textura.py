# Reprojeta as imagens de conceito (frente e lado) na textura do modelo 3D, sem mudar a forma nem as UVs.
# Corrige o que o conversor 3D estragou na textura (boca, olhos, logo, manchas), usando o desenho original.
#
# Uso: python reprojetar_textura.py <entrada.glb> <saida.glb>
#   --frente conceito/frente.png      projeção ortográfica ao longo de -Z (corpo todo, peso pela normal)
#   --lado conceito/vista-lado.png    projeção ao longo de X na cabeça (lado +X e espelhada no lado -X)
#
# Alinhamento: a caixa da silhueta (pixels não brancos) de cada imagem é casada com a caixa do modelo
# nos eixos daquela vista (altura dos pés ao topo do cabelo, centro horizontal).
import sys, argparse
import numpy as np
import trimesh
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("entrada"); ap.add_argument("saida")
ap.add_argument("--frente", default="conceito/frente.png")
ap.add_argument("--lado", default="conceito/vista-lado.png")
ap.add_argument("--debug", default=None, help="salva a máscara de pesos em PNG")
a = ap.parse_args()

cena = trimesh.load(a.entrada)
nome_geo, malha = next(iter(cena.geometry.items()))
V = malha.vertices.astype(np.float64)
F = malha.faces
N = malha.vertex_normals.astype(np.float64)
UV = malha.visual.uv.astype(np.float64)
mat = malha.visual.material
tex = np.asarray(mat.baseColorTexture.convert("RGB")).astype(np.float32)
TH, TW = tex.shape[:2]

ymin, ymax = V[:, 1].min(), V[:, 1].max()
alt = ymax - ymin


def mascara(img, limiar=240, erosao=9):
    from PIL import ImageFilter
    arr = np.asarray(img).astype(np.int16)
    m = (arr < limiar).any(axis=2)
    ys, xs = np.nonzero(m)
    caixa = (xs.min(), xs.max(), ys.min(), ys.max())          # caixa medida antes da erosão
    me = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(erosao))
    return arr.astype(np.float32), np.asarray(me) > 127, caixa


def zbuffer(px, py, prof, shape, escala=0.5):
    """Rasteriza a malha projetada e guarda a maior profundidade (mais perto da câmera) por pixel."""
    h, w = int(shape[0] * escala), int(shape[1] * escala)
    zb = np.full((h, w), -np.inf, np.float32)
    X = px * escala; Y = py * escala
    for f in F:
        x = X[f]; y = Y[f]; z = prof[f]
        x0 = max(int(np.floor(x.min())), 0); x1 = min(int(np.ceil(x.max())), w - 1)
        y0 = max(int(np.floor(y.min())), 0); y1 = min(int(np.ceil(y.max())), h - 1)
        if x1 < x0 or y1 < y0:
            continue
        d = (y[1] - y[2]) * (x[0] - x[2]) + (x[2] - x[1]) * (y[0] - y[2])
        if abs(d) < 1e-9:
            continue
        xs, ys = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        l0 = ((y[1] - y[2]) * (xs - x[2]) + (x[2] - x[1]) * (ys - y[2])) / d
        l1 = ((y[2] - y[0]) * (xs - x[2]) + (x[0] - x[2]) * (ys - y[2])) / d
        l2 = 1 - l0 - l1
        dentro = (l0 >= -0.05) & (l1 >= -0.05) & (l2 >= -0.05)
        if not dentro.any():
            continue
        zz = l0 * z[0] + l1 * z[1] + l2 * z[2]
        bloco = zb[y0:y1 + 1, x0:x1 + 1]
        np.maximum(bloco, np.where(dentro, zz, -np.inf), out=bloco)
    return zb, escala


def amostrar(arr, m, x, y):
    """Amostragem bilinear; devolve cor e validade (dentro da silhueta)."""
    h, w = m.shape
    xi = np.clip(x, 0, w - 1.001); yi = np.clip(y, 0, h - 1.001)
    x0 = np.floor(xi).astype(int); y0 = np.floor(yi).astype(int)
    fx = (xi - x0)[:, None]; fy = (yi - y0)[:, None]
    c = (arr[y0, x0] * (1 - fx) * (1 - fy) + arr[y0, x0 + 1] * fx * (1 - fy)
         + arr[y0 + 1, x0] * (1 - fx) * fy + arr[y0 + 1, x0 + 1] * fx * fy)
    ok = m[y0, x0] & m[y0, x0 + 1] & m[y0 + 1, x0] & m[y0 + 1, x0 + 1]
    ok &= (x >= 0) & (x < w - 1) & (y >= 0) & (y < h - 1)
    return c, ok


# --- rasteriza as faces no espaço UV: posição 3D e normal de cada texel ---
puv = np.stack([UV[:, 0] * TW, (1 - UV[:, 1]) * TH], axis=1)
pos = np.zeros((TH, TW, 3), np.float32)
nor = np.zeros((TH, TW, 3), np.float32)
cob = np.zeros((TH, TW), bool)
for f in F:
    p = puv[f]
    x0, y0 = np.floor(p.min(0)).astype(int); x1, y1 = np.ceil(p.max(0)).astype(int)
    x0 = max(x0, 0); y0 = max(y0, 0); x1 = min(x1, TW - 1); y1 = min(y1, TH - 1)
    if x1 < x0 or y1 < y0:
        continue
    xs, ys = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
    d = (p[1, 1] - p[2, 1]) * (p[0, 0] - p[2, 0]) + (p[2, 0] - p[1, 0]) * (p[0, 1] - p[2, 1])
    if abs(d) < 1e-12:
        continue
    l0 = ((p[1, 1] - p[2, 1]) * (xs - p[2, 0]) + (p[2, 0] - p[1, 0]) * (ys - p[2, 1])) / d
    l1 = ((p[2, 1] - p[0, 1]) * (xs - p[2, 0]) + (p[0, 0] - p[2, 0]) * (ys - p[2, 1])) / d
    l2 = 1 - l0 - l1
    dentro = (l0 >= -0.02) & (l1 >= -0.02) & (l2 >= -0.02)
    if not dentro.any():
        continue
    L = np.stack([l0, l1, l2], -1)[dentro]
    yy = (ys[dentro] - 0.5).astype(int); xx = (xs[dentro] - 0.5).astype(int)
    pos[yy, xx] = L @ V[f]
    nn = L @ N[f]
    nor[yy, xx] = nn / (np.linalg.norm(nn, axis=1, keepdims=True) + 1e-9)
    cob[yy, xx] = True

ty, tx = np.nonzero(cob)
P = pos[ty, tx].astype(np.float64); Nn = nor[ty, tx].astype(np.float64)
cor = tex[ty, tx].copy()
peso_total = np.zeros(len(P))


def suave(x, a0, a1):
    t = np.clip((x - a0) / (a1 - a0), 0, 1)
    return t * t * (3 - 2 * t)


def lum(c):
    return c[:, 0] * 0.299 + c[:, 1] * 0.587 + c[:, 2] * 0.114


def projetar(img_path, eixo_h, sinal_h, eixo_p, sinal_p, normal_peso, regioes, espelhar=False, nome=""):
    """Projeta a imagem nos texels. eixo_h/sinal_h: eixo do modelo que vai para a direita da imagem;
    eixo_p/sinal_p: eixo que aponta para a câmera. Cada região ganha um encaixe fino próprio
    (deslocamento e escala) escolhido por busca, comparando o desenho com a textura atual."""
    img = Image.open(img_path).convert("RGB")
    if espelhar:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    arr, m, (bx0, bx1, by0, by1) = mascara(img)
    hmin = (V[:, eixo_h] * sinal_h).min(); hmax = (V[:, eixo_h] * sinal_h).max()
    esc = (by1 - by0) / alt
    cx_img = (bx0 + bx1) / 2; cx_mod = (hmin + hmax) / 2
    para_img = lambda Q: (cx_img + (Q[:, eixo_h] * sinal_h - cx_mod) * esc, by1 - (Q[:, 1] - ymin) * esc)
    x, y = para_img(P)
    vx, vy = para_img(V)
    zb, e = zbuffer(vx, vy, V[:, eixo_p] * sinal_p, m.shape)
    xi = np.clip((x * e).astype(int), 0, zb.shape[1] - 1); yi = np.clip((y * e).astype(int), 0, zb.shape[0] - 1)
    visivel = (P[:, eixo_p] * sinal_p) >= zb[yi, xi] - 0.012 * alt
    l_tex = lum(cor)

    c_tot = np.zeros((len(P), 3)); w_tot = np.zeros(len(P))
    for rnome, reg in regioes:
        sel = (reg > 0.5) & (normal_peso > 0.8) & visivel
        idx = np.nonzero(sel)[0]
        if len(idx) > 60000:
            idx = idx[:: len(idx) // 60000 + 1]
        cxr, cyr = x[idx].mean(), y[idx].mean()
        alvo = l_tex[idx] - l_tex[idx].mean()

        def custo(dx, dy, sc):
            xx = cxr + (x[idx] - cxr) * sc + dx; yy = cyr + (y[idx] - cyr) * sc + dy
            cc, ok = amostrar(arr, m, xx, yy)
            if ok.mean() < 0.7:
                return 1e9
            li = lum(cc); li = li - li[ok].mean()
            return np.abs(li - alvo)[ok].mean()

        melhor = (custo(0, 0, 1.0), 0.0, 0.0, 1.0)
        for passo, raio, escalas in [(4, 40, [0.90, 0.92, 0.94, 0.96, 0.98, 1.0, 1.02]), (1, 4, None)]:
            _, bdx, bdy, bsc = melhor
            escs = escalas or [bsc - 0.01, bsc, bsc + 0.01]
            for sc in escs:
                for dx in np.arange(bdx - raio, bdx + raio + 0.1, passo):
                    for dy in np.arange(bdy - raio, bdy + raio + 0.1, passo):
                        cst = custo(dx, dy, sc)
                        if cst < melhor[0]:
                            melhor = (cst, dx, dy, sc)
        cst, dx, dy, sc = melhor
        print(f"  encaixe {nome}/{rnome}: dx={dx:+.0f}px dy={dy:+.0f}px escala={sc:.3f} (erro {custo(0,0,1.0):.1f} -> {cst:.1f})")
        xx = cxr + (x - cxr) * sc + dx; yy = cyr + (y - cyr) * sc + dy
        cc, ok = amostrar(arr, m, xx, yy)
        wr = normal_peso * ok * visivel * reg
        c_tot += cc * wr[:, None]; w_tot += wr
    c_tot /= np.maximum(w_tot, 1e-6)[:, None]
    return c_tot, np.clip(w_tot, 0, 1)


# regiões
cabeca = suave(P[:, 1], ymin + 0.64 * alt, ymin + 0.68 * alt)
cx = (V[:, 0].max() + V[:, 0].min()) / 2
fora_bracos = suave(-np.abs(P[:, 0] - cx), -0.125 * alt, -0.105 * alt)   # tronco e pernas: |x| < ~0,11 da altura
sem_sapato = suave(P[:, 1], ymin + 0.10 * alt, ymin + 0.13 * alt)
# vista de lado só na metade de trás da cabeça (o rosto fica com a frente; senão o branco do olho vai para a bochecha)
vh = V[V[:, 1] > ymin + 0.66 * alt]
zc = (vh[:, 2].max() + vh[:, 2].min()) / 2
nuca = cabeca * suave(-(P[:, 2] - zc), -0.03 * alt, 0.0)
corpo = fora_bracos * sem_sapato * (1 - cabeca)

# frente: câmera em +Z olhando -Z; direita da imagem = +X
w_frente_n = np.where(cabeca > 0.5, suave(Nn[:, 2], 0.30, 0.60), suave(Nn[:, 2], 0.45, 0.80))
c_f, w_f = projetar(a.frente, 0, +1, 2, +1, w_frente_n, [("cabeca", cabeca), ("corpo", corpo)], nome="frente")

# lado: a vista do turnaround mostra o rosto à esquerda => câmera em +X; direita da imagem = -Z
w_lado_n = suave(Nn[:, 0], 0.35, 0.75)
c_l, w_l = projetar(a.lado, 2, -1, 0, +1, w_lado_n, [("nuca", nuca)], nome="lado+X")
# outro lado (-X): mesma vista espelhada; direita da imagem espelhada = +Z
w_lado2_n = suave(-Nn[:, 0], 0.35, 0.75)
c_l2, w_l2 = projetar(a.lado, 2, +1, 0, -1, w_lado2_n, [("nuca", nuca)], espelhar=True, nome="lado-X")

w_l = w_l * (1 - w_f); w_l2 = w_l2 * (1 - w_f)
soma = w_f + w_l + w_l2
novo = (c_f * w_f[:, None] + c_l * w_l[:, None] + c_l2 * w_l2[:, None]) / np.maximum(soma, 1e-6)[:, None]
k = np.clip(soma, 0, 1)[:, None]
cor = cor * (1 - k) + novo * k

saida_tex = tex.copy()
saida_tex[ty, tx] = cor
img_out = Image.fromarray(np.clip(saida_tex, 0, 255).astype(np.uint8))
if a.debug:
    dbg = np.zeros((TH, TW, 3), np.uint8)
    dbg[ty, tx, 0] = (np.clip(w_f, 0, 1) * 255).astype(np.uint8)
    dbg[ty, tx, 1] = (np.clip(w_l + w_l2, 0, 1) * 255).astype(np.uint8)
    Image.fromarray(dbg).resize((1024, 1024)).save(a.debug)

mat.baseColorTexture = img_out
malha.visual.material = mat
cena.export(a.saida)
print("texels cobertos:", len(P), "| frente:", int((w_f > 0.5).sum()), "| lados:", int(((w_l + w_l2) > 0.5).sum()))
print("salvo:", a.saida)
