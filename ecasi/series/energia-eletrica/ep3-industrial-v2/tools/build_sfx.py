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
    "click-soft": 4,
    "chime": -1,
    "ping": 2,
    "notification": 0,
    "error": -2,
    "glitch-1": -4,
    "glitch-3": -2,
    "click": -1,
    "impact-bass-1": 3,
    "impact-boom": 0,
    "zhhh": -4,
    # Energia sintetizada (tools/synth_sfx.py)
    "arc-crackle": -3,
    "zap-short": -2,
    "big-arc": 0,
    "spark-burst": -4,
    "spark-small": -6,
    "hum-swell": -8,
    "overload-hum": -6,
    "sizzle": -8,
    "breaker-on": 0,
    "breaker-off": 0,
    "dr-trip": 1,
    "button": -2,
    "rattle": -4,
    "surge": -2,
    "power-down": -6,
    "power-up": -8,
    "ground-flow": -7,
    "leak": -7,
    "lid-close": -1,
    "lid-open": -4,
}

# (marca, deslocamento em s, som, ganho extra em dB) — cada som preso à animação que ele acompanha (world.html)
EVENTS = [
    # Gancho: aperta O, o motor desacelera; o display continua aceso
    ("hook", 0.62, "button", 2),
    ("hook", 0.75, "power-down", 0),
    ("pode", 0.2, "whoosh-short", -2),
    ("nao", 0.0, "impact-bass-1", 0),
    ("desligar", 0.15, "whoosh-short", -2),
    ("desligar", 0.6, "hum-swell", 2),
    ("camadas", 0.0, "pop", -1),
    ("camadas", 0.12, "pop", -1),
    ("camadas", 0.24, "pop", 0),
    # Problema: capacitores carregados, partida remota pelo CLP, curto vira arco
    ("capacitores", -0.2, "hum-swell", 0),
    ("capacitores", 0.0, "pop", -4),
    ("v540", -0.3, "ping", -5),
    ("minutos", 0.0, "sizzle", -2),
    ("alguem", 0.0, "glitch-3", 1),
    ("alguem", 0.65, "button", 0),
    ("alguem", 0.7, "power-up", 2),
    ("curto", -0.1, "pop", -3),
    ("arco", -0.12, "big-arc", -5),
    ("arco", -0.1, "impact-boom", -8),
    ("arco", -0.05, "spark-burst", -2),
    ("arco", 0.35, "spark-burst", 0),
        # Camada 1: prancheta
    ("c1", 0.0, "whoosh-short", 0),
    ("analise", -0.2, "pop", 0),
    ("permissao", -0.15, "pop", 0),
    ("diagrama", -0.15, "pop", 0),
    ("diagrama", 0.4, "chime", -4),
    # Camada 2: chave geral, comando, ar do freio e os cadeados
    ("c2", 0.0, "whoosh-short", -2),
    ("bloquear", 0.2, "breaker-off", 2),
    ("bloquear", 0.35, "power-down", -4),
    ("todas", -0.2, "pop", -2),
    ("fontes", 0.25, "breaker-off", -1),
    ("chave", 0.1, "click", 2),
    ("cada", -0.1, "pop", -2),
    ("proprio", 0.35, "click-soft", 1),
    ("cadeado", 0.75, "click-soft", 1),
    ("tira", 0.0, "chime", -5),
    # Camada 3: espera, tenta dar partida (não gira), abre a porta e mede 0 V
    ("c3", 0.0, "whoosh-short", 0),
    ("espere", -0.2, "pop", -2),
    ("etiqueta", 0.0, "ping", 3),
    ("tente", -0.15, "pop", -2),
    ("partida2", -0.15, "button", 7),
    ("partida2", 0.5, "chime", -4),
    ("meca", -0.55, "lid-open", -2),
    ("meca", -0.15, "pop", -2),
    ("meca", 1.0, "ping", -2),
    # Mito: o display apaga, mas o barramento continua carregado
    ("mito", 0.0, "notification", -5),
    ("mito", 0.05, "lid-close", -3),
    ("apagou", 0.0, "power-down", 2),
    ("naoMito", 0.0, "impact-bass-1", -2),
    ("display2", -0.2, "hum-swell", -6),
    ("v540b", -0.2, "pop", 0),
    ("mas", -0.1, "glitch-3", 0),
    # Norma: abre o painel descarregado, de luvas e roupa FR
    ("norma", 0.1, "lid-open", -3),
    ("norma", 0.2, "pop", 3),
    ("nr12", -0.15, "pop", 0),
    ("nr1", -0.15, "pop", -3),
    ("nr1", 0.1, "click-soft", 3),
    # Chamada final: tira os cadeados, religa as fontes e o motor volta a girar
    ("cta", -0.35, "zhhh", 2),
    ("cta", 0.4, "lid-close", -8),
    ("treinamento", 0.0, "pop", 0),
    ("ecasi", -0.2, "pop", 0),
    ("proximo", -0.2, "pop", -3),
    ("proximo", 0.35, "click-soft", -3),
    ("proximo", 1.05, "breaker-on", -4),
    ("proximo", 2.05, "breaker-on", -3),
    ("proximo", 3.2, "power-up", 5),
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
    synth = os.path.join(BASE, "assets", "sfx", "synth", name + ".wav")
    a = decode(synth if os.path.exists(synth) else os.path.join(BASE, "assets", "sfx", name + ".mp3"))
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
