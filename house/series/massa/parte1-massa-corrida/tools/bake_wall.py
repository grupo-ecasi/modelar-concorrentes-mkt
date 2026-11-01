"""Assa as imagens da parede (assets/wall/*.jpg) a partir de um mapa de relevo com semente fixa.

A ideia física do vídeo: com luz de frente, a variação de brilho de uma parede depende do
quadrado da inclinação (some). Com luz rasante, ela cresce com inclinação × cotangente do ângulo
da luz (cerca de 8× a 7°). Por isso a mesma parede "lisa" mostra ondas e emendas quando o sol
bate de lado.

Saídas (1080×1920):
  ruim-frente.jpg   massa mal feita, luz de frente (parece lisa)
  ruim-lado.jpg     massa mal feita, luz rasante vinda da esquerda (defeitos aparecem)
  boa-frente.jpg    massa bem feita, luz de frente
  boa-lado.jpg      massa bem feita, luz rasante (continua lisa)

Uso: python -I tools/bake_wall.py
"""
import os
import subprocess

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "assets", "wall")
W, H = 1080, 1920
rng = np.random.default_rng(20261031)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float64)


def blur(a, sigma):
    """Desfoque gaussiano via FFT (sem scipy)."""
    fy = np.fft.fftfreq(a.shape[0])[:, None]
    fx = np.fft.fftfreq(a.shape[1])[None, :]
    k = np.exp(-2 * (np.pi * sigma) ** 2 * (fx**2 + fy**2))
    return np.real(np.fft.ifft2(np.fft.fft2(a) * k))


def sig(x):
    return 0.5 * (1 + np.tanh(x))


def grain(amp, sigma):
    g = blur(rng.standard_normal((H, W)), sigma)
    return g / g.std() * amp


def waves(n, lam, amp):
    h = np.zeros((H, W))
    for _ in range(n):
        ang = rng.uniform(0, np.pi)
        l = rng.uniform(*lam)
        ph = rng.uniform(0, 2 * np.pi)
        h += rng.uniform(*amp) * np.sin(2 * np.pi * (xx * np.cos(ang) + yy * np.sin(ang)) / l + ph)
    return h


# ---------- massa mal feita ----------
bad = waves(6, (260, 720), (1.2, 2.2))
# "barriga" (ondulação) bem marcada em torno de (720, 640)
bad += 6.0 * np.exp(-(((xx - 720) / 190) ** 2 + ((yy - 640) / 150) ** 2))
bad -= 3.5 * np.exp(-(((xx - 560) / 120) ** 2 + ((yy - 800) / 110) ** 2))

# emenda: faixa vertical com uma camada a mais de massa, borda viva de um lado
seam = sig((xx - 300) / 3.0) * sig((430 - xx) / 14.0)
bad += 1.6 * seam
bad += 0.35 * np.exp(-(((xx - 302) / 3.0) ** 2))  # rebarba na borda da emenda

# marcas de espátula: crescentes (borda viva do passe da desempenadeira) em torno de (560, 1100)
for _ in range(9):
    cx, cy = rng.uniform(380, 760), rng.uniform(960, 1300)
    r = rng.uniform(170, 330)
    band = rng.uniform(70, 140)
    a0 = rng.uniform(-np.pi, np.pi)
    span = rng.uniform(0.7, 1.5)
    d = np.hypot(xx - cx, yy - cy)
    th = np.angle(np.exp(1j * (np.arctan2(yy - cy, xx - cx) - a0)))
    angm = sig((th + span / 2) / 0.12) * sig((span / 2 - th) / 0.12)
    bad += rng.uniform(0.6, 1.0) * sig((r - d) / 1.8) * sig((d - (r - band)) / 18) * angm
# alguns passes soltos pelo resto da parede
for _ in range(10):
    cx, cy = rng.uniform(0, W), rng.uniform(150, 1750)
    r, band = rng.uniform(150, 380), rng.uniform(60, 120)
    a0, span = rng.uniform(-np.pi, np.pi), rng.uniform(0.5, 1.1)
    d = np.hypot(xx - cx, yy - cy)
    th = np.angle(np.exp(1j * (np.arctan2(yy - cy, xx - cx) - a0)))
    angm = sig((th + span / 2) / 0.12) * sig((span / 2 - th) / 0.12)
    bad += rng.uniform(0.3, 0.6) * sig((r - d) / 2.0) * sig((d - (r - band)) / 18) * angm

# riscos de lixa grossa
for _ in range(80):
    x0, y0 = rng.uniform(0, W), rng.uniform(0, H)
    ang = rng.uniform(0, np.pi)
    ln = rng.uniform(30, 110)
    x1, y1 = x0 + ln * np.cos(ang), y0 + ln * np.sin(ang)
    xa, xb = int(max(0, min(x0, x1) - 4)), int(min(W, max(x0, x1) + 5))
    ya, yb = int(max(0, min(y0, y1) - 4)), int(min(H, max(y0, y1) + 5))
    if xb <= xa or yb <= ya:
        continue
    px, py = xx[ya:yb, xa:xb], yy[ya:yb, xa:xb]
    t = np.clip(((px - x0) * (x1 - x0) + (py - y0) * (y1 - y0)) / ln**2, 0, 1)
    dd = np.hypot(px - (x0 + t * (x1 - x0)), py - (y0 + t * (y1 - y0)))
    bad[ya:yb, xa:xb] -= 0.16 * np.exp(-((dd / 1.1) ** 2))

# poros / bolhas
for _ in range(220):
    cx, cy, s = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(1.8, 4.5)
    xa, xb, ya, yb = int(max(0, cx - 14)), int(min(W, cx + 15)), int(max(0, cy - 14)), int(min(H, cy + 15))
    bad[ya:yb, xa:xb] -= 0.9 * np.exp(-((xx[ya:yb, xa:xb] - cx) ** 2 + (yy[ya:yb, xa:xb] - cy) ** 2) / (2 * s * s))

bad += grain(0.035, 1.4) + grain(0.09, 6)

# ---------- massa bem feita ----------
good = waves(4, (500, 900), (0.08, 0.15)) + grain(0.003, 1.4) + grain(0.006, 6)


def shade(h, light, front):
    hy, hx = np.gradient(h)
    n = np.stack([-hx, -hy, np.ones_like(h)])
    n /= np.linalg.norm(n, axis=0)
    L = np.array(light, dtype=np.float64)
    L /= np.linalg.norm(L)
    ratio = np.tensordot(L, n, axes=1) / L[2]
    albedo = np.array([242, 238, 231]) / 255.0  # branco gelo, tinta fosca
    vgrad = 1.0 - 0.07 * (yy / H)  # um pouco mais escuro perto do chão
    vign = 1.0 - 0.10 * (((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H * 0.45) / (H * 0.8)) ** 2)
    if front:
        lum = (0.88 * np.clip(ratio, 0, 1.5) * vgrad * vign)[..., None]
        rgb = lum * albedo
    else:
        r = np.clip(ratio, 0, 2.8)
        sun = np.array([1.0, 0.9, 0.74])
        amb = np.array([0.82, 0.86, 0.95])
        rgb = albedo * (0.42 * amb + 0.68 * r[..., None] * sun) * (vgrad * vign)[..., None]
        rgb = rgb / (1 + 0.18 * rgb)  # compressão suave dos realces
    return np.clip(rgb * 255, 0, 255).astype(np.uint8)


def save(img, name):
    path = os.path.join(OUT, name)
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-i", "-",
         "-q:v", "2", path],
        input=img.tobytes(), check=True,
    )
    print(name)


os.makedirs(OUT, exist_ok=True)
FRONT = (0.0, -0.05, 1.0)
e = np.radians(7)
SIDE = (-np.cos(e), -0.10, np.sin(e))
bad_side = shade(bad, SIDE, False)
good_side = shade(good, SIDE, False)
# "Mesma luz": a parede boa fica no tom dos trechos claros da ruim (é o que o olho lê como a cor da luz)
k = np.percentile(bad_side.reshape(-1, 3), 80, axis=0) / np.median(good_side.reshape(-1, 3), axis=0)
good_side = np.clip(good_side * k, 0, 255).astype(np.uint8)
save(shade(bad, FRONT, True), "ruim-frente.jpg")
save(bad_side, "ruim-lado.jpg")
save(shade(good, FRONT, True), "boa-frente.jpg")
save(good_side, "boa-lado.jpg")
