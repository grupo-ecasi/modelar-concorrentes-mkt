"""Alinha o texto do roteiro (assets/narracao.txt) aos tempos de uma transcrição automática da voz definitiva.

A transcrição escreve "NR1", "2025", "546", "PGR"; o roteiro tem tudo por extenso ("ene erre um"...).
Este script expande essas formas, casa as palavras (difflib) e interpola as que sobrarem.
Saída: assets/transcript-raw.json com as palavras do roteiro e os tempos da voz, pronto para tools/fix_transcript.py.

Uso: python tools/alinhar.py <transcript-da-voz.json>   (formato do `hyperframes transcribe`: [{text, start, end}])
"""
import difflib
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
norm = lambda s: re.sub(r"[^\wà-ú%]", "", s.lower())

EXPANDE = {
    "nr1": "ene erre um", "nr01": "ene erre um", "2025": "dois mil e vinte e cinco", "2026": "dois mil e vinte e seis",
    "546": "quinhentos e quarenta e seis", "16%": "dezesseis por cento", "pgr": "pê gê erre", "stf": "ésse tê éfe",
    "para": "pra", "ecasi": "ecási", "3": "três", "2": "dois",
}

voz = json.load(open(sys.argv[1], encoding="utf-8"))
if isinstance(voz, dict):
    voz = voz.get("words", [])
T = []  # (palavra falada normalizada, início, fim)
for w in voz:
    n = norm(w["text"])
    if not n:
        continue
    partes = EXPANDE.get(n, n).split()
    d = (w["end"] - w["start"]) / len(partes)
    for i, p in enumerate(partes):
        T.append((norm(p), w["start"] + i * d, w["start"] + (i + 1) * d))

S = [x for x in open(os.path.join(BASE, "assets", "narracao.txt"), encoding="utf-8").read().split() if norm(x)]
Sn = [norm(x) for x in S]
tempos = [None] * len(S)
sm = difflib.SequenceMatcher(a=Sn, b=[t[0] for t in T], autojunk=False)
for a, b, n in sm.get_matching_blocks():
    for k in range(n):
        tempos[a + k] = (T[b + k][1], T[b + k][2])
casadas = sum(1 for t in tempos if t)

# interpola as que não casaram entre as vizinhas
for i in range(len(S)):
    if tempos[i]:
        continue
    j = i
    while j < len(S) and not tempos[j]:
        j += 1
    ini = tempos[i - 1][1] if i > 0 else 0.0
    fim = tempos[j][0] if j < len(S) else voz[-1]["end"]
    passo = (fim - ini) / (j - i)
    for k in range(i, j):
        tempos[k] = (ini + (k - i) * passo, ini + (k - i + 1) * passo)

out = [{"text": re.sub(r"[.,?!:…]+$", "", s), "start": round(a, 3), "end": round(b, 3)} for s, (a, b) in zip(S, tempos)]
json.dump(out, open(os.path.join(BASE, "assets", "transcript-raw.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{casadas}/{len(S)} palavras casadas direto; o resto interpolado. Fim em {out[-1]['end']:.2f} s")
