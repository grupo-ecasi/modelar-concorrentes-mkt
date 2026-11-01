# Narração — Série Energia Elétrica · EP2/4 "Terminou o quadro. Pode entregar?"

- **Público:** eletricistas residenciais (e o morador que contrata, que no EP1 ouviu "no próximo episódio, o que ele confere no seu quadro")
- **Formato:** Reel vertical 9:16, cerca de 85s, no mesmo molde do EP1 (gancho, 3 camadas, problema com números, mito, norma, CTA e loop)
- **Voz:** "Will" no ElevenLabs, a mesma do EP1, com tom calmo e explicativo, sem dramatizar
- **Tom (manual da marca):** técnico, direto e humano. Cita a norma e não usa medo como argumento.
- **Cena:** quadro de distribuição residencial em raio-x (cabos, barramento, disjuntores, DR, DPS e barra de terra). O protagonista é o **eletricista do Grupo ECASI**, com o colete com logo nas costas, **capacete e óculos** (EPI do EP2), alicate e chave isolada no cinto e o detector de tensão no bolso.
- **Regra de conteúdo:** o eletricista só mexe no quadro com o circuito desenergizado. Antes de abrir a tampa, ele desliga o geral e testa com o detector (gancho para o Reel NR-10 já publicado).

---

## 1. Texto para colar na IA de voz (ElevenLabs)

Números e siglas estão escritos por extenso para a voz pronunciar certo. As reticências criam pausas.

```
Terminou o quadro do cliente. Já pode entregar? Ainda não. Quadro que liga não é quadro seguro. Existem três camadas antes de entregar.

Primeiro, o problema. Cabo sobrecarregado esquenta... e o PVC só foi feito pra setenta graus. Uma fuga de poucos miliampéres, o disjuntor nem percebe. E sem terra, a carcaça do aparelho pode ficar energizada.

Camada um: proteção. O disjuntor é escolhido pelo cabo, não pela carga. Cabo de dois e meio, embutido, aguenta uns vinte e quatro ampéres. Então, disjuntor de vinte.

Camada dois: DR. Trinta miliampéres em banheiro, cozinha, lavanderia e área externa. E aperte o botão de teste. Não desarmou? Não entrega.

Camada três: terra. Fio terra em todos os circuitos, DPS no quadro... e cada disjuntor com etiqueta.

Disjuntor vive desarmando? Põe um maior? Não. Um de quarenta ampéres, num cabo que aguenta vinte e quatro, deixa passar quase o dobro sem desarmar. Aí quem vira fusível é o cabo... dentro da parede.

A NBR cinco mil quatrocentos e dez define o cabo, o DR e o terra. E a NR dez exige desenergizar antes, e curso de quarenta horas.

Faça o treinamento NR dez com o Grupo Ecási. No próximo episódio: a indústria, onde desligar não basta.

Terminou o quadro? Confira as três camadas... antes de entregar.
```

**Como exportar:**
- Um único arquivo, só com a voz (sem música), em MP3 ou WAV.
- Salve como `narracao-ep2.mp3` nesta pasta (`C:\app.Modelar-Concorrentes-MKT`) e me avise.
- Duração esperada: 80 a 90s (o texto tem cerca de 210 palavras; o EP1 tinha 205 e deu 82s). Se passar de 95s, aumente um pouco a velocidade da voz.
- Pronúncia: "Ecási" (com acento só no texto da IA), "NBR" soletrado (ene-bê-erre), "NR dez" (ene-erre dez), "DR" (dê-erre), "DPS" (dê-pê-esse) e "PVC" (pê-vê-cê). Se a voz ler alguma sigla como palavra, troque pela forma soletrada no texto (ex.: "dê erre").

---

## 2. Roteiro com o que aparece na tela

| Bloco | Fala | Na tela (cards / callouts) |
|---|---|---|
| Gancho | "Terminou o quadro do cliente. Já pode entregar? Ainda não." | Título: "Terminou o quadro. **Pode entregar?**" · eletricista ECASI de colete, capacete e óculos fecha a tampa do quadro e olha para a câmera · vinheta vermelha · selo "Série Energia Elétrica · EP 2/4" |
| Promessa | "Quadro que liga não é quadro seguro. Existem três camadas antes de entregar." | Tampa fica transparente (raio-x do quadro) · barra no topo: **1 PROTEÇÃO · 2 DR · 3 TERRA** |
| Problema | "Cabo sobrecarregado esquenta… e o PVC só foi feito pra 70 graus." | Cabo vai de azul para laranja · termômetro subindo · card `PVC · 70 °C em serviço contínuo` |
| Problema | "Uma fuga de poucos miliampéres, o disjuntor nem percebe. E sem terra, a carcaça pode ficar energizada." | Fio fino vazando bolinhas vermelhas e o disjuntor parado com "?" · card `fuga de mA → disjuntor não vê` · máquina de lavar com a carcaça piscando em vermelho e um "✕ terra" no cabo |
| Camada 1 | "Proteção. O disjuntor é escolhido pelo cabo, não pela carga. Cabo de 2,5 embutido aguenta uns 24 A. Então, disjuntor de 20." | "1" gigante + PROTEÇÃO · zoom no cabo com etiqueta `2,5 mm² · embutido · ~24 A` · disjuntor `20 A` encaixa com "tum" · callout "disjuntor ≤ capacidade do cabo" ✓ |
| Camada 2 | "DR. 30 mA em banheiro, cozinha, lavanderia e área externa. Aperte o botão de teste. Não desarmou? Não entrega." | "2" gigante + DR · planta da casa com os 4 cômodos acendendo · card `DR 30 mA` · dedo do eletricista aperta o botão "T" e a alavanca do DR cai ✓ · callout "teste no botão T" |
| Camada 3 | "Terra. Fio terra em todos os circuitos, DPS no quadro… e cada disjuntor com etiqueta." | "3" gigante + TERRA · fios verde-amarelo acendem até a barra de terra · DPS acende com um raio pequeno · etiquetas "CHUVEIRO", "COZINHA", "TOMADAS" aparecendo nos disjuntores |
| Mito | "Põe um maior? Não. Um de 40 A, num cabo que aguenta 24, deixa passar quase o dobro sem desarmar. Quem vira fusível é o cabo… dentro da parede." | Card "⚠ mito" · troca do disjuntor de 20 A por um de 40 A · comparação de escala: barra `40 A` × barra `24 A` · card `1,7× · 40 ÷ 24` · cabo dentro da parede fica laranja e solta fumaça, disjuntor continua ligado · vinheta vermelha |
| Norma | "A NBR 5410 define o cabo, o DR e o terra. E a NR-10 exige desenergizar antes, e curso de 40 horas." | Tags: `NBR 5410` · `DR 30 mA` · `NR-10` · `curso básico 40 h` · eletricista desliga o geral e testa com o detector antes de abrir a tampa |
| CTA | "Faça o treinamento NR-10 com o Grupo ECASI. No próximo episódio: a indústria, onde desligar não basta." | Eletricista de costas, logo ECASI no colete em destaque · card final: logo + "Treinamento NR-10" + "Próximo: na indústria, desligar não basta" + @grupoecasi |
| Loop | "Terminou o quadro? Confira as três camadas… antes de entregar." | Volta ao plano do início (o fim emenda no começo: "…antes de entregar" → "Terminou o quadro do cliente…") |

**Sons das entradas** (3 a 8 dB abaixo da voz, mediana perto de −7 dB, conferido com `measure_mix.py`): whoosh nos números gigantes 1, 2 e 3 · "tum" do disjuntor encaixando · clique do botão T e "tac" do DR desarmando · zumbido curto do DPS · chiado de fumaça no mito · pop nos cards · chime nos ✓.

---

## 3. Fontes técnicas (para conferir antes de gravar)

- **Isolação de PVC:** temperatura máxima em serviço contínuo de 70 °C (NBR 5410, tabela 35; 160 °C só em curto-circuito).
- **Capacidade do cabo de 2,5 mm²:** cobre, PVC, método de referência B1 (condutores isolados em eletroduto embutido em alvenaria), 2 condutores carregados: **24 A** (NBR 5410, tabela 36). Com 3 condutores carregados cai para 21 A, e o agrupamento de circuitos reduz mais ainda. Por isso a fala diz "uns".
- **Escolha do disjuntor:** a NBR 5410 (item 5.3.4.1) pede Ib ≤ In ≤ Iz: a corrente nominal do disjuntor fica entre a corrente do circuito e a capacidade do cabo. Com Iz = 24 A, o disjuntor padrão é o de 20 A.
- **Mito do disjuntor maior:** 40 A ÷ 24 A ≈ 1,67 ("quase o dobro" na fala, "1,7×" na tela). Pela curva de disparo, o disjuntor aguenta a corrente nominal sem desarmar, então o cabo trabalha acima da temperatura de projeto e o isolamento se degrada.
- **Fuga de corrente:** o disjuntor termomagnético atua por sobrecarga e curto-circuito (ampères). Uma fuga de dezenas de miliampéres não o faz atuar; quem detecta é o DR (item 5.1.3.2.2).
- **DR de 30 mA:** NBR 5410, item 5.1.3.2.2: circuitos de locais com banheira ou chuveiro, tomadas em áreas externas, tomadas internas que possam alimentar equipamentos na área externa, e circuitos de cozinhas, copas, lavanderias, áreas de serviço, garagens e outros locais molhados. Teste pelo botão "T": os fabricantes recomendam fazer periodicamente (em geral, todo mês).
- **Condutor de proteção (terra):** a NBR 5410 pede condutor de proteção em todos os circuitos (item 6.4.3, conferir a numeração na edição vigente).
- **DPS:** NBR 5410, item 5.4.2 / 6.3.5: obrigatório quando a instalação é alimentada por linha aérea ou fica em região com trovoadas frequentes (a maior parte do Brasil). Conferir a redação na edição vigente.
- **Identificação dos circuitos:** NBR 5410, item 6.1.5: os dispositivos de proteção do quadro devem ser identificados.
- **NR-10:** item 10.5 (desenergização antes de intervir) e item 10.8.8 com o Anexo II (curso básico de 40 horas para trabalhadores autorizados).

> Peça para um técnico de segurança da ECASI revisar os números e os itens da NBR 5410 e da NR-10 antes de gravar a voz.

---

## 4. Decisão pendente

- **CTA:** a versão acima oferece o **Treinamento NR-10 do Grupo ECASI** (como está no plano). Se preferir manter só "segue o Grupo ECASI", igual ao EP1, troco a frase.
