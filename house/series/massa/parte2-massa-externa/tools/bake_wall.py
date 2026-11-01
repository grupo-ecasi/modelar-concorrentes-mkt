"""Assa as imagens do muro externo (assets/wall/*) a partir de UM mapa de molhamento com semente fixa.

Cada estágio de estrago contém o anterior (os limiares só descem), então as fusões entre eles só
acrescentam dano, sem piscar. O estrago vem da chuva batendo na face da parede, de cima para baixo
(escorrimento), e não de umidade subindo do chão.

Saídas (1080×1920):
  ruim-0-nova.jpg       muro recém-pintado sobre massa corrida PVA
  ruim-1-agua.jpg       "puxa água": manchas e escorridos molhados
  ruim-2-estufa.jpg     "estufa": bolhas na película de tinta
  ruim-3-descasca.jpg   "descasca": tinta solta, massa esfarelando, trincas
  boa-seca.jpg          muro refeito (selador + massa acrílica + tinta para fachada)
  boa-chuva.jpg         o mesmo muro molhado: escurece, a água escorre, nada estraga
  chuva.png             gotas de chuva (transparente), para repetir em tile

Uso: python -I tools/bake_wall.py
"""
import os
import subprocess

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "assets", "wall")
W, H = 1080, 1920
TOP, BOT = 380, 1740  # faixa do muro (acima: céu e pingadeira; abaixo: chão)
rng = np.random.default_rng(20261031 + 2)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float64)


def blur(a, sigma):
    fy = np.fft.fftfreq(a.shape[0])[:, None]
    fx = np.fft.fftfreq(a.shape[1])[None, :]
    return np.real(np.fft.ifft2(np.fft.fft2(a) * np.exp(-2 * (np.pi * sigma) ** 2 * (fx**2 + fy**2))))


def sm(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def grain(amp, sigma):
    g = blur(rng.standard_normal((H, W)), sigma)
    return g / g.std() * amp


wall = ((yy >= TOP) & (yy < BOT)).astype(np.float64)

# ---------- mapa de molhamento (0 = seco, 1 = molha primeiro) ----------
streaks = np.zeros((H, W))
for _ in range(46):
    x0 = rng.uniform(20, W - 20)
    w = rng.uniform(6, 34)
    ln = rng.uniform(220, 1250)
    amp = rng.uniform(0.5, 1.0)
    lam, wob = rng.uniform(120, 300), rng.uniform(2, 9)
    xc = x0 + wob * np.sin((yy - TOP) / lam)
    along = sm(TOP + ln, TOP + ln * 0.55, yy) * (yy >= TOP)
    streaks += amp * np.exp(-(((xx - xc) / w) ** 2)) * along
streaks = np.clip(streaks, 0, 1.3) / 1.3
blotch = blur(rng.standard_normal((H, W)), 55)
blotch = (blotch - blotch.min()) / (blotch.max() - blotch.min())
topband = np.exp(-np.clip(yy - TOP, 0, None) / 160)
wet = np.clip(0.62 * streaks + 0.42 * blotch + 0.35 * topband - 0.08, 0, 1) * wall

# ---------- relevo base (reboco pintado) ----------
h_base = grain(0.2, 1.2) + grain(0.4, 4) + grain(1.5, 30)

# ---------- bolhas: onde molha mais ----------
bubbles = []
for _ in range(16):  # aglomerado principal em torno de (720, 800)
    bubbles.append((rng.normal(720, 95), rng.normal(800, 85), rng.uniform(18, 56)))
cand = np.argwhere(wet[TOP + 40 : BOT - 120 : 7, 30 : W - 30 : 7] > 0.62)
for k in rng.choice(len(cand), size=min(14, len(cand)), replace=False):
    y, x = cand[k] * 7 + [TOP + 40, 30]
    bubbles.append((x, y, rng.uniform(8, 24)))
h_bub = np.zeros((H, W))
for cx, cy, r in bubbles:
    ya, yb, xa, xb = int(max(0, cy - r - 3)), int(min(H, cy + r + 4)), int(max(0, cx - r - 3)), int(min(W, cx + r + 4))
    d = np.hypot(xx[ya:yb, xa:xb] - cx, yy[ya:yb, xa:xb] - cy) / r
    h_bub[ya:yb, xa:xb] = np.maximum(h_bub[ya:yb, xa:xb], 0.38 * r * np.sqrt(np.clip(1 - d * d, 0, 1)))

# ---------- descascado: placa principal em torno de (360, 1080) + menores ----------
pn = blur(rng.standard_normal((H, W)), 18)
pn /= pn.std()
peel = np.zeros((H, W))
for cx, cy, rx, ry in [(360, 1080, 190, 140), (800, 1260, 80, 60), (560, 540, 70, 90), (210, 690, 60, 75), (870, 1530, 90, 55), (720, 840, 70, 55)]:
    q = np.hypot((xx - cx) / rx, (yy - cy) / ry) + 0.22 * pn
    peel = np.maximum(peel, sm(1.04, 0.96, q))
peel *= wall
deep = sm(0.55, 0.9, blur(rng.standard_normal((H, W)), 6) / 1.0 + 0.0) * sm(0.3, 0.95, blur(peel, 10))

cracks = np.zeros((H, W))
for cx, cy, n in [(360, 1080, 14), (800, 1260, 5), (560, 540, 5), (720, 840, 6)]:
    for _ in range(n):
        x, y = cx + rng.normal(0, 70), cy + rng.normal(0, 55)
        ang = rng.uniform(0, 2 * np.pi)
        for _ in range(int(rng.uniform(18, 50))):
            ang += rng.normal(0, 0.45)
            x2, y2 = x + 6 * np.cos(ang), y + 6 * np.sin(ang)
            xa, xb, ya, yb = int(min(x, x2) - 3), int(max(x, x2) + 4), int(min(y, y2) - 3), int(max(y, y2) + 4)
            if xa < 0 or ya < TOP or xb > W or yb > BOT:
                break
            px, py = xx[ya:yb, xa:xb], yy[ya:yb, xa:xb]
            t = np.clip(((px - x) * (x2 - x) + (py - y) * (y2 - y)) / 36, 0, 1)
            dd = np.hypot(px - (x + t * (x2 - x)), py - (y + t * (y2 - y)))
            cracks[ya:yb, xa:xb] = np.maximum(cracks[ya:yb, xa:xb], np.exp(-((dd / 0.9) ** 2)))
            x, y = x2, y2

# ---------- cenário fixo: céu, pingadeira do muro e chão ----------
PAINT = np.array([185, 198, 211]) / 255.0  # cinza-azulado claro (combina com a marca)
MASSA = np.array([247, 245, 239]) / 255.0
REBOCO = np.array([150, 144, 135]) / 255.0


def scenery(rgb):
    t = np.clip(yy / 330, 0, 1)[..., None]
    sky = (1 - t) * np.array([126, 168, 214]) / 255 + t * np.array([206, 222, 238]) / 255
    rgb = np.where((yy < 330)[..., None], sky, rgb)
    cap = (yy >= 330) & (yy < TOP)
    capc = np.array([214, 210, 202]) / 255 * (1 - 0.18 * ((yy - 330) / 50))[..., None]
    capc = capc * (1 + grain(0.03, 1.5))[..., None]
    rgb = np.where(cap[..., None], capc, rgb)
    shadow = 1 - 0.35 * np.exp(-np.clip(yy - TOP, 0, None) / 14) * wall  # sombra da pingadeira
    rgb = rgb * shadow[..., None]
    gr = yy >= BOT
    grass = np.array([92, 128, 70]) / 255 * (1 + grain(0.12, 2.0) + 0.15 * np.sin(xx / 7))[..., None]
    grass = np.where((yy < BOT + 26)[..., None], np.array([120, 116, 108]) / 255, grass)  # rodapé de cimento
    return np.where(gr[..., None], grass, rgb)


def shade(h):
    hy, hx = np.gradient(h)
    n = np.stack([-hx, -hy, np.ones_like(h)])
    n /= np.linalg.norm(n, axis=0)
    L = np.array([-0.45, -0.55, 0.70])
    L /= np.linalg.norm(L)
    return np.clip(np.tensordot(L, n, axes=1) / L[2], 0.2, 1.6)


def wall_img(W_amt, with_bub, with_peel, beads=False):
    h = h_base + (h_bub * (1 - peel if with_peel else 1) if with_bub else 0)
    if with_peel:
        h = h - 1.5 * blur(peel, 2) + grain(0.9, 1.0) * peel
    lum = shade(h)
    rgb = PAINT * (0.86 * lum)[..., None]
    if with_bub:  # película esticada: um pouco mais clara
        rgb *= (1 + 0.05 * (h_bub > 0.5))[..., None]
    wetc = np.array([0.66, 0.69, 0.75])
    tide = W_amt * (1 - W_amt) * 4
    rgb = rgb * (1 - W_amt[..., None] * (1 - wetc)) * (1 - 0.10 * tide)[..., None]
    if with_peel:
        m = blur(peel, 1.2)
        exp_c = MASSA * (0.9 + grain(0.08, 0.9))[..., None]
        exp_c = exp_c * (1 - deep[..., None]) + REBOCO * deep[..., None]
        exp_c *= (0.97 * lum ** 0.3)[..., None]
        rgb = rgb * (1 - m[..., None]) + exp_c * m[..., None]
        inner = np.clip(m - blur(m, 5), 0, 1)  # sombra sob a borda da tinta solta
        outer = np.clip(blur(m, 2.5) - m, 0, 1)  # borda da película levantada
        rgb = rgb * (1 - 1.8 * inner)[..., None] + 1.3 * outer[..., None] * np.array([0.95, 0.96, 0.98])
        rgb *= (1 - 0.55 * cracks * (1 - m))[..., None]
    if beads:
        b = np.zeros((H, W))
        for _ in range(700):
            cx, cy, r = rng.uniform(0, W), rng.uniform(TOP + 10, BOT - 10), rng.uniform(1.8, 4.5)
            ya, yb, xa, xb = int(max(0, cy - 8)), int(min(H, cy + 9)), int(max(0, cx - 8)), int(min(W, cx + 9))
            d2 = (xx[ya:yb, xa:xb] - cx + r * 0.35) ** 2 + (yy[ya:yb, xa:xb] - cy + r * 0.35) ** 2
            b[ya:yb, xa:xb] = np.maximum(b[ya:yb, xa:xb], np.exp(-d2 / (2 * (r * 0.35) ** 2)))
        rgb = rgb + 0.55 * b[..., None]
    rgb = rgb * wall[..., None] + (1 - wall[..., None]) * 0
    return scenery(rgb)


def save(img, name, alpha=None):
    path = os.path.join(OUT, name)
    if alpha is None:
        data, fmt, extra = (np.clip(img, 0, 1) * 255).astype(np.uint8), "rgb24", ["-q:v", "2"]
    else:
        data = np.dstack([(np.clip(img, 0, 1) * 255), (np.clip(alpha, 0, 1) * 255)]).astype(np.uint8)
        fmt, extra = "rgba", []
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", fmt, "-s", f"{W}x{H}", "-i", "-", *extra, path],
                   input=data.tobytes(), check=True)
    print(name)


os.makedirs(OUT, exist_ok=True)
zero = np.zeros((H, W))
save(wall_img(zero, False, False), "ruim-0-nova.jpg")
save(wall_img(sm(0.56, 0.70, wet) * wall, False, False), "ruim-1-agua.jpg")
save(wall_img(sm(0.44, 0.58, wet) * wall, True, False), "ruim-2-estufa.jpg")
save(wall_img(sm(0.34, 0.48, wet) * wall, True, True), "ruim-3-descasca.jpg")
save(wall_img(zero, False, False), "boa-seca.jpg")
run = np.zeros((H, W))
for _ in range(60):  # água escorrendo em filetes
    x0, w = rng.uniform(0, W), rng.uniform(2, 7)
    run += np.exp(-(((xx - x0 - 3 * np.sin(yy / rng.uniform(60, 160))) / w) ** 2)) * rng.uniform(0.3, 0.8)
save(wall_img(np.clip(0.42 + 0.1 * blotch + 0.35 * run, 0, 0.9) * wall, False, False, beads=True), "boa-chuva.jpg")

# gotas de chuva: traços finos levemente inclinados
a = np.zeros((H, W))
for _ in range(900):
    x0, y0 = rng.uniform(0, W), rng.uniform(0, H)
    ln, w = rng.uniform(40, 110), rng.uniform(0.8, 1.8)
    ang = np.radians(98)
    x1, y1 = x0 + ln * np.cos(ang), y0 + ln * np.sin(ang)
    xa, xb, ya, yb = int(min(x0, x1) - 3), int(max(x0, x1) + 4), int(min(y0, y1) - 3), int(max(y0, y1) + 4)
    xa, ya, xb, yb = max(xa, 0), max(ya, 0), min(xb, W), min(yb, H)
    if xb <= xa or yb <= ya:
        continue
    px, py = xx[ya:yb, xa:xb], yy[ya:yb, xa:xb]
    t = np.clip(((px - x0) * (x1 - x0) + (py - y0) * (y1 - y0)) / ln**2, 0, 1)
    dd = np.hypot(px - (x0 + t * (x1 - x0)), py - (y0 + t * (y1 - y0)))
    a[ya:yb, xa:xb] = np.maximum(a[ya:yb, xa:xb], rng.uniform(0.35, 0.7) * np.exp(-((dd / w) ** 2)) * (0.4 + 0.6 * t))
save(np.ones((H, W, 3)) * np.array([0.88, 0.93, 1.0]), "chuva.png", alpha=a)
