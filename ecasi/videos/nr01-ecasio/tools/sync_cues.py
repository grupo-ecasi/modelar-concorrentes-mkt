"""Copia tools/cues.json para o objeto C de compositions/world.html e hud.html (entre /*CUES*/ e /*FIM*/)
e ajusta a duração do index.html. Rode depois de tools/fix_transcript.py.

Uso: python tools/sync_cues.py
"""
import json, os, re
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = json.load(open(os.path.join(BASE, "tools", "cues.json"), encoding="utf-8"))
txt = json.dumps(C, ensure_ascii=False)
for f in ["world.html", "hud.html"]:
    p = os.path.join(BASE, "compositions", f); s = open(p, encoding="utf-8").read()
    s = re.sub(r"/\*CUES\*/.*?/\*FIM\*/", lambda m: "/*CUES*/" + txt + "/*FIM*/", s, flags=re.S)
    open(p, "w", encoding="utf-8").write(s)
p = os.path.join(BASE, "index.html"); s = open(p, encoding="utf-8").read()
s = re.sub(r'data-duration="[\d.]+"', f'data-duration="{C["end"]}"', s)
open(p, "w", encoding="utf-8").write(s)
print("cues sincronizados; fim em", C["end"])
