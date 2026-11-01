"""Monta o áudio do Reel (assets/audio-mix.wav): o som do pincel e do verniz que o Veo gerou nos próprios
clipes, realçado, mais efeitos sonoros nas entradas de cada elemento. Sem música: a ideia é deixar o
Instagram livre para um áudio em alta, se a House quiser.

Uso: python -I tools/build_audio.py
"""
import os
import subprocess

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
END = 20.4


def decode(path, start=None, dur=None):
    cmd = ["ffmpeg", "-v", "error"]
    if start is not None:
        cmd += ["-ss", str(start), "-t", str(dur)]
    cmd += ["-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"]
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

# Som dos clipes (o pincel e o verniz vêm muito baixos do Veo; sobem com o mesmo trecho usado no vídeo)
for clip, t0, src, dur, gain in [("02-pintar", 2.4, 3.6, 3.4, 26), ("03-verniz", 5.8, 2.6, 3.2, 20)]:
    a = decode(os.path.join(BASE, "assets", "clips", clip + ".mp4"), src, dur)
    fade = np.minimum(1, np.minimum(np.arange(len(a)), np.arange(len(a))[::-1]) / (0.08 * SR))
    place(mix, a * fade, t0, gain)

# (tempo em s, som, ganho em dB)
EVENTS = [
    (0.0, "impact-bass-1", -2),
    (0.15, "whoosh", -6),
    (2.4, "whoosh-short", -4),
    (2.5, "pop", -6),
    (5.8, "whoosh-short", -4),
    (5.9, "pop", -6),
    (9.0, "whoosh-short", -4),
    (9.1, "pop", -6),
    (9.4, "whoosh-cinematic", -6),
    (10.5, "impact-bass-2", -1),
    (10.65, "sparkle", -6),
    (12.8, "pop", -7),
    (16.5, "whoosh", -6),
    (16.85, "pop", -4),
    (17.5, "pop", -6),
    (17.85, "click", -4),
    (18.6, "click", -6),
    (18.65, "chime", -8),
]
cache = {}
for t, name, db in EVENTS:
    cache.setdefault(name, sfx(name))
    place(mix, cache[name], t, db)

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
print(f"{len(EVENTS)} efeitos + som dos clipes · {out}")
