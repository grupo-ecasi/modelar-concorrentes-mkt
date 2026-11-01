"""Monta a trilha de efeitos sonoros (assets/sfx-track.wav) a partir de tools/cues.json.

Cada efeito está preso à mesma marca de tempo da animação que ele acompanha. A trilha seca é
mixada em Python e depois passa por um compressor com a voz como sidechain, que abaixa os efeitos
enquanto a narração fala.

Uso: python -I tools/build_sfx.py
"""
import array
import json
import os
import subprocess
import tempfile
import wave

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
C = json.load(open(os.path.join(BASE, "tools", "cues.json"), encoding="utf-8"))

# Equilíbrio entre os sons (dB), aplicado depois de normalizar cada arquivo pelo próprio pico
SOUND_GAIN = {
    "pop": 0,
    "whoosh-short": -4,
    "click": -2,
    "click-soft": 0,
    "chime": -4,
    "ping": -4,
    "notification": -5,
}

# (marca, deslocamento em s, som, ganho extra em dB)
EVENTS = [
    # Abertura
    ("nao", 0.0, "whoosh-short", 0),
    ("nr10", 0.24, "pop", 0),
    ("camadas", 0.0, "pop", -3),
    ("camadas", 0.12, "pop", -4),
    ("camadas", 0.24, "pop", -5),
    # Problema
    ("problema", 0.25, "click", -2),  # disjuntor liga para a explicação
    ("v220", -0.1, "pop", 0),
    ("molhada", 0.0, "click-soft", 0),
    ("ma10", 0.1, "pop", 0),
    ("trava", 0.0, "click-soft", 0),
    ("ma50", 0.1, "pop", 0),
    ("coracao", 0.0, "ping", -2),
    # Camada 1
    ("c1", 0.0, "whoosh-short", 0),
    ("desliga", 0.6, "click", 0),
    ("circuito", 0.0, "click-soft", 0),
    ("cadeado", 0.0, "click", 0),
    ("etiqueta", 0.0, "pop", -2),
    ("religa", -0.2, "pop", 0),
    # Camada 2
    ("c2", 0.0, "whoosh-short", 0),
    ("detector", -0.2, "pop", -2),
    ("energia", 0.1, "ping", -2),
    ("energia", 0.5, "pop", -3),
    ("semTensao", 0.1, "chime", 0),
    # Camada 3
    ("c3", 0.0, "whoosh-short", 0),
    ("aterramento", 0.0, "click", 0),
    ("aterramento", 1.0, "click-soft", 0),
    ("luva", 0.0, "pop", 0),
    ("ferramenta", 0.0, "pop", -1),
    # Atenção
    ("atencao", 0.0, "notification", 0),
    ("rede", 0.3, "pop", 0),
    ("polo", 0.0, "pop", 0),
    ("desligaUma", -0.05, "click", 0),
    ("v127", -0.25, "pop", 0),
    ("soDetector", 0.0, "ping", -2),
    # Norma
    ("norma", 0.8, "pop", -1),
    ("desenergizacao", -0.3, "pop", -1),
    ("treino", 0.0, "pop", -1),
    ("reciclagem", 0.0, "click-soft", 0),
    # Chamada final e fecho
    ("cta", 0.0, "whoosh-short", -1),
    ("fale", 0.0, "click", 0),
    ("loop", 0.1, "whoosh-short", -3),
    ("confira", 0.0, "pop", -3),
    ("confira", 0.72, "pop", -2),
    ("antes", 0.0, "pop", -2),
]


def decode(name):
    """Decodifica um MP3 para mono 48 kHz, corta o silêncio inicial e normaliza o pico em 1,0."""
    src = os.path.join(BASE, "assets", "sfx", name + ".mp3")
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", src, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
        capture_output=True,
        check=True,
    ).stdout
    a = array.array("h")
    a.frombytes(raw)
    peak = max(1, max(abs(x) for x in a))
    first = next(i for i, x in enumerate(a) if abs(x) > peak * 0.05)
    return [x / peak for x in a[max(0, first - 48) :]]


total = int((C["end"] + 1.0) * SR)
mix = [0.0] * total
cache = {}
for cue, off, snd, extra in EVENTS:
    if snd not in cache:
        cache[snd] = decode(snd)
    g = 10 ** ((SOUND_GAIN[snd] + extra) / 20)
    start = int(max(0.0, C[cue] + off) * SR)
    for i, s in enumerate(cache[snd]):
        j = start + i
        if j >= total:
            break
        mix[j] += s * g

peak = max(1.0, max(abs(x) for x in mix))
# Trilha seca com pico em -6 dBFS; o nível final vem do compressor e do volume no index.html
scale = (10 ** (-6 / 20)) * 32767 / peak
pcm = array.array("h", (int(max(-32767, min(32767, x * scale))) for x in mix))

with tempfile.TemporaryDirectory() as tmp:
    dry = os.path.join(tmp, "sfx-dry.wav")
    with wave.open(dry, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    out = os.path.join(BASE, "assets", "sfx-track.wav")
    voice = os.path.join(BASE, "assets", "narracao-nr10-norm.mp3")
    # Ducking leve: com a voz falando, os efeitos caem ~5 dB; voltam em 250 ms
    subprocess.run(
        [
            "ffmpeg", "-v", "error", "-y", "-i", dry, "-i", voice,
            "-filter_complex",
            f"[1:a]aformat=sample_rates=48000:channel_layouts=mono,volume=2,apad=whole_dur={total / SR:.3f}[sc];"
            "[0:a][sc]sidechaincompress=threshold=0.05:ratio=3:attack=8:release=250:makeup=1.8[d];"
            "[d]highpass=f=120,alimiter=limit=0.5:level=false,aformat=sample_rates=48000:channel_layouts=stereo[o]",
            "-map", "[o]", "-c:a", "pcm_s16le", out,
        ],
        check=True,
    )
print(f"{len(EVENTS)} efeitos · {len(cache)} sons · trilha em assets/sfx-track.wav")
