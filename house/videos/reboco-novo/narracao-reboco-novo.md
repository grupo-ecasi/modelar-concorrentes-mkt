# Narração — House Pinturas · "Rebocou ontem. Já pode pintar?"

- **Formato:** Reel vertical 9:16, cerca de 80 a 88s, no molde do vídeo do mofo: gancho, 3 camadas, problema, mito com número, norma, CTA e loop.
- **Personagens (bonequinho low-poly):**
  - **Morador**, de camiseta e bermuda. Quer pintar a parede que o pedreiro rebocou ontem.
  - **Pintor da House**, de camiseta azul #2457D6 com o logo e rolo na mão. Entra nas camadas e no CTA.
- **Cena:** cômodo em reforma, com a parede recém-rebocada (cinza escuro e úmida), balde de massa, colher de pedreiro, lona no chão e uma lata de tinta fechada.
- **Tom:** de conversa e explicativo. Não usa medo como argumento.

---

## 1. Texto para colar na IA de voz

Os números e as siglas estão por extenso para a voz pronunciar certo. As reticências criam pausas.

```
Rebocou ontem. Já pode pintar? Ainda não. Seco por fora não é parede pronta. São três camadas antes da tinta.

Primeiro, o problema. Reboco novo ainda tem água e cal lá dentro. Se pintar agora, a água sai empurrando a tinta... e aparecem bolhas, manchas brancas e tinta descascando.

Camada um: esperar. Vinte e oito dias de cura. É o tempo da parede secar por dentro.

Camada dois: limpar e firmar. Escova o pó e os grãos soltos. Se a parede esfarela na mão, fundo preparador.

Camada três: selar. Selador acrílico antes da massa e da tinta. Ele iguala a absorção... e a tinta rende mais.

Passou a mão e está seco? Não basta. Por dentro, o reboco novo tem pH perto de treze: um milhão de vezes mais alcalino que a água. É isso que mancha e solta a tinta.

A ene bê erre treze mil duzentos e quarenta e cinco pede esperar a cura do reboco antes de pintar.

Na dúvida, chama a House Pinturas. Orçamento grátis no WhatsApp.

Rebocou ontem? Espera, prepara e sela... antes de pintar.
```

**Como exportar**
- Um arquivo só, com a voz (sem música), em MP3 ou WAV, com a mesma voz e as mesmas configurações do vídeo do mofo.
- Me mande o caminho do arquivo, como nos outros vídeos.
- Duração esperada: 80 a 88s (cerca de 185 palavras). Se passar de 95s, aumente um pouco a velocidade.
- Pronúncia: "House" como "Ráus". Se a voz errar, escreva "Ráus" no texto da IA. "pH" deve sair "pê agá"; se a voz ler errado, troque por "pê agá" no texto.

---

## 2. Roteiro com o que aparece na tela

| Bloco | Fala | Na tela |
|---|---|---|
| Gancho | "Rebocou ontem. Já pode pintar? Ainda não." | O morador chega com o rolo cheio de tinta na frente da parede cinza recém-rebocada. Título: "Rebocou ontem. **Já pode pintar?**" Vinheta vermelha e "Ainda não." gigante |
| Promessa | "Seco por fora não é parede pronta. São três camadas antes da tinta." | Card "seco por fora ≠ parede pronta" · barra no topo: **1 ESPERAR · 2 LIMPAR · 3 SELAR** |
| Problema | "Reboco novo ainda tem água e cal lá dentro." | Corte da parede (raio-x): gotas de água e grãos de cal dentro do reboco · callouts "água", "cal" |
| Problema | "A água sai empurrando a tinta: bolhas, manchas brancas e tinta descascando." | Simulação (o morador não pinta de verdade, é um "e se"): a película de tinta aparece sobre a parede, a água sobe e estufa bolhas, surgem manchas brancas (eflorescência) e a tinta descasca · callouts nos três defeitos · vinheta vermelha |
| Camada 1 | "Esperar. Vinte e oito dias de cura. É o tempo da parede secar por dentro." | Número gigante **"1"** · calendário virando até **28 dias** · a parede passa de cinza escuro (úmida) para cinza claro (seca), e as gotas do corte somem |
| Camada 2 | "Limpar e firmar. Escova o pó e os grãos soltos. Se esfarela na mão, fundo preparador." | Número **"2"** · o pintor da House passa a escova e o pó cai · ele passa a mão: se sai areia, entra a lata "FUNDO PREPARADOR" (genérica, sem marca) |
| Camada 3 | "Selar. Selador acrílico antes da massa e da tinta. Iguala a absorção e a tinta rende mais." | Número **"3"** · camadas montando no corte: reboco, selador, massa e tinta · comparação de absorção: sem selador a tinta "some" em manchas, com selador fica uniforme |
| Mito | "Passou a mão e está seco? Não basta. pH perto de treze: um milhão de vezes mais alcalino que a água." | Card "⚠ mito" · a mão do morador na parede e "seco ✓" por fora · régua de pH de 0 a 14 com a água em 7 e o reboco novo em 13 · card **10⁶× · 13 − 7 = 6 casas** |
| Mito | "É isso que mancha e solta a tinta." | Corte: a alcalinidade "ataca" a película de tinta (manchas e descolamento) |
| Norma | "A NBR 13245 pede esperar a cura do reboco antes de pintar." | Card verde: "**NBR 13245** · preparo da superfície · cura do reboco" com check |
| CTA | "Na dúvida, chama a House Pinturas. Orçamento grátis no WhatsApp." | O pintor da House de costas, logo na camiseta · botão verde do WhatsApp, logo e @house_pintura10 |
| Loop | "Rebocou ontem? Espera, prepara e sela... antes de pintar." | Volta ao plano do início ("...antes de pintar" emenda em "Rebocou ontem...") |

**Sons das entradas** (de 3 a 8 dB abaixo da voz, conferidos com `measure_mix.py`): pingos de água · "ploc" das bolhas · whoosh nos números 1, 2 e 3 · virada de página do calendário · escova raspando · pop nos cards · chime nos ✓.

---

## 3. Fontes técnicas (para conferir antes de gravar)

- **Cura do reboco:** a ABNT NBR 13245 (Tintas para construção civil — execução de pinturas em edificações não industriais — preparação de superfície) orienta aguardar a cura e a secagem do reboco antes de pintar; o prazo usual citado para argamassa e reboco novos é de **28 dias**. Conferir a redação na edição vigente.
- **Alcalinidade:** argamassas de cimento e cal ficam com pH perto de 12,5 a 13 quando novas. O pH cai com a secagem e a carbonatação da superfície ao longo das semanas.
- **"Um milhão de vezes":** o pH é logarítmico. De 7 (água pura) para 13 são 6 unidades, ou seja, 10⁶ vezes mais íons hidroxila (alcalinidade).
- **Defeitos de pintar cedo:** a água que evapora empurra a película (bolhas e descascamento); os sais da cal migram e cristalizam na superfície (eflorescência, as manchas brancas); a alcalinidade ataca a resina da tinta (saponificação: manchas, perda de aderência).
- **Fundo preparador:** indicado pelos fabricantes para superfícies que soltam pó ou esfarelam (reboco fraco), para dar coesão antes da pintura.
- **Selador acrílico:** indicado para reboco novo e poroso, depois da cura. Uniformiza a absorção e reduz o consumo de massa e tinta.
- Não citar marcas nem valores em R$.

> Se possível, peça para a House conferir as recomendações dos fabricantes que ela usa (prazo de cura, fundo preparador e selador) antes de gravar.
