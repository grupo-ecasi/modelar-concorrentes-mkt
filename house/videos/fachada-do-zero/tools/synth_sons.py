"""Sintetiza os sons de obra (loops) e a música de fundo do vídeo, tudo em numpy, com sementes fixas.

Saída em assets/sfx/synth/: chuva, rolo, broxa, lixa, espatula, grilos, trovao (48 kHz, mono) e
assets/musica.wav (estéreo): trilha leve e alegre (Dó maior, 96 BPM, I–V–vi–IV) com pad, pluck,
baixo e chocalho, filtrada para ficar atrás da voz. Sem licença de terceiros: tudo é gerado aqui.

Uso: python -I tools/synth_sons.py
"""
import os
import wave

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "assets", "sfx", "synth")
SR = 48000


def t_axis(d):
    return np.arange(int(d * SR)) / SR


def band(x, lo, hi, order=4):
    n = len(x); f = np.fft.rfftfreq(n, 1 / SR); X = np.fft.rfft(x); m = np.ones_like(f)
    if lo > 0: m *= 1 / np.sqrt(1 + (lo / np.maximum(f, 1e-3)) ** (2 * order))
    if hi < SR / 2: m *= 1 / np.sqrt(1 + (f / hi) ** (2 * order))
    return np.fft.irfft(X * m, n)


def norm(x, peak=0.89):
    return x * (peak / (np.abs(x).max() or 1.0))


def fade(x, a=0.01, b=0.05):
    na, nb = int(a * SR), int(b * SR); x = x.copy()
    x[:na] *= np.linspace(0, 1, na); x[-nb:] *= np.linspace(1, 0, nb); return x


def loopavel(x, xf=0.25):
    """Cruza o fim com o começo para o loop não estalar."""
    n = int(xf * SR); y = x[:-n].copy(); y[:n] = y[:n] * np.linspace(0, 1, n) + x[-n:] * np.linspace(1, 0, n); return y


def salvar(nome, x, sr=SR, estereo=False):
    os.makedirs(os.path.dirname(nome), exist_ok=True)
    x = np.clip(x, -1, 1)
    dados = (x * 32767).astype(np.int16)
    with wave.open(nome, "wb") as w:
        w.setnchannels(2 if estereo else 1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(dados.T.flatten().tobytes() if estereo else dados.tobytes())


rng = np.random.default_rng(42)

# ---------- loops de obra ----------
def chuva(d=6.0):
    n = rng.standard_normal(int(d * SR))
    base = band(n, 400, 9000) * 0.6
    gotas = np.zeros_like(n)
    for _ in range(int(d * 90)):
        i = rng.integers(0, len(n) - 800); e = np.exp(-np.arange(800) / 90.0)
        gotas[i:i + 800] += e * rng.standard_normal(800) * rng.uniform(0.3, 1)
    return loopavel(norm(base + band(gotas, 1500, 12000) * 0.5, 0.7))


def rolo(d=4.0):
    # "shhhk" úmido no ritmo do vaivém (2 Hz) com estalidos da espuma
    tt = t_axis(d); n = rng.standard_normal(len(tt))
    corpo = band(n, 300, 3500) * (0.55 + 0.45 * np.abs(np.sin(np.pi * 2 * tt))) ** 1.5
    estalo = band(rng.standard_normal(len(tt)) * (rng.random(len(tt)) > 0.997), 2000, 9000) * 2
    return loopavel(norm(corpo + estalo, 0.7))


def broxa(d=4.0):
    tt = t_axis(d); n = rng.standard_normal(len(tt))
    env = np.abs(np.sin(np.pi * 2.5 * tt)) ** 2
    return loopavel(norm(band(n, 1200, 7000) * env, 0.6))


def lixa(d=4.0):
    tt = t_axis(d); n = rng.standard_normal(len(tt))
    env = 0.4 + 0.6 * np.abs(np.sin(np.pi * 3.5 * tt))
    return loopavel(norm(band(n, 2500, 11000) * env + band(n, 600, 1800) * env * 0.3, 0.7))


def espatula(d=4.0):
    tt = t_axis(d); n = rng.standard_normal(len(tt))
    env = np.clip(np.sin(np.pi * 1.2 * tt), 0, 1) ** 0.5
    raspa = band(n, 1800, 6000) * env + 0.15 * np.sin(2 * np.pi * 2400 * tt) * env * band(n, 1, 30)
    return loopavel(norm(raspa, 0.6))


def grilos(d=6.0):
    tt = t_axis(d); y = np.zeros_like(tt)
    for f0, ritmo, fase in [(4200, 3.1, 0), (4700, 2.7, 1.3), (3900, 3.6, 2.1)]:
        pulsos = (np.sin(2 * np.pi * ritmo * tt + fase) > 0.6) * (np.sin(2 * np.pi * 28 * tt) > 0)
        y += np.sin(2 * np.pi * f0 * tt) * pulsos * 0.3
    return loopavel(norm(band(y, 2500, 9000), 0.5))


def trovao(d=3.5):
    tt = t_axis(d); n = rng.standard_normal(len(tt))
    env = np.exp(-tt * 1.2) * (1 - np.exp(-tt * 30))
    return fade(norm(band(n, 30, 400) * env + band(n, 400, 2000) * env * np.exp(-tt * 4) * 0.4, 0.85), 0.005, 0.5)


# ---------- música ----------
def nota(f, d, amp=1.0, tipo="pluck"):
    tt = t_axis(d)
    if tipo == "pluck":
        env = np.exp(-tt * 5.5) * (1 - np.exp(-tt * 400))
        y = sum(np.sin(2 * np.pi * f * k * tt) / k ** 1.6 for k in range(1, 6))
    elif tipo == "pad":
        env = np.minimum(1, tt / 0.6) * np.minimum(1, (d - tt) / 0.6)
        y = sum(np.sin(2 * np.pi * f * (1 + dt) * tt) for dt in (-0.004, 0, 0.004)) / 3
        y += 0.3 * np.sin(2 * np.pi * f * 2 * tt)
    else:  # baixo
        env = np.exp(-tt * 2.2) * (1 - np.exp(-tt * 200))
        y = np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(2 * np.pi * f * 2 * tt)
    return y * env * amp


def musica(dur):
    bpm = 96; beat = 60 / bpm; compasso = 4 * beat
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    acordes = [[60, 64, 67], [55, 59, 62], [57, 60, 64], [53, 57, 60]]  # C G Am F
    baixos = [36, 43, 45, 41]
    L = np.zeros(int((dur + 4) * SR)); R = np.zeros_like(L)
    def add(sig, t0, pan=0.0):
        i = int(t0 * SR); n = min(len(sig), len(L) - i)
        if n <= 0: return
        L[i:i + n] += sig[:n] * (1 - pan) * 0.5 * 2 ** 0.5 / 1.414
        R[i:i + n] += sig[:n] * (1 + pan) * 0.5 * 2 ** 0.5 / 1.414
    t = 0.0; c = 0
    padrao = [0, 1, 2, 1, 0, 2, 1, 2]  # arpejo em colcheias
    while t < dur:
        ac = acordes[c % 4]
        for m in ac: add(nota(hz(m), compasso + 0.3, 0.16, "pad"), t, 0.0)
        add(nota(hz(baixos[c % 4]), beat * 1.8, 0.5, "baixo"), t)
        add(nota(hz(baixos[c % 4]), beat * 1.8, 0.35, "baixo"), t + 2 * beat)
        for k, idx in enumerate(padrao):
            oit = 12 if k in (3, 7) else 0
            add(nota(hz(ac[idx] + 12 + oit), beat * 1.2, 0.22, "pluck"), t + k * beat / 2, -0.35 if k % 2 else 0.35)
        # chocalho leve nos contratempos
        for k in range(8):
            if k % 2 == 1:
                s = band(rng.standard_normal(int(0.06 * SR)), 6000, 14000) * np.exp(-np.arange(int(0.06 * SR)) / 500.0) * 0.08
                add(s, t + k * beat / 2, 0.2)
        t += compasso; c += 1
    st = np.stack([L, R])[:, : int(dur * SR)]
    st = np.stack([band(ch, 60, 7000, 2) for ch in st])
    env = np.minimum(1, t_axis(dur) / 1.0) * np.minimum(1, (dur - t_axis(dur)) / 3.0)
    return norm(st * env, 0.8)


if __name__ == "__main__":
    for nome, f in [("chuva", chuva), ("rolo", rolo), ("broxa", broxa), ("lixa", lixa), ("espatula", espatula), ("grilos", grilos), ("trovao", trovao)]:
        salvar(os.path.join(OUT, nome + ".wav"), f())
    dur = 122.84
    salvar(os.path.join(BASE, "assets", "musica.wav"), musica(dur), estereo=True)
    print("ok: 7 sons em assets/sfx/synth e assets/musica.wav")
