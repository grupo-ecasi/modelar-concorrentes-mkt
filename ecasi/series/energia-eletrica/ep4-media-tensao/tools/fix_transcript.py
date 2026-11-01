"""Corrige a grafia da transcrição automática (assets/transcript-raw.json -> assets/transcript.json).

Uso: python -I tools/fix_transcript.py
"""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Troca simples, palavra por palavra
FIX = {
    "13.800V.": "13.800 V.",
    "13.800": "13.800 V.",
    "380V": "380 V",
    "NR10,": "NR-10,",
    "NR10": "NR-10",
    "1,38": "1,38",
    "1439": "14039",
    "grupo": "Grupo",
    "ECASE.": "ECASI.",
    "camadas.": "camadas",
    "Antes": "antes",
    "chave?": "chave?",
}

words = json.load(open(os.path.join(BASE, "assets", "transcript-raw.json"), encoding="utf-8"))
out = []
for w in words:
    w = dict(w)
    w["text"] = FIX.get(w["text"], w["text"])
    out.append(w)

json.dump(out, open(os.path.join(BASE, "assets", "transcript.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(" ".join(w["text"] for w in out))
