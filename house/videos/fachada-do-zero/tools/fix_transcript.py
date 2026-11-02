"""Corrige a grafia da transcrição automática (assets/transcript.json, in-place; original em transcript-raw.json)."""
import json, os, shutil
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(B, "assets", "transcript.json"); raw = os.path.join(B, "assets", "transcript-raw.json")
if not os.path.exists(raw): shutil.copy(p, raw)
w = json.load(open(raw, encoding="utf-8"))
TROCA = {"cau": "cal", "brocha.": "broxa.", "cál": "cal", "pigm": "pigmento", "seu": "selante", "lanchestica": "estica"}
out = []
i = 0
while i < len(w):
    t = w[i]["text"]
    if t == "de" and i + 1 < len(w) and w[i + 1]["text"].startswith("mãos"):
        out.append({**w[i], "text": "demãos" + w[i + 1]["text"][4:], "end": w[i + 1]["end"]}); i += 2; continue
    out.append({**w[i], "text": TROCA.get(t, t)}); i += 1
json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(" ".join(x["text"] for x in out))
