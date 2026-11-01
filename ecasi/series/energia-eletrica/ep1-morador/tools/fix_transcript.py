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
    "amperes.": "ampères.",
    "microondas": "micro-ondas",
    "50V,": "50,",
    "127V": "127 V",
    "220V.": "220 V.",
    "grupo": "Grupo",
    "ECAS.": "ECASI.",
    "Ecasi.": "ECASI.",
    "quadro?": "quadro.",
}

words = json.load(open(os.path.join(BASE, "assets", "transcript-raw.json"), encoding="utf-8"))
out = []
for w in words:
    w = dict(w)
    w["text"] = FIX.get(w["text"], w["text"])
    out.append(w)

json.dump(out, open(os.path.join(BASE, "assets", "transcript.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(" ".join(w["text"] for w in out))
