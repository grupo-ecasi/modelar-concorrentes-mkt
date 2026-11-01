# Plano: refazer EP2, EP3 e EP4 da Série Energia Elétrica no padrão "reboco novo"

## Contexto
Os EP2–4 (`ecasi\series\energia-eletrica\`) foram entregues em 31/10 com o boneco antigo: boxes, sem cotovelo/joelho, cabeça sem rosto, IK de 1 osso (`aimArm`), sem tone mapping, fundo liso, energia feita de bolinhas e um icosaedro de "arco". O vídeo `house\videos\reboco-novo\` elevou a régua (`makePerson` com cápsulas, rosto, piscada, IK de 2 ossos `reach`, ACES, PCFSoft, céu em shader, texturas procedurais). O pedido é refazer os 3 episódios nesse nível, um por vez, com aprovação entre eles: o eletricista ECASI com roupa de eletricista e logo nas costas, energia animada o mais realista possível nos objetos (quadro, painel/inversor, cabine/poste) e áudio impecável.

## Diagnóstico já feito
- Narrações TTS (ElevenLabs "Will") estão limpas: piso nas pausas de -68 a -76 dB RMS, integrado -16,7/-16,9 LUFS. Não precisam de denoise; reaproveitar mantém `cues_spec.json`, `sync_cues.py` e legendas válidos.
- Não há bloom/pós-processamento em nenhum projeto. Three.js 0.184.0 (jsdelivr), GSAP 3.14.2, hyperframes@0.8.217.
- `C:\Editor.Videos` (sem git) tem ferramentas aproveitáveis, sem chaves no código.

## Decisões (31/10/2026)
- Narração: **reaproveitar** os MP3 atuais (polimento leve opcional com A/B).
- Uniforme: **antichama azul-marinho** de manga longa (camisa + calça), faixas refletivas, logo ECASI grande nas costas, capacete com jugular, óculos, luvas isolantes, botina, cinto de ferramentas. Sem colete.
- EP4: **abre no poste externo** (céu do reboco, isoladores, chave fusível) **e entra na cabine primária** para a manobra.
- Versões: pastas **`-v2`**, antigas mantidas; na "serie eletrica insta" os arquivos novos entram com sufixo `v2`.

## Abordagem (EP2 completo; EP3 e EP4 como diferenças)

### 1. Projeto novo por episódio
`ecasi\series\energia-eletrica\ep2-residencial-v2\` copiado do EP2 atual (mantém roteiro, MP3, `cues_spec.json`, transcript, tools). Antigo fica intacto.

### 2. Personagem: portar o rig do reboco-novo
De `house\videos\reboco-novo\compositions\world.html`:
- `makePerson` (L756-904), `reach` IK 2 ossos (L932-966), `animateBody`/`swingArms` (L968-990), renderer ACES + PCFSoft (L144-151), helpers `mat/smooth/canvasTex/textTex` (L190-301).
- Nova função `makeElectrician(opts)` sobre `makePerson`: uniforme NR-10 antichama azul-marinho de manga longa (camisa + calça, sem colete), faixas refletivas em braços/tronco/pernas, **logo ECASI grande nas costas** (textura `assets\brand\simbolo-ecasi.png` + "ECASI" via `textTex`) e pequeno no peito, capacete classe B com aba e jugular, óculos, luvas isolantes (cor por classe), botina, cinto com porta-ferramentas, crachá. Opções: `visor` (EP4), cores do colega.
- Substituir `aimArm` por `reach` em todas as ações (mãos com cotovelo dobrado, polo correto).
- Câmera de lado quando a mão toca o objeto (lição do reboco).

### 3. Cenários mais próximos do real (procedural, sem modelos externos)
- **EP2 residencial:** quadro de embutir com porta metálica, espelho/contraespelho, trilho DIN, disjuntores com alavanca, DR com botão T, DPS com janela verde/vermelha, barramentos N/PE com parafusos, cabos coloridos (fase preto/vermelho, N azul, PE verde-amarelo) com curvatura real, etiquetas; área de serviço com azulejo, tomada, lava-roupas.
- **EP3 industrial:** galpão com estrutura metálica, iluminação high-bay, CCM com várias colunas, inversor com display e LEDs, barramento CC com capacitores, chave geral com cadeados/etiquetas LOTO, CLP, motor + bomba, piso epóxi com faixas.
- **EP4 média tensão:** abertura externa — rua com poste de concreto duplo T, cruzeta, isoladores de porcelana em saias, chave fusível, para-raios, transformador no poste, ramal de entrada, céu em shader, sol e nuvens do reboco; corte para dentro da cabine primária — chaves seccionadoras com facas, barramento, transformador com aletas e buchas, gerador/QGBT, aterramento temporário com grampos, bastão de manobra com detector, cones e fita zebrada. O mito (gerador devolvendo 13,8 kV) fecha com a energia subindo de volta até o poste lá fora.
- Texturas procedurais (`canvasTex`) para metal escovado, pintura epóxi, porcelana, concreto.

### 4. Energia (núcleo do pedido)
Tudo determinístico e seguro para seek (função de `t`, sem estado acumulado):
- **Bloom seletivo:** `EffectComposer` + `RenderPass` + `UnrealBloomPass` + `OutputPass` de `three@0.184.0/examples/jsm` (mesma CDN/versão), camada só para emissivos; SMAA/FXAA. Nada temporal.
- **Corrente nos cabos:** tubo emissivo com shader de "fluxo" (uv.x - t·v) em vez de bolinhas; intensidade proporcional à corrente (sobrecarga → laranja/vermelho + calor/fumaça).
- **Arco elétrico:** polilinha ramificada com jitter por semente `floor(t*fps/2)`, núcleo branco + halo azul, PointLight piscando, flash de tela, fumaça e metal derretido.
- **Faíscas:** balística fechada (gravidade, quique no piso) com rastros, como no EP3, ampliada.
- **Fuga para a carcaça/choque:** "aura" pulsante na carcaça, caminho pelo corpo em silhueta (simulação "e se", nunca com o eletricista ECASI fazendo errado — regra da série).
- **Descarga capacitiva (EP3):** glow do barramento decaindo com contador de volts.
- **Campo/zonas (EP4):** zonas NR-10 com shader de fresnel, corona nos isoladores.

### 5. Áudio
- Voz: reaproveitar `narracao-norm.mp3`; só um polimento leve opcional (de-esser + EQ de presença da cadeia do `C:\Editor.Videos\app\temas\08-instalacao-central-de-gas\reels\scripts\preparar.mjs`, **sem** arnndn em TTS), validando por A/B.
- SFX: refazer `build_sfx.py` com camadas sintetizadas em numpy (zumbido 60 Hz + harmônicos, crepitar de arco, estalo de disjuntor, clunk de seccionadora, chiado de capacitor, faísca) + arquivos Pixabay existentes + os 5 SFX MIT de `C:\Editor.Videos\app\.claude\skills\short-editing\assets\sfx\`. Cada animação de energia com som próprio.
- Mix: voz a -16 LUFS, SFX 3–8 dB abaixo (`measure_mix.py`), master final a **-14 LUFS / -1 dBTP** com loudnorm 2 passes (bloco do `preparar.mjs`) aplicado no mux final.

### 6. Render
- 1080×1920, 30 fps. Conferir com `npx hyperframes@0.8.217 render --help` se existem as opções de render segmentado/low-memory usadas em `C:\Editor.Videos\app\temas\12-cobertura-alto-padrao\scripts\render.mjs` (`HF_SEGMENT_FRAMES`, `--low-memory-mode`, `--resume`); usar se existirem (bloom aumenta memória).
- O aviso de falta de memória pode aparecer com o render terminando — conferir `renders/` e `render.log` antes de renderizar de novo.

### 7. Ferramentas e skills
- **Usar:** three examples/jsm (bloom), numpy (SFX), ffmpeg loudnorm 2 passes, cadeia de voz do editor.videos, SFX MIT do short-editing, grain/vinheta em canvas da skill `vox` (opcional, leve), `verify.mjs` do editor.videos como referência para checar LUFS/pico/quadros pretos.
- **Não usar:** LightningStrike (saiu do three após r152), three-nebula (estado acumulado, quebra o seek), Remotion (licença paga para empresa), OpenMontage (AGPL), minterpolate/Real-ESRGAN.
- **Depois do EP2 aprovado:** criar skill própria do projeto com `skill-creator` (`.claude\skills\bonequinho-3d\`) documentando rig, energia, SFX e mix — mais seguro que instalar coleções de terceiros.

### 8. Ordem
EP2 → aprovação → EP3 (reusa rig/efeitos, foco em painel/inversor/LOTO/descarga CC) → aprovação → EP4 (poste externo + cabine primária, SEP, aterramento; confirmar se a ECASI oferece o curso SEP).

## Arquivos críticos
- Base: `house\videos\reboco-novo\compositions\world.html`, `...\tools\build_sfx.py`, `measure_mix.py`, `sync_cues.py`.
- Por episódio: `epX-*-v2\compositions\world.html` (reescrito), `tools\build_sfx.py`, `index.html`, `cues_spec.json` (mantido).
- Editor.videos: `preparar.mjs` (tema 08), `render.mjs` (tema 12), `short-editing\assets\sfx\`.

## Verificação
- `npx hyperframes@0.8.217 check` sem erros.
- `snapshot` nos cues-chave lado a lado com o render antigo (personagem, logo nas costas, arco/bloom, mãos tocando os alvos).
- `tools\measure_mix.py` (SFX 3–8 dB abaixo, pico ≤ voz) e `ffmpeg ebur128` no MP4 final (-14 LUFS ±0,5, TP ≤ -1).
- Assistir o MP4 inteiro antes de entregar; entrega na pasta "serie eletrica insta" (vídeo, capa, legenda).
- Atualizar memória da série (base agora é o EP2-v2 / reboco) e README.
