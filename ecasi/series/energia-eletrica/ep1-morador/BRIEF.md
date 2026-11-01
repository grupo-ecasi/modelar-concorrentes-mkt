---
workflow: hyperframes-explainer
flow: automation
storyboard: no
message: "Trocar a resistência do chuveiro pode dar choque: 3 camadas antes de encostar (desligar no quadro, conferir, saber parar)"
destination: instagram-reels
aspect: "9:16"
language: pt-BR
length: 83s
angle: concept
---

## Intent

EP1/4 da "Série Energia Elétrica" do Grupo ECASI (plano em `../plano-serie-energia-eletrica.md`), para moradores sem
formação em elétrica. Mesmo molde viral do Reel NR-10: gancho com resposta seca, barra 1-2-3, problema com números,
camadas com número gigante, mito com comparação de escala (resistência de 127 V em 220 V = 3×), norma (NBR 5410),
CTA e fecho em loop. O morador nunca aparece medindo tensão. O eletricista de colete da ECASI (logo nas costas) entra no CTA.

## Assets

- Narração: ElevenLabs (voz "Will"), `assets/narracao-ep1.mp3`, normalizada para -16 LUFS em `assets/narracao-norm.mp3`.
- Efeitos sonoros: biblioteca embutida do media-use (Pixabay Content License), em `assets/sfx/`; trilha pré-mixada em `assets/sfx-track.wav`.
- Logo e símbolo oficiais em `assets/brand/`.

## Customizations

- Design system Grupo ECASI: laranja Segurança do Trabalho, azul-marinho, Poppins + JetBrains Mono.
- Sem música. Efeitos sonoros mais altos que no NR-10: cerca de 3 a 8 dB abaixo da voz no momento da entrada,
  ducking leve e limitador em -3 dBFS (o pico nunca passa o da voz). Conferido com `tools/measure_mix.py`.

## Pipeline (depois de trocar a narração)

1. `ffmpeg -i assets/narracao-ep1.mp3 -af loudnorm=I=-16:TP=-1.5:LRA=11 -ar 48000 -ac 1 assets/narracao-norm.mp3`
2. `npx hyperframes transcribe assets/narracao-norm.mp3 --language pt` e copie `assets/transcript.json` para `assets/transcript-raw.json`
3. `python -I tools/fix_transcript.py` (grafia: disjuntor, micro-ondas, ECASI…)
4. `python -I tools/sync_cues.py` (tempos de todas as cenas, a partir das âncoras de `tools/cues_spec.json`)
5. `python -I tools/build_captions.py`, `python -I tools/build_sfx.py` e `python -I tools/measure_mix.py`
6. `npx hyperframes check`, snapshot e render
