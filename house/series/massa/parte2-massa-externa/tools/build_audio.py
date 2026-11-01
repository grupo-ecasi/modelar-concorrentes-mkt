"""Monta o áudio de fundo do Reel (assets/audio-mix.wav): chuva e trovão sintetizados (semente fixa)
e efeitos sonoros nas entradas. A narração fica em outra faixa (assets/narracao-voz.wav). Sem música.

Uso: python -I tools/build_audio.py
"""
import os
import subprocess

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
END = 21.5
rng = np.random.default_rng(31102026)


def decode(path):
    cmd = ["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, dtype=np.float32).astype(np.float64)


def sfx(name):
    """Corta o silêncio inicial e nivela pela energia dos primeiros 250 ms (RMS em -18 dBFS)."""
    a = decode(os.path.join(BASE, "assets", "sfx", name + ".mp3"))
    pk = np.abs(a).max() or 1.0
    a = a[max(0, int(np.argmax(np.abs(a) > pk * 0.05)) - 48) :]
    rms = np.sqrt(np.mean(a[: int(0.25 * SR)] ** 2)) or 1e-6
    a = a * (10 ** (-18 / 20) / rms)
    return a * min(1.0, 10 ** (-3 / 20) / (np.abs(a).max() or 1.0))


def band(x, lo, hi):
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X = np.fft.rfft(x)
    X *= (f >= lo) & (f <= hi)
    return np.fft.irfft(X, len(x))


def env(n, segs):
    """Envelope por trechos (início, fim, fade) em segundos."""
    t = np.arange(n) / SR
    e = np.zeros(n)
    for a, b, fd in segs:
        e = np.maximum(e, np.clip((t - a) / fd, 0, 1) * np.clip((b - t) / fd, 0, 1))
    return e


def place(mix, sig, t, db):
    i = int(t * SR)
    n = min(len(sig), len(mix) - i)
    mix[i : i + n] += sig[:n] * 10 ** (db / 20)


N = int(END * SR)
mix = np.zeros(N)

# Chuva: ruído em faixa + pingos curtos; liga junto com a chuva da imagem (compositions/muro.html)
rain = band(rng.standard_normal(N), 700, 7000)
rain /= np.abs(rain).max()
drops = np.zeros(N)
for i in rng.integers(0, N - 400, size=2600):
    drops[i : i + 240] += rng.uniform(0.2, 1.0) * np.exp(-np.arange(240) / 30) * rng.choice([-1, 1])
drops = band(drops, 1500, 9000)
drops /= np.abs(drops).max()
rain = (0.7 * rain + 0.5 * drops) * env(N, [(6.1, 9.8, 0.35), (14.45, 17.6, 0.35)])
place(mix, rain, 0, -16)

# Trovão grave quando começa a chover
th = band(rng.standard_normal(int(2.8 * SR)), 25, 160)
t = np.arange(len(th)) / SR
th = th / np.abs(th).max() * np.clip(t / 0.08, 0, 1) * np.exp(-t / 0.9) * (1 + 0.6 * np.sin(2 * np.pi * 1.7 * t))
place(mix, th, 5.95, -4)

# (tempo em s, som, ganho em dB) — casado com as deixas CUE das composições
EVENTS = [
    (0.0, "impact-bass-1", -3),  # gancho na tela
    (2.4, "impact-bass-2", -3),  # "dinheiro jogado fora"
    (2.45, "whoosh", -5),  # notas voando
    (4.15, "whoosh-short", -7),  # balde vai ao centro
    (5.0, "impact-bass-1", -4),  # carimbo "só área interna"
    (6.2, "pop", -7),  # selo ❌
    (6.96, "pop", -5),  # puxa água
    (7.94, "pop", -5),  # estufa
    (8.72, "pop", -5),  # descasca
    (8.75, "impact-bass-2", -6),
    (9.75, "whoosh", -3),  # desempenadeira
    (10.25, "whoosh-short", -8),
    (10.32, "sparkle", -6),  # selo ✅
    (10.96, "click", -5),  # etapas
    (11.84, "click", -5),
    (13.04, "click", -5),
    (14.48, "pop", -7),  # "mesma chuva"
    (15.68, "impact-bass-2", -6),  # "parede inteira"
    (15.7, "sparkle", -8),
    (16.9, "whoosh", -6),  # encerramento
    (17.1, "pop", -5),
    (17.7, "pop", -7),
    (18.96, "click", -4),  # botão do WhatsApp
    (19.9, "chime", -8),
]
cache = {}
for t0, name, db in EVENTS:
    cache.setdefault(name, sfx(name))
    place(mix, cache[name], t0, db)

n = int(0.3 * SR)
mix[-n:] *= np.linspace(1, 0, n)

tmp = os.path.join(BASE, "tools", ".mix.f32")
mix.astype(np.float32).tofile(tmp)
out = os.path.join(BASE, "assets", "audio-mix.wav")
subprocess.run(
    [
        "ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", tmp,
        "-af", "highpass=f=30,loudnorm=I=-15:TP=-1.5:LRA=11,aformat=sample_rates=48000:channel_layouts=stereo",
        "-c:a", "pcm_s16le", out,
    ],
    check=True,
)
os.remove(tmp)
print(f"chuva + trovão + {len(EVENTS)} efeitos · {out}")
