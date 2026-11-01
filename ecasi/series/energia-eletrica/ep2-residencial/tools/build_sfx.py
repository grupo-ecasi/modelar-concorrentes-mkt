"""Monta a trilha de efeitos sonoros (assets/sfx-track.wav) a partir de tools/cues.json.

Cada efeito está preso à mesma marca de tempo da animação que ele acompanha. Cada som é nivelado pela
energia do seu início (não pelo pico), para um clique e um sino soarem com o mesmo peso. A trilha passa
por um ducking leve com a voz como sidechain e por um limitador. O volume final é conferido com
tools/measure_mix.py: os efeitos ficam bem audíveis, mas sempre abaixo da narração.

Uso: python -I tools/build_sfx.py
"""
import json
import os
import subprocess

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
VOICE = os.path.join(BASE, "assets", "narracao-norm.mp3")
C = json.load(open(os.path.join(BASE, "tools", "cues.json"), encoding="utf-8"))

# Volume geral dos efeitos (dB). É o botão principal: mais perto de 0 = mais alto.
MASTER_DB = 0.0

# Equilíbrio entre os sons (dB), depois do nivelamento pela energia do início
SOUND_GAIN = {
    "pop": -5,
    "whoosh-short": -6,
    "click": -1,
    "click-soft": 4,
    "chime": -1,
    "ping": 2,
    "notification": 0,
    "error": -2,
    "glitch-1": -4,
    "glitch-3": -2,
    "impact-bass-1": 3,
}

# (marca, deslocamento em s, som, ganho extra em dB)
EVENTS = [
    # Gancho
    ("hook", 0.75, "click", 3),
    ("pode", 0.2, "whoosh-short", -4),
    ("ainda", 0.0, "impact-bass-1", 0),
    ("quadro2", 0.15, "whoosh-short", -2),
    ("quadro2", 0.2, "glitch-3", -3),
    ("camadas", 0.0, "pop", -1),
    ("camadas", 0.12, "pop", -1),
    ("camadas", 0.24, "pop", 0),
    # Problema
    ("esquenta", 0.0, "glitch-1", -3),
    ("pvc", -0.2, "pop", -6),
    ("g70", -0.2, "ping", -5),
    ("fuga", 0.1, "glitch-3", 2),
    ("mili", -0.1, "pop", 0),
    ("semTerra", 0.0, "error", -2),
    ("carcaca", 0.0, "glitch-1", -1),
    # Camada 1
    ("c1", 0.0, "whoosh-short", 0),
    ("escolhido", -0.2, "pop", 4),
    ("cabo25", 0.0, "pop", -4),
    ("a24", -0.1, "click-soft", 0),
    ("d20", -0.4, "click", 1),
    ("d20", -0.1, "chime", -1),
    # Camada 2
    ("c2", 0.0, "whoosh-short", -2),
    ("ma30", -0.1, "pop", -3),
    ("banheiro", -0.05, "click-soft", -3),
    ("cozinha", -0.05, "click-soft", -9),
    ("lavanderia", -0.05, "click-soft", -3),
    ("externa", -0.05, "click-soft", -3),
    ("teste", -0.15, "click", 4),
    ("teste", 0.1, "impact-bass-1", -4),
    ("teste", 0.3, "chime", -5),
    # Camada 3
    ("c3", 0.0, "whoosh-short", 0),
    ("fioTerra", -0.2, "pop", 0),
    ("fioTerra", 0.9, "chime", -2),
    ("dps", -0.15, "pop", -3),
    ("dps", 0.0, "glitch-3", -4),
    ("etiqueta", -0.15, "pop", 0),
    ("etiqueta", 0.5, "ping", -1),
    # Mito
    ("mito", 0.0, "notification", -5),
    ("poe", -0.1, "pop", 0),
    ("naoMito", 0.0, "impact-bass-1", -2),
    ("a40", -0.25, "click", 3),
    ("cabo24", -0.1, "click-soft", 0),
    ("dobro", -0.1, "ping", 0),
    ("fusivel", 0.0, "glitch-1", 0),
    ("parede", 0.0, "impact-bass-1", -3),
    # Norma
    ("norma", 0.2, "pop", 3),
    ("nr10", -0.1, "pop", 0),
    ("desenergizar", 0.45, "click", 2),
    ("antesNr", 0.3, "chime", -5),
    ("curso", -0.1, "pop", -9),
    # Chamada final e fecho
    ("cta", 0.0, "whoosh-short", -5),
    ("treinamento", 0.0, "pop", 0),
    ("ecasi", -0.2, "click", 0),
    ("proximo", -0.2, "pop", -3),
    ("loop", 0.1, "whoosh-short", -2),
    ("confira", 0.64, "pop", -2),
    ("confira", 0.8, "pop", -2),
    ("confira", 1.04, "pop", -2),
    ("antes", 0.0, "pop", -5),
]


def decode(path):
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
        capture_output=True,
        check=True,
    ).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)


def load_sound(name):
    """Corta o silêncio inicial e nivela pela energia dos primeiros 250 ms (RMS em -18 dBFS)."""
    a = decode(os.path.join(BASE, "assets", "sfx", name + ".mp3"))
    peak = np.abs(a).max() or 1.0
    first = int(np.argmax(np.abs(a) > peak * 0.05))
    a = a[max(0, first - 48) :]
    head = a[: int(0.25 * SR)]
    rms = np.sqrt(np.mean(head**2)) or 1e-6
    a = a * (10 ** (-18 / 20) / rms)
    # Nenhum som isolado passa de -3 dBFS
    return a * min(1.0, 10 ** (-3 / 20) / (np.abs(a).max() or 1.0))


if __name__ == "__main__":
    total = int((C["end"] + 1.0) * SR)
    mix = np.zeros(total)
    cache = {}
    for cue, off, snd, extra in EVENTS:
        if snd not in cache:
            cache[snd] = load_sound(snd)
        s = cache[snd] * 10 ** ((SOUND_GAIN[snd] + extra + MASTER_DB) / 20)
        start = int(max(0.0, C[cue] + off) * SR)
        n = min(len(s), total - start)
        mix[start : start + n] += s[:n]

    dry = os.path.join(BASE, "tools", ".sfx-dry.f32")
    mix.astype(np.float32).tofile(dry)
    out = os.path.join(BASE, "assets", "sfx-track.wav")
    # Ducking leve: com a voz falando, os efeitos caem uns 3 dB e voltam em 200 ms. Limitador em -3 dBFS (abaixo do pico da voz).
    subprocess.run(
        [
            "ffmpeg", "-v", "error", "-y",
            "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", dry,
            "-i", VOICE,
            "-filter_complex",
            f"[1:a]aformat=sample_rates={SR}:channel_layouts=mono,apad=whole_dur={total / SR:.3f}[sc];"
            "[0:a][sc]sidechaincompress=threshold=0.1:ratio=2:attack=5:release=200:makeup=1[d];"
            "[d]highpass=f=90,alimiter=limit=0.7:level=false,aformat=sample_rates=48000:channel_layouts=stereo[o]",
            "-map", "[o]", "-c:a", "pcm_s16le", out,
        ],
        check=True,
    )
    os.remove(dry)
    print(f"{len(EVENTS)} efeitos · {len(cache)} sons · trilha em assets/sfx-track.wav")
