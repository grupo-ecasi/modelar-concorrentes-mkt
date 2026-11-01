# Plano — Série "Energia Elétrica" do Grupo ECASI (4 Reels no molde viral do NR-10)

## Contexto

O Grupo ECASI quer uma série educativa de segurança elétrica com 4 públicos: morador, eletricista residencial, eletricista industrial e média tensão. O texto de briefing traz roteiros de 3 a 5 minutos em formato institucional. A decisão é **manter o tema e o público de cada vídeo, mas usar a fórmula viral do Reel NR-10 do chuveiro** (`video-nr10-chuveiro/`, baseada na decupagem do @raiox.tec em `decupagem-raiox-chuveiro.md`).

Decisões já tomadas:
- **4 vídeos**, produzidos um de cada vez (aprovação ao final de cada um).
- **Um plano mestre** (este arquivo) com o molde comum e uma seção por vídeo. É melhor que 4 planos soltos porque os 4 vídeos usam o mesmo esqueleto, os mesmos scripts e o mesmo personagem.
- Formato Reel vertical 9:16, **60 a 90 s** (não 3 a 5 min), porque a fórmula viral depende de ritmo.
- **Personagem:** eletricista low-poly com colete de verdade. No vídeo 1, o protagonista é o morador (sem colete), e o eletricista de colete entra no CTA "chame um eletricista".
- **Efeitos sonoros mais altos** que no NR-10, sem passar da narração.

---

## 1. Molde viral (igual ao NR-10)

```
[0–4s]   GANCHO: situação comum + pergunta. Resposta seca: "Não." / "Pode."  (vinheta vermelha)
[4–8s]   PROMESSA: "Existem 3 camadas…". A barra 1-2-3 aparece no topo
[8–25s]  PROBLEMA: como o perigo funciona, com 2 ou 3 números na tela (raio-x do objeto)
[25–60s] CAMADAS 1, 2 e 3: número gigante + chip da barra acende + cards e callouts presos aos objetos
[60–72s] MITO + "momento uau": comparação de escala com número exato (barra grande × quadradinho)
[72–80s] NORMA (tags com o item) + CTA Grupo ECASI (card com logo + WhatsApp)
[80–85s] LOOP: volta ao plano do início, e a última frase emenda na primeira
```

Interface (reaproveitada de `video-nr10-chuveiro/compositions/hud.html`): barra 1-2-3, card de dado em fonte mono, callouts com linha guia, número gigante de seção, contadores animados, vinheta vermelha, legenda palavra por palavra (`captions.html`), card final (`cta.html`). Novidade: selo **"Série Energia Elétrica · EP X/4"** no canto superior direito, para ligar os episódios.

Texto: tom técnico, direto e humano, citando a norma e sem usar medo como argumento. Números e siglas escritos por extenso no texto da voz.

---

## 2. Melhorias que valem para os 4 vídeos

### 2.1 Eletricista com colete (em `compositions/world.html`, função `makeWorker()`)
Hoje o colete é uma caixa laranja sobre o tronco (linhas 470–480) e quase não se lê como colete. Novo modelo:
- Colete aberto na frente (dois painéis laterais com a camisa azul-marinho aparecendo no meio em "V"), alças nos ombros e cava sem manga.
- Faixas refletivas: 2 horizontais + 2 verticais tipo suspensório (padrão de colete de eletricista).
- Bolso no peito com uma caneta/detector e **símbolo ECASI nas costas** (textura de `assets/brand/simbolo-ecasi.png`).
- Cinto de ferramentas com alicate e chave isolada (cabo amarelo).
- EPI por episódio: EP2 capacete + óculos; EP3 + luvas isolantes e roupa FR; EP4 + protetor facial e luva isolante de AT.
- Morador do EP1: camiseta, bermuda e chinelo (sem EPI), para contrastar com o eletricista do CTA.

### 2.2 Efeitos sonoros mais altos (em `tools/build_sfx.py`)
No NR-10, os efeitos ficaram uns 24 LU abaixo da voz: a trilha seca sai com pico em −6 dBFS, o sidechain abaixa mais 5 dB quando a voz fala e o limitador corta em 0,5. Mudanças:
- Pico da trilha seca em −1 dBFS; ducking mais leve (ratio 2, cerca de 3 dB); limitador em 0,8.
- Meta: o efeito no instante da entrada fica **8 a 10 dB abaixo da voz** (loudness de curto prazo) e o pico nunca passa do pico da voz menos 2 dB.
- Novo `tools/measure_mix.py`: mede com ffmpeg (`ebur128`/`astats`) a voz e a trilha de efeitos em cada evento e avisa se algum passar da voz. Com isso o volume vira número conferido, não chute.
- Novos sons elétricos da biblioteca do `/media-use` (faísca/zap no perigo, clique de cadeado, "tum" de disjuntor), com crédito em `assets/sfx/CREDITS.md`.

### 2.3 Base de projeto
Cada vídeo é um projeto HyperFrames próprio, copiado de `video-nr10-chuveiro/` (sem `renders/`, `.hyperframes/` e assets de voz):
- `video-serie-ep1-morador/`, `video-serie-ep2-residencial/`, `video-serie-ep3-industrial/`, `video-serie-ep4-media-tensao/`
- Reaproveitados como estão: `tools/fix_transcript.py`, `tools/sync_cues.py`, `tools/build_captions.py`, `compositions/captions.html`, `compositions/cta.html` (só troca o texto), `hud.html` (troca cards e chips).
- Reescrito por vídeo: cenário 3D de `world.html`, `tools/cues_spec.json` (âncoras nas palavras da narração), lista `EVENTS` de `build_sfx.py`, `BRIEF.md`.
- Ajustes obrigatórios ao copiar (senão o projeto quebra sem avisar):
  - `meta.json` (`id`, `name`) e `package.json` (`name`).
  - Caminho da voz: `tools/build_sfx.py:130` e `tools/sync_cues.py:15` (hoje `narracao-nr10-norm.mp3`). Passa a vir de uma constante única por projeto.
  - `index.html`: `src` da voz, todos os `data-duration` (90.33 / 89.55) e o `data-start` do CTA (81.75), recalculados pela duração da nova narração.
  - Dicionários de grafia em `fix_transcript.py` e `build_captions.py` (`FIX`): incluir os termos do episódio (DR, DPS, NBR 5410, PIE, SEP, kV…).
- Logo ECASI nas costas do colete: textura carregada **antes** de montar a cena e registrar a timeline (ou desenhada de forma síncrona em canvas), para não sumir nem piscar nos primeiros quadros do render. Conferir com snapshot em t=0 e num quadro com o boneco de costas.

---

## 3. Os 4 vídeos

> Os números abaixo são o rascunho técnico. Cada roteiro sai com a seção "Fontes" para um técnico da ECASI revisar antes da gravação da voz.

### EP1 — Morador · "Vai trocar a resistência do chuveiro sozinho?"
- **Cenário:** banheiro de casa, quadro de luz no corredor, morador de camiseta e chinelo.
- **Gancho:** "Fechou o chuveiro e vai trocar a resistência. Pode levar choque? Pode."
- **Problema:** os fios da parede continuam com 127 ou 220 V; o chuveiro puxa uns **34 A** (7.500 W ÷ 220 V); mão molhada + 10 mA / 50 mA.
- **Camadas:** 1 DESLIGAR no quadro (o disjuntor certo, não o registro) · 2 CONFERIR (resistência da mesma tensão e modelo; fio sem marca de queimado) · 3 SABER PARAR (não sabe qual é o circuito ou não tem como confirmar a ausência de tensão? Para aqui e chama um eletricista). O morador **nunca** aparece medindo tensão: a verificação é de pessoa competente, e o detector só aparece na mão do eletricista do CTA.
- **Mito + uau:** "resistência é tudo igual": uma de 127 V ligada em 220 V dá **3× a potência** ((220÷127)² ≈ 3) e queima na hora.
- **Norma:** NBR 5410 exige circuito exclusivo e DR de 30 mA para o chuveiro.
- **CTA:** entra o eletricista de colete ECASI, com o detector na mão: "Na dúvida, chame um eletricista qualificado." (confirmar comigo antes: CTA de serviço ou só "segue o Grupo ECASI").
- **Loop:** "Vai trocar a resistência? Confira as três camadas antes."

### EP2 — Eletricista residencial · "Terminou o quadro. Pode entregar?"
- **Cenário:** quadro de distribuição residencial em raio-x (cabos, barramento, DR, DPS).
- **Gancho:** "Você terminou o quadro do cliente. Já pode entregar? Ainda não."
- **Problema:** sobrecarga esquenta o cabo (PVC até 70 °C), fuga de corrente, falta de terra; desenergização da NR-10 antes de tudo (gancho para o episódio NR-10 já publicado).
- **Camadas:** 1 PROTEÇÃO (disjuntor escolhido pelo cabo, não pela carga) · 2 DR (30 mA em banheiro, cozinha, lavanderia e área externa + teste no botão T) · 3 TERRA (aterramento, DPS e circuitos identificados).
- **Mito + uau:** "disjuntor desarmando? Põe um maior": cabo de 2,5 mm² aguenta uns **24 A** (embutido); disjuntor de 40 A deixa passar **1,7×** isso sem desarmar. Barra 40 A × 24 A.
- **Norma:** NBR 5410 + NR-10 (procedimento de desenergização, curso básico de 40 h).
- **CTA:** "Treinamento NR-10 · Grupo ECASI".

### EP3 — Eletricista industrial · "Desligou o inversor. Já pode abrir?"
- **Cenário:** chão de fábrica com motor, inversor de frequência e painel de comando; multibloqueio com vários cadeados.
- **Gancho:** "Você desligou o inversor do motor. Já pode abrir o painel? Não."
- **Problema:** 380 / 440 V; arco elétrico (energia incidente); partida inesperada; **energia armazenada**: o barramento CC do inversor fica em uns **540 V** (380 × √2) ou **620 V** (440 V) por minutos depois de desligar.
- **Camadas:** 1 PLANEJAR (APR, permissão de trabalho, diagrama atualizado) · 2 BLOQUEAR (todas as fontes; cada pessoa com seu cadeado na garra de multibloqueio) · 3 TESTAR E DESCARREGAR (esperar o tempo do fabricante, medir 0 V no barramento CC, tentativa de partida).
- **Mito + uau:** "750 V é alta tensão? Não, pela NR-10 ainda é baixa tensão (até 1.000 V CA)… e é **6×** a tomada de 127 V" (contra 220 V seria 3,4×; dizer a tensão de referência na fala e na tela). Contador do barramento CC caindo de 620 V até 0 V.
- **Norma:** NR-10 (PIE para carga instalada acima de 75 kW), NR-12, NR-01 (PGR). Tags: `PIE > 75 kW` · `APR / PT` · `NR-12 bloqueio`.
- **CTA:** "Treinamento NR-10 e PIE · Grupo ECASI".

### EP4 — Média tensão / SEP · "Abriu a chave da cabine. Pode encostar?"
- **Cenário:** cabine primária com cubículos, chave seccionadora, transformador e gerador de emergência; equipe de 2 pessoas com roupa FR.
- **Gancho:** "A seccionadora da cabine está aberta. Já pode encostar no barramento? Não."
- **Problema:** **13.800 V**: a NR-10 chama de alta tensão tudo acima de 1.000 V CA (13,8×); o arco pula sem encostar. Zonas da NR-10 para a faixa de 10 a 15 kV: risco **0,38 m** e controlada **1,38 m**, desenhadas no chão (conferir no texto vigente da NR-10 o número do anexo antes de pôr na tela).
- **Camadas:** 1 AUTORIZAR (ordem de serviço, equipe de no mínimo 2, curso SEP, plano de resgate) · 2 DESENERGIZAR E TESTAR (manobra pelo procedimento; detector de AT no bastão, testado antes) · 3 ATERRAR (conjunto de aterramento temporário dos dois lados + zonas sinalizadas).
- **Mito + uau:** "abriu a chave, tá sem energia": um gerador ligado na baixa pode **voltar pelo transformador** e devolver 13.800 V à cabine (380 V → 13.800 V = **36×**). Animação do retorno de energia.
- **Norma:** NR-10 (alta tensão, Anexo I, curso complementar SEP), NBR 14039, exigências da concessionária.
- **CTA:** "Treinamento NR-10 SEP · Grupo ECASI".

---

## 4. Passo a passo de cada vídeo (repetir para EP1, EP2, EP3, EP4)

1. **Roteiro:** eu escrevo `narracao-serie-epX-<tema>.md` (texto para o ElevenLabs com voz "Will", tabela fala × tela e fontes), no formato de `narracao-nr10-chuveiro.md`. Você revisa e pede ajustes.
2. **Voz:** você gera o MP3 no ElevenLabs e salva na pasta do projeto. Eu normalizo para −16 LUFS.
3. **Projeto:** copio a base do NR-10 e monto o cenário 3D, o personagem com colete e os cards (carregando antes as skills `/hyperframes`, `/hyperframes-core` e `/hyperframes-animation`).
4. **Sincronia:** `npx hyperframes transcribe` → `fix_transcript.py` → `sync_cues.py` → `build_captions.py` → `build_sfx.py` → `measure_mix.py`.
5. **Conferência:** `npx hyperframes check`, snapshots nos momentos-chave (gancho, cada camada, mito, CTA, loop) e eu olho os quadros antes de renderizar.
6. **Render + entrega:** MP4 em `renders/`, capa 1080×1920 e `legenda-instagram-seo.md` (CTA de palavra-chave, 3 camadas em texto, mito, fontes, 5 hashtags, texto alternativo).
7. **Aprovação:** você assiste e aprova. Só depois começamos o próximo episódio. O EP1 também valida o colete novo e o volume dos efeitos para a série toda.

## 5. Verificação

- `npm run check` sem erros em cada projeto.
- Snapshots em 6 a 8 tempos: barra 1-2-3 acende no tempo certo, callouts presos aos objetos, legenda sem cobrir cards, colete legível de frente e de costas.
- `measure_mix.py`: nenhum efeito passa da voz; diferença no evento entre 8 e 10 dB.
- Último quadro igual ao primeiro (loop).
- Revisão técnica dos números (seção "Fontes" de cada roteiro) por um técnico da ECASI antes de publicar.

## Começamos pelo EP1 (morador)
- Passo 0: salvar este plano no projeto, em `C:\app.Modelar-Concorrentes-MKT\plano-serie-energia-eletrica.md`.
- Primeiro entregável: `narracao-serie-ep1-morador.md` para você revisar e gerar a voz.
