"""Gera compositions/captions.html a partir de assets/transcript.json.

Uso: python -I tools/build_captions.py
"""
import html
import json
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Correções de grafia da transcrição automática
FIX = {"NR10": "NR-10", "Ecasi.": "ECASI.", "Ecási.": "ECASI."}
MAX_WORDS = 5
MAX_CHARS = 24
PAUSE = 0.15

words = json.load(open(os.path.join(BASE, "assets", "transcript.json"), encoding="utf-8"))
for w in words:
    w["text"] = FIX.get(w["text"], w["text"])

# Agrupa: quebra em fim de frase, pausa >= 150 ms ou limite de palavras/caracteres
groups, cur = [], []
for i, w in enumerate(words):
    if cur:
        chars = len(" ".join(x["text"] for x in cur + [w]))
        gap = w["start"] - cur[-1]["end"]
        if len(cur) >= MAX_WORDS or chars > MAX_CHARS or gap >= PAUSE:
            groups.append(cur)
            cur = []
    cur.append(w)
    if re.search(r"[.?!]$", w["text"]):
        groups.append(cur)
        cur = []
if cur:
    groups.append(cur)

rows, gsap = [], []
for gi, g in enumerate(groups):
    gid = f"cap-g{gi}"
    start = max(0.12, g[0]["start"] - 0.05)
    nxt = groups[gi + 1][0]["start"] - 0.05 if gi + 1 < len(groups) else g[-1]["end"] + 0.6
    end = min(g[-1]["end"] + 0.5, nxt)
    spans = []
    for wi, w in enumerate(g):
        cls = "cap-w is-num" if re.search(r"\d", w["text"]) else "cap-w"
        spans.append(f'<span id="{gid}-w{wi}" class="{cls}">{html.escape(w["text"])}</span>')
        gsap.append(f'tl.to("#{gid}-w{wi}", {{ opacity: 1, duration: 0.08, ease: "none" }}, {w["start"]:.2f});')
    rows.append(f'      <div id="{gid}" class="cap-group"><div class="cap-pill">{" ".join(spans)}</div></div>')
    gsap.insert(len(gsap) - len(g), f'tl.fromTo("#{gid}", {{ opacity: 0, y: 12 }}, {{ opacity: 1, y: 0, duration: 0.18, ease: "power3.out" }}, {start:.2f});')
    gsap.append(f'tl.to("#{gid}", {{ opacity: 0, duration: 0.12, ease: "power2.in" }}, {end - 0.12:.2f});')
    gsap.append(f'tl.set("#{gid}", {{ visibility: "hidden" }}, {end:.2f});')

doc = f"""<template>
  <style>
    #root {{
      position: absolute;
      inset: 0;
      pointer-events: none;
    }}
    .cap-group {{
      position: absolute;
      left: 0;
      right: 0;
      top: 1190px;
      text-align: center;
      opacity: 0;
      overflow: visible;
    }}
    .cap-pill {{
      display: inline-block;
      max-width: 900px;
      padding: 14px 30px 18px;
      border-radius: 16px;
      background: #0b1d3f;
      font-family: Poppins, sans-serif;
      font-weight: 600;
      font-size: 54px;
      line-height: 1.15;
      letter-spacing: -0.01em;
      color: #ffffff;
      box-shadow: 0 16px 36px -18px rgba(11, 29, 63, 0.6);
    }}
    .cap-w {{
      opacity: 0.45;
    }}
    .cap-w.is-num {{
      color: #fb923c;
    }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{chr(10).join(rows)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {chr(10) + "    ".join(gsap)}
    window.__timelines["captions"] = tl;
  </script>
</template>
"""
open(os.path.join(BASE, "compositions", "captions.html"), "w", encoding="utf-8").write(doc)
print(f"{len(groups)} grupos, {len(words)} palavras")
