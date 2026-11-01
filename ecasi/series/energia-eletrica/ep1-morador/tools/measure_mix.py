"""Mede o volume de cada efeito sonoro contra a narração, no momento em que ele entra.

Para cada efeito de tools/build_sfx.py compara:
- energia máxima do efeito (RMS em janelas de 50 ms, nos primeiros 400 ms) x energia média da voz em volta
  (±0,6 s, só trechos com fala);
- pico do efeito x pico da voz na mesma janela.
Meta: efeito de 3 a 8 dB abaixo da voz, e o pico do efeito nunca acima do pico da voz.

Uso: python -I tools/measure_mix.py
"""
import importlib.util
import os
import subprocess

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("build_sfx", os.path.join(BASE, "tools", "build_sfx.py"))
sfx_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sfx_mod)
SR = sfx_mod.SR
TARGET = (-8.0, -3.0)


def db(x):
    return 20 * np.log10(max(x, 1e-9))


voice = sfx_mod.decode(sfx_mod.VOICE)
track = sfx_mod.decode(os.path.join(BASE, "assets", "sfx-track.wav"))
n = max(len(voice), len(track))
voice = np.pad(voice, (0, n - len(voice)))
track = np.pad(track, (0, n - len(track)))


def voiced_rms(a, b):
    seg = voice[max(0, a) : b]
    if len(seg) == 0:
        return None
    fr = int(0.05 * SR)
    frames = [seg[i : i + fr] for i in range(0, len(seg) - fr + 1, fr)]
    levels = [np.sqrt(np.mean(f**2)) for f in frames]
    talk = [lv for lv in levels if db(lv) > -40]
    return np.sqrt(np.mean(np.square(talk))) if talk else None


rows, diffs, bad = [], [], 0
for cue, off, snd, _ in sfx_mod.EVENTS:
    t = max(0.0, sfx_mod.C[cue] + off)
    i = int(t * SR)
    s = track[i : i + int(0.4 * SR)]
    fr = int(0.05 * SR)
    s_rms = max(np.sqrt(np.mean(s[k : k + fr] ** 2)) for k in range(0, len(s) - fr + 1, fr // 2))
    s_pk = np.abs(s).max()
    w0, w1 = i - int(0.6 * SR), i + int(0.6 * SR)
    v_rms = voiced_rms(w0, w1)
    v_pk = np.abs(voice[max(0, w0) : w1]).max()
    if v_rms is None:
        rows.append(f"{t:6.2f}s {snd:<14} efeito {db(s_rms):6.1f} dB · sem voz por perto")
        continue
    d = db(s_rms) - db(v_rms)
    diffs.append(d)
    flag = ""
    if db(s_pk) > db(v_pk):
        flag = "  <- PICO ACIMA DA VOZ"
    elif d > TARGET[1]:
        flag = "  <- alto demais"
    elif d < TARGET[0] - 4:
        flag = "  <- baixo"
    bad += bool(flag.strip().startswith("<- PICO") or "alto" in flag)
    rows.append(f"{t:6.2f}s {snd:<14} efeito {db(s_rms):6.1f} dB · voz {db(v_rms):6.1f} dB · diferença {d:+5.1f} dB · pico {db(s_pk):5.1f}/{db(v_pk):5.1f}{flag}")

print("\n".join(rows))
print(
    f"\nDiferença efeito - voz: mediana {np.median(diffs):+.1f} dB · faixa {min(diffs):+.1f} a {max(diffs):+.1f} dB"
    f" · meta {TARGET[0]:+.0f} a {TARGET[1]:+.0f} dB · problemas: {bad}"
)
