"""Monta a trilha de fundo (assets/bed.wav): efeitos pontuais + loops de obra + música, com ducking pela voz.

Os tempos vêm de tools/cues.json (os mesmos de C em compositions/world.html e hud.html).
- Efeitos pontuais (Pixabay, assets/sfx/*.mp3) e sintetizados (assets/sfx/synth/*.wav), nivelados pela energia do início.
- Loops (chuva, rolo, broxa, lixa, espátula, grilos) com entrada e saída suaves.
- Música (assets/musica.wav) bem abaixo: MUSICA_DB.
- Tudo passa por um sidechain com a voz (cai ~6 dB quando ela fala) e por um limitador.

Uso: python -I tools/build_bed.py   (depois: python -I tools/measure_mix.py, se quiser conferir)
"""
import json
import os
import subprocess

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
VOZ = os.path.join(BASE, "assets", "narracao-norm.mp3")
C = json.load(open(os.path.join(BASE, "tools", "cues.json"), encoding="utf-8"))

MASTER_DB = 0.0      # volume geral dos efeitos
MUSICA_DB = -23.0    # música em relação aos efeitos (bem baixa, atrás da voz)

GANHO = {"pop": -5, "whoosh-short": -6, "whoosh": -6, "click": -2, "click-soft": 3, "chime": -2, "ping": 1, "notification": -1,
         "error": -4, "glitch-1": -5, "glitch-3": -4, "impact-bass-1": 1, "sparkle": -4, "riser": -8,
         "trovao": -3, "chuva": -9, "rolo": -8, "broxa": -9, "lixa": -10, "espatula": -10, "grilos": -15}

E = []  # (tempo, som, ganho extra)
def ev(t, s, g=0.0): E.append((t, s, g))

# abertura
ev(0.05, "impact-bass-1", -2); ev(0.15, "sparkle", 0); ev(1.25, "whoosh-short", 0)
# selos dos degraus + recap + CTA
for k in ["d1", "d2", "d3", "d4", "d5", "d6", "d7", "recap", "cta"]:
    ev(C[k] - 0.05, "whoosh-short", 1); ev(C[k] + 0.1, "pop", -2)
# etiquetas (pop) — mesmas entradas do hud.html
for t in [5.6, 12.2, 15.6, 22.0, 30.0, 38.9, 45.6, 50.6, 55.4, 61.0, 70.0, 76.0, 78.4, 86.2, C["faca7"] + 0.2]:
    ev(t, "pop", -1)
# latas e ferramentas entrando
for t in [C["d2"] + 0.3, C["d3"] + 0.3, C["d4"] + 5.3, C["d5"] + 0.3, C["d6"] + 0.3]:
    ev(t, "click-soft", 0)
# raio-x
for t in [24.4, 31.2, 50.6, 79.6]:
    ev(t, "whoosh-short", -2); ev(t + 0.25, "ping", -3)
# problemas e conquistas
ev(C["chuva1"] + 0.2, "trovao", 0); ev(C["chuva2"] + 0.2, "trovao", -3)
ev(22.0, "error", -2); ev(38.96, "glitch-1", 0); ev(55.4, "glitch-3", 0); ev(70.0, "error", -4)
ev(C["porem3"] + 0.1, "whoosh", 2); ev(C["soque5"] + 0.1, "whoosh", 2)     # passagem de tempo
ev(C["d6"] + 6.9, "sparkle", 2); ev(C["agora6"], "pop", 0); ev(C["agora6"] + 0.12, "pop", 0); ev(C["agora6"] + 0.24, "pop", 2); ev(C["agora6"] + 0.4, "chime", 0)
# barras do degrau final
ev(94.0, "whoosh-short", -2); ev(96.7, "click", 0); ev(97.6, "click", 0); ev(C["faca7"] - 1.2, "riser", 0); ev(C["faca7"] + 0.8, "chime", 0)
# recap e CTA
ev(C["recap"] + 2.6, "sparkle", 2); ev(C["recap"] + 2.7, "pop", 0); ev(C["recap"] + 2.85, "pop", 2); ev(C["cta"] + 0.3, "notification", 0)

LOOPS = [  # (som, início, fim)
    ("broxa", C["d1"] + 1.3, C["chuva1"]), ("chuva", C["chuva1"], C["d2"]), ("rolo", C["d2"] + 0.8, C["ent2"]), ("chuva", C["chuva2"], C["d3"]),
    ("rolo", C["d3"] + 0.7, C["d3"] + 5), ("lixa", C["d4"] + 0.1, C["d4"] + 5.2), ("rolo", C["d4"] + 5.3, C["existe4"]),
    ("espatula", C["d5"] + 0.2, C["d5"] + 6.5), ("grilos", C["soque5"] + 2.0, C["d6"] - 1.0), ("rolo", C["d6"] + 0.8, C["agora6"]),
    ("chuva", C["agora6"] + 0.3, C["d7"]),
]


def decode(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)


def som(nome):
    p = os.path.join(BASE, "assets", "sfx", nome + ".mp3")
    if not os.path.exists(p):
        p = os.path.join(BASE, "assets", "sfx", "synth", nome + ".wav")
    a = decode(p)
    pk = np.abs(a).max() or 1.0
    a = a[max(0, int(np.argmax(np.abs(a) > pk * 0.05)) - 48):]
    rms = np.sqrt(np.mean(a[: int(0.25 * SR)] ** 2)) or 1e-6
    a = a * (10 ** (-18 / 20) / rms)
    return a * min(1.0, 10 ** (-3 / 20) / (np.abs(a).max() or 1.0))


if __name__ == "__main__":
    total = int((C["end"] + 0.5) * SR)
    mix = np.zeros(total); cache = {}
    def pega(n):
        if n not in cache: cache[n] = som(n)
        return cache[n]
    for t, s, g in E:
        x = pega(s) * 10 ** ((GANHO[s] + g + MASTER_DB) / 20)
        i = int(max(0, t) * SR); n = min(len(x), total - i); mix[i:i + n] += x[:n]
    for s, a, b in LOOPS:
        base = pega(s) * 10 ** ((GANHO[s] + MASTER_DB) / 20)
        n = int((b - a) * SR); reps = int(np.ceil(n / len(base))) + 1
        x = np.tile(base, reps)[:n]
        f = min(int(0.5 * SR), n // 3); x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
        i = int(a * SR); mix[i:i + n] += x[: total - i]
    # música (estéreo) por baixo
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(BASE, "assets", "musica.wav"), "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    mus = np.frombuffer(raw, dtype=np.float32).astype(np.float64).reshape(-1, 2).T * 10 ** (MUSICA_DB / 20) * 4.0
    st = np.stack([mix, mix])
    n = min(st.shape[1], mus.shape[1]); st[:, :n] += mus[:, :n]
    seco = os.path.join(BASE, "tools", ".bed-seco.f32")
    st.T.astype(np.float32).tofile(seco)
    out = os.path.join(BASE, "assets", "bed.wav")
    subprocess.run([
        "ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", seco, "-i", VOZ,
        "-filter_complex",
        f"[1:a]aformat=sample_rates={SR}:channel_layouts=stereo,apad=whole_dur={total / SR:.3f}[sc];"
        "[0:a][sc]sidechaincompress=threshold=0.05:ratio=3:attack=8:release=250:makeup=1[d];"
        "[d]highpass=f=50,alimiter=limit=0.7:level=false[o]",
        "-map", "[o]", "-c:a", "pcm_s16le", out], check=True)
    os.remove(seco)
    print(f"{len(E)} efeitos, {len(LOOPS)} loops, música em {MUSICA_DB} dB -> assets/bed.wav")
