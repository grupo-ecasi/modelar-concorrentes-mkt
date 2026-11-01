# Revisão — House · Mofo (31/10/2026)

**Base:** projeto do EP1 da Série Energia Elétrica (`../video-serie-ep1-morador`), com o mesmo pipeline:
- transcrição → `tools/fix_transcript.py` → `tools/sync_cues.py` (âncoras em `tools/cues_spec.json`)
- `tools/build_captions.py` → `tools/build_sfx.py` → `tools/measure_mix.py`

**Check:** ok. Os avisos restantes são os mesmos do EP1: fromTo repetido nos números de seção, arquivos grandes e o relógio do Three.js medindo o DOM.

**Mixagem:** efeitos com mediana de -5,9 dB abaixo da voz, faixa de -10,7 a -3,1 dB, nenhum pico acima da voz (meta: -8 a -3 dB).

**Narração:** `assets/narracao-mofo.wav`, normalizada em -16 LUFS (`assets/narracao-norm.mp3`), 86,5 s. Duração do vídeo: 87,3 s.

**Quadros conferidos:** 0; 2,8; 5,5; 9; 15,6; 18,8; 21,5; 24,3; 26; 28,6; 34; 36,5; 40,2; 44,5; 48,5; 52; 55,5; 60,6; 65,8; 72; 78; 82,5; 85,5 s.

**Corrigido nesta revisão**
- A câmera ficava perto demais nas cenas do banheiro e o bonequinho ocupava a tela toda. Os planos foram reenquadrados.
- O corte da parede (raio-x) era largo para o vertical. Agora é mais estreito e mais alto, com o topo abaixo dos cards.
- O morador ficava de braços erguidos a cena toda. Agora baixa o rolo depois de pintar e sai na camada 1.
- O pintor pintava até a norma. Agora para no mito.
- O número gigante da seção tinha pouco contraste sobre o teto cinza. Ganhou um fundo claro.
- O card "Só esconde" e as etiquetas "tinta com antimofo" e "o fungo volta" ficavam pouco tempo na tela.
