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
    "sparkle": -4,
    "whoosh": -6,
}

# (marca, deslocamento em s, som, ganho extra em dB)
EVENTS = [
    # Gancho
    ("hook", 0.3, "whoosh-short", 4),  # rolo passando
    ("volta", 0.0, "impact-bass-1", 0),
    ("mas", -0.15, "whoosh-short", -3),  # corte para o raio-x
    ("vivo", -0.1, "pop", 0),
    ("camadas", 0.0, "pop", -1),
    ("camadas", 0.12, "pop", -2),
    ("camadas", 0.24, "pop", -3),
    # Problema
    ("umidade1", -0.1, "pop", 0),
    ("p70", -0.5, "click-soft", 0),
    ("p70", 0.2, "ping", 0),
    ("cria", -0.2, "whoosh-short", -4),
    ("raizes", 0.0, "glitch-1", 5),
    ("poros", 0.0, "click-soft", -5),
    ("esconde", -0.1, "error", -2),
    # Camada 1
    ("c1", 0.0, "whoosh-short", -3),
    ("infiltracao", -0.15, "pop", -5),
    ("vazamento", -0.1, "pop", 0),
    ("vapor", -0.1, "pop", 0),
    ("resolver", -0.1, "error", 0),
    # Camada 2
    ("c2", 0.0, "whoosh-short", -2),
    ("agua", -0.1, "pop", -2),
    ("luva", 0.0, "click-soft", 0),
    ("janela", 0.0, "whoosh", 0),
    ("agir", -0.1, "pop", 0),
    ("enxagua", -0.1, "pop", 0),
    ("secar", -0.1, "chime", 0),
    ("nunca", -0.1, "notification", -3),
    # Camada 3
    ("c3", 0.0, "whoosh-short", 0),
    ("c3", 1.0, "whoosh-short", -3),
    ("base", -0.1, "pop", 0),
    ("antimofo1", -0.1, "sparkle", 0),
    ("banheiro", -0.1, "pop", 0),
    # Mito
    ("mito", 0.0, "notification", -5),
    ("naoMito", 0.0, "impact-bass-1", -2),
    ("protege", -0.1, "pop", 0),
    ("umida", 0.0, "glitch-3", 5),
    ("voltaBaixo", -0.5, "glitch-1", -2),
    # Norma
    ("norma", 0.3, "pop", 2),
    ("limpa", -0.15, "click", 0),
    ("seca", -0.15, "click", 0),
    ("semMofo", -0.15, "chime", 0),
    # Chamada final e fecho
    ("cta", 0.0, "whoosh-short", 0),
    ("house", 0.0, "pop", 0),
    ("orcamento", -0.1, "click", 0),
    ("loop", 0.0, "whoosh-short", -2),
    ("dessas", 0.0, "pop", 5),
    ("dessas", 0.15, "pop", 5),
    ("dessas", 0.3, "pop", 5),
    ("faltando", -0.1, "impact-bass-1", -4),
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
