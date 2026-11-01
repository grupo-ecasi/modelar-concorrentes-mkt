---
workflow: hyperframes-explainer
flow: automation
storyboard: no
message: "Desligou o disjuntor não basta: a NR-10 exige 3 camadas antes de encostar no fio (bloquear, testar, aterrar)"
destination: instagram-reels
aspect: "9:16"
language: pt-BR
length: 90s
angle: concept
---

## Intent

Reel de motion graphics 3D low-poly sobre NR-10 (desenergização para trocar a resistência do chuveiro do vestiário),
no mesmo molde do Reel NR-35 e da decupagem do @raiox.tec: barra 1-2-3, cards de dado, callouts presos aos objetos,
raio-x do chuveiro, legenda palavra por palavra e fecho em loop. Mito: disjuntor de 1 polo deixa a F2 com 127 V.

## Assets

- Narração: ElevenLabs (voz "Will"), `assets/narracao-nr10.mp3`, normalizada para -16 LUFS em `assets/narracao-nr10-norm.mp3`.
- Efeitos sonoros: biblioteca embutida do media-use (Pixabay Content License), em `assets/sfx/`; trilha pré-mixada em `assets/sfx-track.wav`.
- Logo oficial: `assets/brand/logo-fundo-claro.png` (design system Grupo ECASI).

## Customizations

- Design system Grupo ECASI: laranja Segurança do Trabalho, azul-marinho, Poppins + JetBrains Mono.
- Sem música. Efeitos sonoros nas entradas das animações, ~24 LU abaixo da voz e abaixados por sidechain quando ela fala.

## Pipeline (depois de trocar a narração)

1. `npx hyperframes transcribe assets/narracao-nr10.mp3 --language pt` e copie para `assets/transcript-raw.json`
2. `python -I tools/fix_transcript.py` (grafia: disjuntor, NR-10, Luva, ECASI…)
3. `python -I tools/sync_cues.py` (tempos de todas as cenas, a partir das âncoras de `tools/cues_spec.json`)
4. `python -I tools/build_captions.py` e `python -I tools/build_sfx.py`
5. `npx hyperframes check`, snapshot e render
