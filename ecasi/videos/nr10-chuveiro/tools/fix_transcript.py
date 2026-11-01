"""Corrige a grafia da transcrição automática (assets/transcript-raw.json -> assets/transcript.json).

Uso: python -I tools/fix_transcript.py
"""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Troca simples, palavra por palavra
FIX = {
    "desjuntor": "disjuntor",
    "desjuntor.": "disjuntor.",
    "MR10": "NR-10",
    "NR10": "NR-10",
    "220V.": "220 V.",
    "miliamperes,": "miliampères,",
    "Nuva": "Luva",
    "Ecasi.": "ECASI.",
    "grupo": "Grupo",
    "dois": "2",
}

words = json.load(open(os.path.join(BASE, "assets", "transcript-raw.json"), encoding="utf-8"))
out = []
for i, w in enumerate(words):
    w = dict(w)
    w["text"] = FIX.get(w["text"], w["text"])
    prev = out[-1]["text"] if out else ""
    nxt = words[i + 1]["text"] if i + 1 < len(words) else ""
    # "Com uns cinquenta" saiu como "Com o 50V,"
    if w["text"] == "o" and prev == "Com" and nxt == "50V,":
        w["text"] = "uns"
    if w["text"] == "50V,":
        w["text"] = "50,"
    # "cento e vinte e sete e duzentos e vinte volts" saiu como "127 V 220V,"
    if w["text"] == "V" and prev == "127":
        w["text"] = "e"
    if w["text"] == "220V,":
        w["text"] = "220 V,"
    out.append(w)

json.dump(out, open(os.path.join(BASE, "assets", "transcript.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(" ".join(w["text"] for w in out))
