"""Sintetiza os efeitos sonoros de energia da série (arco, faísca, zumbido, chiado, disjuntor, DR, surto, tampa).

Tudo é gerado em numpy com sementes fixas: o mesmo comando sempre produz os mesmos arquivos. Os filtros são
feitos por FFT (sem scipy). Saída em assets/sfx/synth/<nome>.wav, 48 kHz, mono, pico em -1 dBFS.

Uso: python -I tools/synth_sfx.py
"""
import os
import wave

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "assets", "sfx", "synth")
SR = 48000


def t_axis(dur):
    return np.arange(int(dur * SR)) / SR


def band(x, lo, hi, order=4):
    """Passa-faixa por FFT com resposta tipo Butterworth (lo/hi em Hz)."""
    n = len(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    X = np.fft.rfft(x)
    m = np.ones_like(f)
    if lo > 0:
        m *= 1 / np.sqrt(1 + (lo / np.maximum(f, 1e-3)) ** (2 * order))
    if hi < SR / 2:
        m *= 1 / np.sqrt(1 + (f / hi) ** (2 * order))
    return np.fft.irfft(X * m, n)


def norm(x, peak=0.89):
    p = np.abs(x).max() or 1.0
    return x * (peak / p)


def fade(x, a=0.004, b=0.03):
    n = len(x)
    na, nb = int(a * SR), int(b * SR)
    env = np.ones(n)
    if na:
        env[:na] = np.linspace(0, 1, na)
    if nb:
        env[-nb:] *= np.linspace(1, 0, nb)
    return x * env


def clicks(dur, rate, rng, lo=1800, hi=11000, decay=0.0035, rate_env=None):
    """Estalos curtos em tempos aleatórios (densidade em estalos/s, opcionalmente variável no tempo)."""
    n = int(dur * SR)
    out = np.zeros(n)
    t = 0.0
    while t < dur:
        r = rate * (rate_env(t) if rate_env else 1.0)
        t += rng.exponential(1 / max(r, 1e-3))
        if t >= dur:
            break
        L = int(rng.uniform(0.6, 1.6) * decay * SR * 6)
        i = int(t * SR)
        L = min(L, n - i)
        if L <= 8:
            continue
        burst = rng.standard_normal(L) * np.exp(-np.arange(L) / (decay * SR))
        out[i : i + L] += burst * rng.uniform(0.3, 1.0)
    return band(out, lo, hi)


def buzz(dur, f0=60, rng=None, sharp=4):
    """Zumbido de arco: ruído modulado a 2×f0 (meia-onda da rede), bem 'elétrico'."""
    t = t_axis(dur)
    am = np.abs(np.sin(2 * np.pi * f0 * t)) ** sharp
    nz = rng.standard_normal(len(t))
    return band(nz, 250, 7000) * (0.25 + am)


def hum(dur, f0=60, weights=(0.0, 1.0, 0.55, 0.7, 0.35, 0.4, 0.2, 0.25), grit=0.0, rng=None):
    t = t_axis(dur)
    x = np.zeros_like(t)
    for k, w in enumerate(weights, start=1):
        x += w * np.sin(2 * np.pi * f0 * k * t + k * 0.7)
    if grit > 0:
        g = np.tanh(3 * np.sin(2 * np.pi * 2 * f0 * t)) * grit
        x += g + grit * 0.3 * band(rng.standard_normal(len(t)), 400, 3000) * np.abs(np.sin(2 * np.pi * f0 * t))
    return x


def sh_flicker(dur, rate, rng, lo=0.35, hi=1.0):
    """Amplitude que muda aos saltos (piscar do arco), suavizada."""
    n = int(dur * SR)
    steps = int(dur * rate) + 2
    vals = rng.uniform(lo, hi, steps)
    idx = np.minimum((np.arange(n) / SR * rate).astype(int), steps - 1)
    env = vals[idx]
    k = int(0.004 * SR)
    return np.convolve(env, np.ones(k) / k, mode="same")


def env_adsr(dur, a, r, sustain=1.0):
    n = int(dur * SR)
    e = np.full(n, sustain)
    na, nr = int(a * SR), int(r * SR)
    e[:na] = np.linspace(0, sustain, na)
    if nr:
        e[-nr:] = np.linspace(sustain, 0, nr)
    return e


def modes(dur, freqs, decays, amps, rng):
    t = t_axis(dur)
    x = np.zeros_like(t)
    for f, d, a in zip(freqs, decays, amps):
        x += a * np.sin(2 * np.pi * f * t + rng.uniform(0, 6)) * np.exp(-t / d)
    return x


def at(dst, src, sec, gain=1.0):
    i = int(sec * SR)
    n = min(len(src), len(dst) - i)
    if n > 0:
        dst[i : i + n] += src[:n] * gain
    return dst


# ---------------- Sons ----------------
def arc_crackle(seed=1, dur=1.6):
    rng = np.random.default_rng(seed)
    t = t_axis(dur)
    x = 0.7 * buzz(dur, rng=rng, sharp=6) * sh_flicker(dur, 18, rng)
    x += 1.1 * clicks(dur, 90, rng)
    x += 0.35 * band(rng.standard_normal(len(t)), 3000, 12000) * sh_flicker(dur, 30, rng, 0.1, 1)
    x *= np.exp(-t / (dur * 0.7)) * env_adsr(dur, 0.005, 0.15)
    return x


def zap_short(seed=2, dur=0.38):
    rng = np.random.default_rng(seed)
    t = t_axis(dur)
    f = 1900 * np.exp(-t / 0.09) + 260
    sweep = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.12)
    x = 0.8 * buzz(dur, rng=rng, sharp=8) * np.exp(-t / 0.1) + 0.5 * sweep + 0.9 * clicks(dur, 220, rng, rate_env=lambda s: np.exp(-s / 0.08))
    return x * env_adsr(dur, 0.002, 0.05)


def big_arc(seed=3, dur=2.4):
    rng = np.random.default_rng(seed)
    t = t_axis(dur)
    blast = band(rng.standard_normal(len(t)), 80, 9000) * np.exp(-t / 0.12)
    thump = np.sin(2 * np.pi * (70 * np.exp(-t / 0.3) + 38) * t) * np.exp(-t / 0.35)
    tail = arc_crackle(seed + 10, dur) * 0.9
    hum120 = 0.5 * hum(dur, weights=(0, 1, 0.8, 0.6, 0.5, 0.4), grit=0.6, rng=rng) * np.exp(-t / 0.7)
    x = 1.3 * blast + 1.1 * thump + tail + 0.5 * hum120
    return x * env_adsr(dur, 0.001, 0.3)


def spark_burst(seed=4, dur=1.1, rate=260):
    rng = np.random.default_rng(seed)
    t = t_axis(dur)
    x = clicks(dur, rate, rng, lo=1500, hi=13000, decay=0.0025, rate_env=lambda s: np.exp(-s / 0.25))
    tinks = np.zeros(len(t))
    for _ in range(14):
        s = rng.uniform(0.0, 0.7)
        L = int(0.03 * SR)
        f = rng.uniform(3500, 7500)
        tt = np.arange(L) / SR
        at(tinks, np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.008) * rng.uniform(0.2, 0.6), s)
    return (x + tinks) * env_adsr(dur, 0.001, 0.1)


def hum_swell(seed=5, dur=2.6):
    rng = np.random.default_rng(seed)
    t = t_axis(dur)
    x = hum(dur, rng=rng) * (1 + 0.08 * np.sin(2 * np.pi * 3.1 * t))
    x += 0.15 * band(rng.standard_normal(len(t)), 120, 900) * np.abs(np.sin(2 * np.pi * 60 * t))
    return x * env_adsr(dur, 0.45, 0.9)


def overload_hum(seed=6, dur=3.2):
    rng = np.random.default_rng(seed)
    t = t_axis(dur)
    grow = np.clip(t / (dur * 0.7), 0, 1)
    wob = 1 + 0.004 * np.sin(2 * np.pi * 0.7 * t)
    x = hum(dur, f0=60 * wob.mean(), weights=(0, 1, 0.7, 0.8, 0.5, 0.55, 0.3, 0.35), grit=0.25 + 0.75 * 1, rng=rng)
    x = x * (0.45 + 0.55 * grow)
    x += 0.25 * clicks(dur, 6, rng, lo=1500, hi=9000) * grow
    return x * env_adsr(dur, 0.35, 0.6)


def sizzle(seed=7, dur=4.2):
    rng = np.random.default_rng(seed)
    t = t_axis(dur)
    fry = band(rng.standard_normal(len(t)), 1800, 9000) * sh_flicker(dur, 22, rng, 0.25, 1.0)
    x = 0.5 * fry + 0.8 * clicks(dur, 45, rng, lo=2000, hi=12000)
    return x * env_adsr(dur, 0.4, 1.0)


def breaker(seed=8, dur=0.28, off=False):
    rng = np.random.default_rng(seed)
    t = t_axis(dur)
    x = np.zeros(len(t))
    c1 = band(rng.standard_normal(int(0.012 * SR)), 1500, 7000) * np.exp(-np.arange(int(0.012 * SR)) / (0.0025 * SR))
    c2 = band(rng.standard_normal(int(0.02 * SR)), 900, 6000) * np.exp(-np.arange(int(0.02 * SR)) / (0.004 * SR))
    body = modes(0.12, [180 if not off else 150, 910, 2300], [0.025, 0.012, 0.006], [0.9, 0.5, 0.3], rng)
    at(x, c1 * 0.5, 0.0)
    at(x, c2 * 1.0, 0.024 if not off else 0.016)
    at(x, body * 0.9, 0.024 if not off else 0.016)
    return fade(x, 0.0005, 0.03)


def dr_trip(seed=9, dur=0.42):
    rng = np.random.default_rng(seed)
    x = breaker(seed, dur, off=True) * 1.2
    t = t_axis(0.18)
    spring = np.sin(2 * np.pi * (1350 + 90 * np.sin(2 * np.pi * 38 * t)) * t) * np.exp(-t / 0.045) * 0.35
    at(x, spring, 0.02)
    snap = band(rng.standard_normal(int(0.006 * SR)), 3000, 12000)
    at(x, snap * 0.8, 0.0)
    return x


def button(seed=10, dur=0.12):
    rng = np.random.default_rng(seed)
    x = np.zeros(int(dur * SR))
    c = band(rng.standard_normal(int(0.008 * SR)), 2000, 9000) * np.exp(-np.arange(int(0.008 * SR)) / (0.0015 * SR))
    at(x, c, 0.0)
    at(x, modes(0.05, [1400, 3100], [0.008, 0.004], [0.4, 0.2], rng), 0.0)
    return x


def rattle(seed=11, dur=0.9):
    rng = np.random.default_rng(seed)
    x = np.zeros(int(dur * SR))
    for k in range(9):
        at(x, button(seed + k) * rng.uniform(0.4, 0.9), 0.03 + k * 0.085 + rng.uniform(-0.01, 0.01))
    return x


def surge(seed=12, dur=1.0):
    rng = np.random.default_rng(seed)
    t = t_axis(dur)
    f = 260 * (3200 / 260) ** np.clip(t / 0.36, 0, 1)
    whine = np.sin(2 * np.pi * np.cumsum(f) / SR) * (np.abs(np.sin(2 * np.pi * 60 * t)) ** 2 * 0.6 + 0.4)
    whine *= np.clip(t / 0.05, 0, 1) * np.where(t < 0.38, 1.0, np.exp(-(t - 0.38) / 0.05))
    x = 0.55 * whine
    at(x, zap_short(seed + 1) * 1.1, 0.36)
    return x * env_adsr(dur, 0.01, 0.1)


def power_down(seed=13, dur=0.7):
    rng = np.random.default_rng(seed)
    t = t_axis(dur)
    f = 240 * np.exp(-t / 0.25) + 50
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.3)
    x += 0.3 * np.sin(2 * np.pi * np.cumsum(f * 2) / SR) * np.exp(-t / 0.2)
    return x * env_adsr(dur, 0.01, 0.1)


def power_up(seed=14, dur=0.8):
    t = t_axis(dur)
    f = 60 + 180 * (1 - np.exp(-t / 0.2))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.35 * np.sin(2 * np.pi * np.cumsum(f * 2) / SR)
    return x * env_adsr(dur, 0.05, 0.4) * 0.8


def ground_flow(seed=15, dur=1.4):
    rng = np.random.default_rng(seed)
    t = t_axis(dur)
    f = 220 * (1 + 0.5 * np.clip(t / dur, 0, 1))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.5 * np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR) + 0.3 * np.sin(2 * np.pi * np.cumsum(f * 2) / SR)
    x += 0.2 * band(rng.standard_normal(len(t)), 2000, 8000) * sh_flicker(dur, 25, rng, 0.2, 1)
    return x * env_adsr(dur, 0.15, 0.6)


def leak(seed=16, dur=2.4):
    rng = np.random.default_rng(seed)
    t = t_axis(dur)
    x = hum(dur, weights=(0, 1, 0.3, 0.6, 0.2, 0.3), rng=rng) * (0.55 + 0.45 * np.sin(2 * np.pi * 5.5 * t) ** 2)
    x += 0.35 * clicks(dur, 8, rng, lo=2500, hi=10000)
    return x * env_adsr(dur, 0.25, 0.7)


def lid_close(seed=17, dur=0.7):
    rng = np.random.default_rng(seed)
    x = np.zeros(int(dur * SR))
    at(x, modes(0.6, [312, 747, 1193, 1822, 2650], [0.12, 0.09, 0.06, 0.04, 0.03], [0.8, 0.6, 0.45, 0.3, 0.2], rng), 0.0)
    thud = band(rng.standard_normal(int(0.05 * SR)), 60, 600) * np.exp(-np.arange(int(0.05 * SR)) / (0.012 * SR))
    at(x, thud * 1.4, 0.0)
    at(x, button(seed + 1) * 0.9, 0.04)
    return fade(x, 0.0005, 0.08)


def lid_open(seed=18, dur=0.75):
    rng = np.random.default_rng(seed)
    t = t_axis(dur)
    x = np.zeros(len(t))
    at(x, button(seed) * 1.0, 0.0)
    creak_f = 520 + 160 * np.sin(2 * np.pi * 1.3 * t)
    creak = band(rng.standard_normal(len(t)), 300, 2500) * (np.abs(np.sin(2 * np.pi * np.cumsum(creak_f / 9) / SR)) ** 6)
    x += 0.5 * creak * env_adsr(dur, 0.08, 0.3)
    x += 0.3 * modes(dur, [430, 1020], [0.2, 0.1], [0.4, 0.2], rng) * env_adsr(dur, 0.05, 0.3)
    return x


SOUNDS = {
    "arc-crackle": arc_crackle,
    "zap-short": zap_short,
    "big-arc": big_arc,
    "spark-burst": spark_burst,
    "spark-small": lambda: spark_burst(seed=21, dur=0.6, rate=150),
    "hum-swell": hum_swell,
    "overload-hum": overload_hum,
    "sizzle": sizzle,
    "breaker-on": lambda: breaker(seed=8, off=False),
    "breaker-off": lambda: breaker(seed=19, off=True),
    "dr-trip": dr_trip,
    "button": button,
    "rattle": rattle,
    "surge": surge,
    "power-down": power_down,
    "power-up": power_up,
    "ground-flow": ground_flow,
    "leak": leak,
    "lid-close": lid_close,
    "lid-open": lid_open,
}


def write_wav(path, x):
    x = np.clip(x, -1, 1)
    pcm = (x * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in SOUNDS.items():
        # Teto em 11 kHz: arco e faísca sem chiado áspero no agudo
        x = norm(fade(band(fn(), 0, 11000), 0.0005, 0.02))
        write_wav(os.path.join(OUT, name + ".wav"), x)
    print(f"{len(SOUNDS)} sons em assets/sfx/synth/")
