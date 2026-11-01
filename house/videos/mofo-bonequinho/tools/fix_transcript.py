"""Corrige a grafia da transcrição automática (assets/transcript-raw.json -> assets/transcript.json).

Uso: python -I tools/fix_transcript.py
"""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Troca simples, palavra por palavra
FIX = {
    "1245,": "13245,",
    "house": "House",
    "pinturas.": "Pinturas.",
    "1.": "1:",
    "2.": "2:",
    "3.": "3:",
    "Infiltração,": "Infiltração,",
}

words = json.load(open(os.path.join(BASE, "assets", "transcript-raw.json"), encoding="utf-8"))
out = []
for i, w in enumerate(words):
    w = dict(w)
    w["text"] = FIX.get(w["text"], w["text"])
    # "passa de uns 70%": a transcrição ouviu "um"
    if w["text"] == "um" and i + 1 < len(words) and words[i + 1]["text"].startswith("70"):
        w["text"] = "uns"
    out.append(w)

json.dump(out, open(os.path.join(BASE, "assets", "transcript.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(" ".join(w["text"] for w in out))
