"""Monta o áudio do Reel (assets/audio-mix.wav): efeitos sonoros nas entradas de cada elemento.
Sem música: o Instagram fica livre para um áudio em alta, se a House quiser.

Uso: python -I tools/build_audio.py
"""
import os
import subprocess

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
END = 21.0


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


def place(mix, sig, t, db):
    i = int(t * SR)
    n = min(len(sig), len(mix) - i)
    mix[i : i + n] += sig[:n] * 10 ** (db / 20)


mix = np.zeros(int(END * SR))

# (tempo em s, som, ganho em dB) — casado com os tempos de index.html e compositions/*.html
EVENTS = [
    (0.0, "impact-bass-1", -3),  # gancho na tela
    (2.2, "impact-bass-2", -2),  # "…até o sol bater de lado"
    (3.6, "whoosh-cinematic", -5),  # a luz começa a varrer
    (4.1, "pop", -5),  # emenda
    (4.96, "pop", -5),  # ondulação
    (5.45, "riser", -12),  # o sol entra na parede toda
    (5.92, "pop", -5),  # marca de espátula
    (7.35, "impact-bass-1", -5),  # "é massa mal feita"
    (7.37, "pop", -7),
    (9.0, "whoosh", -3),  # desempenadeira
    (9.5, "whoosh-short", -8),
    (9.9, "sparkle", -5),  # parede lisa + selo "massa bem feita"
    (9.92, "pop", -6),
    (10.08, "click", -5),  # etapas
    (11.3, "click", -5),
    (12.16, "click", -5),
    (13.81, "pop", -7),  # "mesma luz"
    (14.85, "impact-bass-2", -6),  # "zero onda"
    (15.9, "whoosh", -6),  # encerramento
    (16.1, "pop", -5),
    (16.7, "pop", -7),
    (18.33, "click", -4),  # botão do WhatsApp
    (19.3, "chime", -8),
]
cache = {}
for t, name, db in EVENTS:
    cache.setdefault(name, sfx(name))
    place(mix, cache[name], t, db)

# fade curto no fim para não cortar seco
n = int(0.25 * SR)
mix[-n:] *= np.linspace(1, 0, n)

tmp = os.path.join(BASE, "tools", ".mix.f32")
mix.astype(np.float32).tofile(tmp)
out = os.path.join(BASE, "assets", "audio-mix.wav")
subprocess.run(
    [
        "ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", tmp,
        "-af", "highpass=f=70,loudnorm=I=-15:TP=-1.5:LRA=11,aformat=sample_rates=48000:channel_layouts=stereo",
        "-c:a", "pcm_s16le", out,
    ],
    check=True,
)
os.remove(tmp)
print(f"{len(EVENTS)} efeitos · {out}")
