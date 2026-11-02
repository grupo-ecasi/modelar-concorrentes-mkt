---
workflow: hyperframes-explainer
flow: automation
storyboard: no
message: "Terminou o quadro do cliente? Ainda não entrega: 3 camadas antes de entregar (proteção, DR, terra)"
destination: instagram-reels
aspect: "9:16"
language: pt-BR
length: 92s
angle: concept
---

## Intent

EP2/4 da "Série Energia Elétrica" do Grupo ECASI (plano em `../plano-serie-energia-eletrica.md`), para eletricistas
residenciais. Mesmo molde viral do EP1: gancho com resposta seca ("Ainda não."), barra 1-2-3 (proteção, DR, terra),
problema com números (PVC a 70 °C, fuga de mA, carcaça sem terra), camadas com número gigante, mito com comparação
de escala (disjuntor de 40 A em cabo de 24 A = 1,7×), norma (NBR 5410 + NR-10), CTA do Treinamento NR-10 e loop.
O protagonista é o eletricista do Grupo ECASI (v2: uniforme antichama azul-marinho com faixas refletivas e logo grande nas costas, capacete com jugular, óculos e luvas isolantes; rig do reboco-novo com IK de 2 ossos). Ele nunca mexe dentro
do quadro energizado: aperta o botão T pela frente e desliga o geral antes de testar com o detector. A troca do
disjuntor por um de 40 A (prática errada) acontece sozinha, sem o personagem da marca.

## Assets

- Narração: ElevenLabs (voz "Will"), `assets/narracao-ep2.mp3`, normalizada para -16 LUFS em `assets/narracao-norm.mp3`.
- Efeitos sonoros: biblioteca embutida do media-use (Pixabay Content License), em `assets/sfx/`; trilha pré-mixada em `assets/sfx-track.wav`.
- Logo e símbolo oficiais em `assets/brand/`.

## Customizations

- Design system Grupo ECASI: laranja Segurança do Trabalho, azul-marinho, Poppins + JetBrains Mono.
- Sem música. Efeitos sonoros mais altos que no NR-10: cerca de 3 a 8 dB abaixo da voz no momento da entrada,
  ducking leve e limitador em -3 dBFS (o pico nunca passa o da voz). Conferido com `tools/measure_mix.py`.

## Pipeline (depois de trocar a narração)

1. `ffmpeg -i assets/narracao-ep2.mp3 -af loudnorm=I=-16:TP=-1.5:LRA=11 -ar 48000 -ac 1 assets/narracao-norm.mp3`
2. `npx hyperframes transcribe assets/narracao-norm.mp3 --language pt` e copie `assets/transcript.json` para `assets/transcript-raw.json`
3. `python -I tools/fix_transcript.py` (grafia: disjuntor, ampères, NR-10, ECASI…)
4. `python -I tools/sync_cues.py` (tempos de todas as cenas, a partir das âncoras de `tools/cues_spec.json`)
5. `python -I tools/build_captions.py`, `python -I tools/synth_sfx.py` (efeitos de energia), `python -I tools/build_sfx.py` e `python -I tools/measure_mix.py`
6. `npx hyperframes check`, snapshot e render (`--quality delivery`)
7. `python -I tools/master.py renders/<bruto>.mp4 renders/<final>.mp4` (master a -14 LUFS / -1 dBTP)
