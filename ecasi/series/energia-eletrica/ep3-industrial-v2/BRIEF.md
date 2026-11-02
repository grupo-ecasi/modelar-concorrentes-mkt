---
workflow: hyperframes-explainer
flow: automation
storyboard: no
message: "Desligou o inversor? Ainda não abre: 3 camadas antes de abrir (planejar, bloquear, testar)"
destination: instagram-reels
aspect: "9:16"
language: pt-BR
length: 100s
angle: concept
---

## Intent

EP3/4 da "Série Energia Elétrica" do Grupo ECASI (plano em `../plano-serie-energia-eletrica.md`), para eletricistas
e técnicos de manutenção industrial. Mesmo molde do EP1 e do EP2: gancho com resposta seca ("Não."), barra 1-2-3
(planejar, bloquear, testar), problema com números (barramento CC do inversor em 540 V = 380 × √2, partida remota
inesperada, arco elétrico), camadas com número gigante, mito ("display apagou, então descarregou?") com o contador do
barramento ainda em centenas de volts e a régua de baixa tensão da NR-10, norma (NR-10 PIE > 75 kW, NR-12, NR-01 PGR),
CTA do Treinamento NR-10 e loop. O protagonista é o eletricista do Grupo ECASI (v2: uniforme antichama azul-marinho com faixas refletivas e logo grande nas costas, capacete com jugular, óculos e
luvas isolantes; rig do reboco-novo com IK de 2 ossos); um colega da manutenção (uniforme cinza, capacete azul) põe o próprio cadeado. O eletricista só abre o painel depois
das 3 camadas; a partida inesperada vem do CLP, sem pessoa. No mito a porta fecha de novo e a cena funciona como
"replay" ilustrativo.

## Assets

- Narração: ElevenLabs (voz "Will"), `assets/narracao-ep3.mp3`, normalizada para -16 LUFS em `assets/narracao-norm.mp3`.
- Efeitos sonoros: biblioteca embutida do media-use (Pixabay Content License), em `assets/sfx/`; trilha pré-mixada em `assets/sfx-track.wav`.
- Logo e símbolo oficiais em `assets/brand/`.

## Customizations

- Design system Grupo ECASI: laranja Segurança do Trabalho, azul-marinho, Poppins + JetBrains Mono.
- Sem música. Efeitos sonoros mais altos que no NR-10: cerca de 3 a 8 dB abaixo da voz no momento da entrada,
  ducking leve e limitador em -3 dBFS (o pico nunca passa o da voz). Conferido com `tools/measure_mix.py`.

## Pipeline (depois de trocar a narração)

1. `ffmpeg -i assets/narracao-ep3.mp3 -af loudnorm=I=-16:TP=-1.5:LRA=11 -ar 48000 -ac 1 assets/narracao-norm.mp3`
2. `npx hyperframes transcribe assets/narracao-norm.mp3 --language pt` e copie `assets/transcript.json` para `assets/transcript-raw.json`
3. `python -I tools/fix_transcript.py` (grafia: disjuntor, ampères, NR-10, ECASI…)
4. `python -I tools/sync_cues.py` (tempos de todas as cenas, a partir das âncoras de `tools/cues_spec.json`)
5. `python -I tools/build_captions.py`, `python -I tools/build_sfx.py` e `python -I tools/measure_mix.py`
6. `npx hyperframes check`, snapshot e render
