# Roteiro — @house_pintura10 · "Sacada de madeira: dá pra salvar?"

- **Formato:** Reel vertical 9:16, **cerca de 20s**, sem narração. Só sons reais do trabalho (lixa, pincel, verniz), como no viral de 218 milhões do @volos.bushcraft.
- **Base:** fotos **reais** do site (`assets/img/ba4-antes.webp` e `ba4-depois.webp`, "Sacada de madeira com guarda-corpo pintado e deck envernizado", Atibaia - SP).
- **O que a IA faz:** só anima as etapas entre o antes e o depois reais (lixar, pintar o guarda-corpo, envernizar o deck). O começo e o fim são as fotos de verdade da obra.
- **Modelos combinados:** gancho em tela dividida (@volos.bushcraft) + etapas do processo (@dshousetransformation) + o momento da tinta cobrindo (@ateliervendome.pt) + frase em caixa alta (@master.pinturas10).
- **Identidade visual (site):** fundo `#0B1220`, destaque `#2457D6`, apoio `#5A98EF`, WhatsApp `#1A9E4B`, claro `#EEF2F8`. Títulos em **Barlow Condensed 800** (caixa alta), textos em **Bricolage Grotesque**, números em JetBrains Mono.

---

## 1. Plano a plano

| Tempo | Plano | O que se vê | Texto na tela | Som |
|---|---|---|---|---|
| **0,0–2,0s** | **GANCHO: tela dividida (fotos reais)** | Foto de ANTES em cima e foto de DEPOIS embaixo (cada uma 1080×960, encaixam juntas no 9:16). Uma barra azul `#2457D6` desliza de cima a baixo, como o "arraste e veja a diferença" do site. | Selos **ANTES** / **DEPOIS** no canto de cada metade. Título no meio: **"DÁ PRA SALVAR ESSA SACADA?"** | "tum" grave na entrada + whoosh na barra |
| **2,0–5,0s** | **ETAPA 1: LIXAR (IA)** | Close na madeira crua e descascada do guarda-corpo. Uma mão com luva lixa, sobe pó contra a luz do sol e aparece a madeira limpa por baixo. | Selo `01 · LIXAR` | lixa raspando (ASMR) |
| **5,0–9,0s** | **ETAPA 2: PINTAR (IA)** | Pincel com tinta branca correndo pelos balaústres recortados. A madeira cinza some sob o branco liso. É o momento satisfatório. | Selo `02 · PINTAR O GUARDA-CORPO` | pincel deslizando |
| **9,0–13,0s** | **ETAPA 3: ENVERNIZAR (IA)** | Rolo ou trincha passando verniz nas tábuas do deck. A tábua cinza vira marrom escuro e brilhante, tábua por tábua. | Selo `03 · VERNIZ NO DECK` | verniz molhado + clique leve a cada tábua |
| **13,0–17,0s** | **REVELAÇÃO (IA, do 1º ao último quadro)** | A câmera se afasta devagar e a sacada inteira aparece pronta. O vídeo termina exatamente na foto real de DEPOIS, com o sol batendo. | **"ANTES ➜ DEPOIS"** · `Atibaia - SP` | sino suave + respiro |
| **17,0–20,0s** | **ASSINATURA (motion, cores do site)** | Cartão escuro `#0B1220` com o logo da House, a linha **"MADEIRA E VERNIZ"**, **"Orçamento grátis"** e o botão verde **WhatsApp**. Ao fundo, a foto de depois desfocada. | `@house_pintura10` · `housepintura.com.br` | pop no botão |
| **20,0s** | **LOOP** | Volta à tela dividida do início, para a pessoa ver de novo. | — | — |

**Por que essa ordem prende:** o gancho mostra o resultado nos primeiros 2 segundos, mas em duas metades pequenas. A curiosidade é ver como ficou de perto, e isso só acontece aos 13s. As três etapas numeradas (01, 02, 03) seguram a atenção do mesmo jeito que a barra 1-2-3 do Reel da NR-10.

---

## 2. Prompts para a IA de vídeo (Seedance 2.5, imagem para vídeo, 9:16, 720p)

Todos partem das fotos reais. O texto em inglês rende melhor no modelo.

1. **Lixar (4s)**, a partir de um recorte em close de `ba4-antes`:
   `Vertical close-up of a weathered wooden balcony railing with peeling white paint. A gloved hand sands the wavy wooden baluster with sandpaper, fine dust floating in warm afternoon sunlight, bare clean wood revealed underneath. Realistic, handheld, shallow depth of field, no text.`
2. **Pintar (4s)**, a partir do recorte do guarda-corpo já lixado:
   `A paintbrush loaded with bright white paint glides down a curved wooden baluster of a balcony railing, smooth white coat covering the raw grey wood in one stroke, satisfying, realistic, warm sunlight, vertical, no text.`
3. **Envernizar (4s)**, a partir de um recorte do deck em `ba4-antes`:
   `Top-down vertical shot of grey weathered wooden deck boards. A brush applies dark walnut varnish board by board, the wood turns rich brown and glossy, wet shine reflecting sunlight, realistic, no text.`
4. **Revelação (4s)**, com primeiro quadro = `ba4-antes` e último quadro = `ba4-depois`:
   `Slow cinematic camera move along a wooden balcony as it transforms: the railing becomes clean bright white and the deck becomes dark varnished wood, warm sunlight, realistic, no people, no text.`

> As fotos reais têm 960×960 e ângulos diferentes. O modelo completa as bordas para chegar ao 9:16. No plano 4 a câmera "viaja" do ângulo do antes até o do depois, o que vira um movimento de câmera natural.

**Custo estimado:** 4 clipes × 4s = 16s × cerca de US$ 0,10–0,23/s ≈ **US$ 2 a 4** por rodada. Com uma ou duas refações, uns **US$ 5 a 8**. O saldo atual do treg é de US$ 0,90, então é preciso recarregar antes de gerar.

---

## 3. Legenda do post (rascunho)

```
Dá pra salvar uma sacada de madeira assim? 👀

Essa aqui, em Atibaia, estava com a madeira crua, a tinta descascando e o deck cinza do sol e da chuva.

O que a House fez:
01 · Lixou tudo até a madeira limpa
02 · Pintou o guarda-corpo de branco
03 · Envernizou o deck, tábua por tábua

Madeira bem preparada e protegida dura muito mais. Antes e depois são fotos reais da obra (as etapas foram ilustradas com IA).

Você deixaria o deck escuro assim ou mais claro? Conta aqui 👇

📲 Orçamento grátis pelo WhatsApp · link na bio
House Pinturas e Decorações · Atibaia - SP

#pinturademadeira #verniz #antesedepois #atibaia #housepinturas
```

Ao postar, marcar o rótulo **"Feito com IA"** do Instagram. Ele é obrigatório para imagem realista gerada por IA, e a legenda já explica o que é real.

---

## 4. Como fica a produção

1. Você aprova este roteiro e recarrega o treg.
2. Eu gero os 4 clipes, escolho as melhores tomadas e monto no HyperFrames: tela dividida, selos, cartão final nas cores do site, sons e loop.
3. Entrego o MP4, a capa e a legenda na pasta **house pintura insta** da Área de Trabalho.

**Alternativa já baixada:** o par **piso vermelho encerado** (`ba3`, corredor externo) rende um segundo vídeo no mesmo molde. O gancho seria "OLHA O BRILHO DESSE PISO", com a revelação do reflexo do sol nas lajotas.
