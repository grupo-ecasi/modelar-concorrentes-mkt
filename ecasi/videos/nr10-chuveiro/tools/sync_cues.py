"""Calcula os tempos das cenas a partir de assets/transcript.json e grava em todas as composições.

Cada cena está presa a uma palavra da narração (tools/cues_spec.json). O resultado vai para
tools/cues.json, para o bloco /*CUES*/ de world.html, hud.html e cta.html, e para as durações do index.html.

Uso: python -I tools/sync_cues.py
"""
import json
import os
import re
import subprocess
import unicodedata

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICE = "assets/narracao-nr10-norm.mp3"


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", s)


words = json.load(open(os.path.join(BASE, "assets", "transcript.json"), encoding="utf-8"))
spec = json.load(open(os.path.join(BASE, "tools", "cues_spec.json"), encoding="utf-8"))
toks = [norm(w["text"]) for w in words]

cues = {"hook": 0.0}
for name, rule in spec.items():
    hits = [i for i, t in enumerate(toks) if t == norm(rule["word"])]
    n = rule.get("n", 1)
    if len(hits) < n:
        raise SystemExit(f"âncora não encontrada: {name} -> '{rule['word']}' #{n}")
    cues[name] = round(words[hits[n - 1] + rule.get("shift", 0)]["start"], 2)

voice_len = float(
    subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", os.path.join(BASE, VOICE)],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
)
cues["end"] = round(max(words[-1]["end"] + 0.9, voice_len + 0.2), 2)

# Ordem cronológica: uma âncora fora de ordem indica erro de transcrição
names = list(cues)
for a, b in zip(names, names[1:]):
    if cues[b] < cues[a]:
        print(f"AVISO: {b} ({cues[b]}) vem antes de {a} ({cues[a]})")

json.dump(cues, open(os.path.join(BASE, "tools", "cues.json"), "w", encoding="utf-8"), indent=2)

block = "/*CUES*/\n    const C = " + json.dumps(cues, indent=6).replace("\n}", "\n    }") + ";\n    /*END-CUES*/"
for f in ("world.html", "hud.html", "cta.html"):
    p = os.path.join(BASE, "compositions", f)
    src = open(p, encoding="utf-8").read()
    src, k = re.subn(r"/\*CUES\*/.*?/\*END-CUES\*/", lambda m: block, src, flags=re.S)
    if k != 1:
        raise SystemExit(f"bloco CUES não encontrado em {f}")
    open(p, "w", encoding="utf-8").write(src)

# index.html: duração total, cena da chamada final e trilhas de áudio
p = os.path.join(BASE, "index.html")
src = open(p, encoding="utf-8").read()


def set_attr(src, el_id, attr, value):
    pat = re.compile(r'(<(?:div|audio)\b[^>]*\bid="' + el_id + r'"[^>]*>)', re.S)
    m = pat.search(src)
    if not m:
        raise SystemExit(f"elemento #{el_id} não encontrado no index.html")
    tag = re.sub(attr + r'="[^"]*"', f'{attr}="{value}"', m.group(1))
    return src[: m.start()] + tag + src[m.end() :]


END = cues["end"]
for el in ("root", "world", "hud", "captions"):
    src = set_attr(src, el, "data-duration", END)
src = set_attr(src, "cta", "data-start", cues["cta"])
src = set_attr(src, "cta", "data-duration", round(cues["loop"] + 0.39 - cues["cta"], 2))
src = set_attr(src, "vo", "data-duration", round(voice_len, 2))
src = set_attr(src, "sfx", "data-duration", END)
open(p, "w", encoding="utf-8").write(src)

print(f"{len(cues)} marcas · fim em {END}s · narração {voice_len:.2f}s")
