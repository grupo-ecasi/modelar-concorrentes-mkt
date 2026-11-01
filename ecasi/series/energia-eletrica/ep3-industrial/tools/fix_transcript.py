"""Corrige a grafia da transcrição automática (assets/transcript-raw.json -> assets/transcript.json).

Uso: python -I tools/fix_transcript.py
"""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Troca simples, palavra por palavra
FIX = {
    "380V,": "380 V,",
    "540V": "540 V",
    "Emeça": "Meça",
    "NR10": "NR-10",
    "MR10": "NR-10",
    "MR12": "NR-12",
    "MR1": "NR-1",
    "grupo": "Grupo",
    "ECASE.": "ECASI.",
    "Bloquear": "Bloquear.",
    "apagou.": "apagou,",
    "Então,": "então",
}

words = json.load(open(os.path.join(BASE, "assets", "transcript-raw.json"), encoding="utf-8"))
out = []
for w in words:
    w = dict(w)
    w["text"] = FIX.get(w["text"], w["text"])
    out.append(w)

json.dump(out, open(os.path.join(BASE, "assets", "transcript.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(" ".join(w["text"] for w in out))
