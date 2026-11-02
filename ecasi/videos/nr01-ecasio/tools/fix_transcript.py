"""Prepara assets/transcript.json (legendas) e tools/cues.json (tempos dos blocos) a partir de assets/transcript-raw.json.

1. Devolve a pontuação do texto original (assets/narracao.txt) a cada palavra, na ordem.
2. Troca o que a voz fala por extenso pelo que a legenda mostra ("ene erre um" -> "NR-01", "quinhentos ... mil" -> "546 mil").
3. Acha os tempos dos blocos pelas palavras-chave e grava tools/cues.json (o mesmo objeto C de world.html e hud.html).

Uso: python tools/fix_transcript.py
"""
import json
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw = json.load(open(os.path.join(BASE, "assets", "transcript-raw.json"), encoding="utf-8"))
txt = open(os.path.join(BASE, "assets", "narracao.txt"), encoding="utf-8").read().split()

# 1) pontuação: alinhamento sequencial (as palavras do serviço vêm sem pontuação)
norm = lambda s: re.sub(r"[^\wà-ú]", "", s.lower())
w, j = [], 0
for p in raw:
    while j < len(txt) and norm(txt[j]) == "":
        j += 1
    if j < len(txt) and norm(txt[j]) == norm(p["text"]):
        w.append({**p, "text": txt[j]}); j += 1
    else:
        w.append(dict(p))

# 2) troca de trechos falados por extenso (a pontuação do último token é mantida)
TROCAS = [
    ("quinhentos e quarenta e seis mil", "546 mil"), ("dois mil e vinte e cinco", "2025"), ("dois mil e vinte e seis", "2026"),
    ("dezesseis por cento", "16%"), ("ene erre um", "NR-01"), ("pê gê erre", "PGR"), ("ésse tê éfe", "STF"),
    ("dois anos", "2 anos"), ("três pilares", "3 pilares"),
    ("Ecási", "ECASI"),
]
out, i = [], 0
while i < len(w):
    for frase, novo in TROCAS:
        f = frase.split()
        seg = w[i:i + len(f)]
        if len(seg) == len(f) and all(norm(a["text"]) == norm(b) for a, b in zip(seg, f)):
            pont = re.sub(r"^.*?([.,?!:…]*)$", r"\1", seg[-1]["text"])
            out.append({"text": novo + pont, "start": seg[0]["start"], "end": seg[-1]["end"]}); i += len(f); break
    else:
        out.append(w[i]); i += 1
json.dump(out, open(os.path.join(BASE, "assets", "transcript.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


# 3) tempos dos blocos: início da n-ésima ocorrência de uma sequência de palavras
def em(frase, n=1):
    plano = [(norm(sub), k) for k, x in enumerate(out) for sub in x["text"].split()]
    f = [norm(x) for x in frase.split()]
    achou = 0
    for q in range(len(plano) - len(f) + 1):
        if all(plano[q + r][0] == f[r] for r in range(len(f))):
            achou += 1
            if achou == n:
                return round(out[plano[q][1]]["start"], 2)
    raise SystemExit(f"não achei: {frase} ({n})")


C = {
    "promessa": em("E ela se apoia"),
    "problema": em("Antes, o tamanho"),
    "num": next(round(x["start"], 2) for x in out if x["text"].startswith("546")),
    "pct": em("Quase"),
    "psico": em("Por isso"),
    "c1": em("Primeiro pilar"),
    "c1psi": em("e também sobrecarga"),
    "c1inv": em("Tudo entra"),
    "c2": em("Segundo pilar"),
    "c2pgr": em("Inventário e plano"),
    "c3": em("Terceiro pilar"),
    "c3cons": em("A empresa consulta"),
    "mito": em("Mas o STF"),
    "nao": em("Não.", 2),
    "susp": em("Suspendeu, por"),
    "vale": em("A norma continua"),
    "norma": em("E o PGR"),
    "rev": em("A avaliação de riscos"),
    "cta": em("Quer saber"),
    "fale": em("Fale com"),
    "loop": em("Tem gente"),
    # palavras que disparam objetos e etiquetas
    "ruido": em("Ruído,"), "quimico": em("produto químico"), "altura": em("altura,"), "eletr": em("eletricidade"),
    "sobrecarga": em("sobrecarga"), "apoio": em("falta de apoio"), "assedio": em("assédio"),
    "medida": em("uma medida"), "resp": em("um responsável"), "prazo": em("um prazo"),
    "consulta": em("consulta"), "informa": em("informa"), "treina": em("treina"),
    "multas": em("as multas"), "gaveta": em("pra gaveta"), "doisanos": em("2 anos"), "mudar": em("se o trabalho"),
    "loop3": em("confira os 3"),
    "end": round(out[-1]["end"] + 1.2, 2),
}
json.dump(C, open(os.path.join(BASE, "tools", "cues.json"), "w", encoding="utf-8"), ensure_ascii=False)
print(" ".join(x["text"] for x in out))
print(json.dumps(C, ensure_ascii=False))
