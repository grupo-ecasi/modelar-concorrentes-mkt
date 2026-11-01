"""Corrige a grafia da transcrição automática (assets/transcript-raw.json -> assets/transcript.json).

Uso: python -I tools/fix_transcript.py
"""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Troca simples, palavra por palavra
FIX = {
    "desjuntor": "disjuntor",
    "miliamperes": "miliampères,",
    "amperes.": "ampères.",
    "amperes,": "ampères,",
    "ampesam,": "ampères,",
    "MR10": "NR-10",
    "grupo": "Grupo",
    "ECAS.": "ECASI.",
    "Ecasi.": "ECASI.",
    "para": "pra",
    "2,5,": "2,5,",
}

words = json.load(open(os.path.join(BASE, "assets", "transcript-raw.json"), encoding="utf-8"))
out = []
for w in words:
    w = dict(w)
    w["text"] = FIX.get(w["text"], w["text"])
    out.append(w)

json.dump(out, open(os.path.join(BASE, "assets", "transcript.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(" ".join(w["text"] for w in out))
