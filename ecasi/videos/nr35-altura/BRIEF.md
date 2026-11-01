---
workflow: hyperframes-explainer
flow: automation
storyboard: no
message: "Só o cinto não basta: a NR-35 organiza a proteção em 3 camadas (evitar, eliminar, reduzir)"
destination: instagram-reels
aspect: "9:16"
language: pt-BR
length: 90s
angle: concept
---

## Intent

Reel de motion graphics 3D low-poly sobre NR-35 (trabalho em altura), no formato do @raiox.tec:
barra 1-2-3, cards de dado, callouts presos aos objetos, legenda palavra por palavra e fecho em loop.

## Assets

- Narração: ElevenLabs (voz "Will"), `assets/narracao-nr35.mp3`, normalizada para -16 LUFS em `assets/narracao-nr35-norm.mp3`.
- Logo oficial: `assets/brand/logo-fundo-claro.png` (design system Grupo ECASI).

## Customizations

- Design system Grupo ECASI: laranja Segurança do Trabalho, azul-marinho, Poppins + JetBrains Mono.
- Gancho suavizado ("Só o cinto basta? Não."), porque a marca não usa medo como argumento.
- Sem música, só a voz. Sem a Esmeralda na chamada final (só logo + WhatsApp).

## Notes

- Tempos de todas as cenas vêm de `assets/transcript.json` (Parakeet), no bloco `/*CUES*/` de `world.html` e `hud.html`.
- Legendas geradas por `python -I tools/build_captions.py`.
