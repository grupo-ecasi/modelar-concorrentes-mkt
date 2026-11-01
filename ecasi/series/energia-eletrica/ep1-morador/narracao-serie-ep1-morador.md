# Narração — Série Energia Elétrica · EP1/4 "Trocar a resistência do chuveiro pode dar choque?"

- **Público:** moradores e proprietários, sem formação em elétrica
- **Formato:** Reel vertical 9:16, cerca de 85s, no mesmo molde do Reel NR-10 (gancho, 3 camadas, problema com números, mito, norma, CTA e loop)
- **Voz:** a mesma do NR-10 e do NR-35 ("Will" no ElevenLabs), com tom calmo e explicativo, sem dramatizar
- **Tom (manual da marca):** técnico, direto e humano. Cita a norma e não usa medo como argumento.
- **Cena:** banheiro de casa, com o quadro de luz no corredor. O protagonista é o **morador** (camiseta, bermuda e chinelo, sem EPI). No fim, entra o **eletricista do Grupo ECASI de colete**, com o detector de tensão na mão.
- **Regra de conteúdo:** o morador **nunca** aparece medindo tensão nem mexendo em fio. A verificação de ausência de tensão é de pessoa competente, e o detector só aparece com o eletricista.

---

## 1. Texto para colar na IA de voz (ElevenLabs)

Números e siglas estão escritos por extenso para a voz pronunciar certo. As reticências criam pausas.

```
Fechou o chuveiro pra trocar a resistência. Pode levar choque? Pode. Os fios continuam com energia. Existem três camadas antes de encostar.

Primeiro, o problema. O chuveiro puxa uns trinta e quatro ampéres... mais que a geladeira, a TV e o micro-ondas juntos. E mão molhada conduz bem. Com uns dez miliampéres, o músculo trava. Com uns cinquenta, o coração pode parar.

Camada um: desligar no quadro. Nem o registro, nem a chave de temperatura cortam a energia. Só o disjuntor do chuveiro.

Camada dois: conferir. Resistência do mesmo modelo e da mesma tensão: cento e vinte e sete ou duzentos e vinte volts. Fio queimado? O problema é na instalação.

Camada três: saber parar. Não achou o disjuntor? Não tem como confirmar que está sem tensão? Pare aqui.

E resistência é tudo igual? Não. Uma de cento e vinte e sete volts ligada em duzentos e vinte esquenta três vezes mais... e pode queimar na hora.

A NBR cinco mil quatrocentos e dez exige um circuito só pro chuveiro, com proteção DR.

Na dúvida, chame um eletricista qualificado. E segue o Grupo Ecási: no próximo episódio, o que ele confere no seu quadro.

Vai trocar a resistência? Confira as três camadas... antes de encostar.
```

**Como exportar:**
- Um único arquivo, só com a voz (sem música), em MP3 ou WAV.
- Salve como `narracao-ep1.mp3` nesta pasta (`C:\app.Modelar-Concorrentes-MKT`) e me avise.
- Duração esperada: 80 a 90s. Se passar de 95s, aumente um pouco a velocidade da voz.
- Pronúncia: "Ecási" (com acento só no texto da IA, para a voz não errar), "miliampéres" e "NBR" soletrado (ene-bê-erre). Se a voz ler "NBR" como palavra, troque por "ene bê erre" no texto.

---

## 2. Roteiro com o que aparece na tela

| Bloco | Fala | Na tela (cards / callouts) |
|---|---|---|
| Gancho | "Fechou o chuveiro pra trocar a resistência. Pode levar choque? Pode." | Título: "Trocar a resistência pode dar **choque**?" · morador de chinelo fecha o registro e olha para o chuveiro · vinheta vermelha · selo "Série Energia Elétrica · EP 1/4" |
| Promessa | "Os fios continuam com energia. Existem três camadas antes de encostar." | Raio-x rápido: fios da parede acesos em vermelho até o chuveiro · barra no topo: **1 DESLIGAR · 2 CONFERIR · 3 SABER PARAR** |
| Problema | "O chuveiro puxa uns 34 A… mais que a geladeira, a TV e o micro-ondas juntos." | Card `34 A · 7.500 W ÷ 220 V` · comparação de escala: barra grande "chuveiro 34 A" ao lado de três barrinhas empilhadas (geladeira, TV, micro-ondas ≈ 13 A) |
| Problema | "Mão molhada conduz bem. 10 mA… 50 mA…" | Gotas na mão do morador · bolinha vermelha da mão ao peito · cards `10 mA · o músculo trava` → `50 mA · o coração pode parar` |
| Camada 1 | "Desligar no quadro. Nem o registro, nem a chave de temperatura cortam a energia. Só o disjuntor do chuveiro." | "1" gigante + DESLIGAR · ✕ sobre o registro e ✕ sobre a chave "inverno / verão" (fios continuam vermelhos) · câmera vai ao quadro no corredor · disjuntor com etiqueta "CHUVEIRO" desce · fios ficam cinza ✓ · callout "disjuntor do chuveiro" |
| Camada 2 | "Conferir. Resistência do mesmo modelo e da mesma tensão: 127 ou 220 V. Fio queimado? O problema é na instalação." | "2" gigante + CONFERIR · embalagem da resistência ao lado do chuveiro com etiquetas `modelo ✓` e `220 V ✓` · close no fio escurecido · callout "fio queimado = problema na instalação" |
| Camada 3 | "Saber parar. Não achou o disjuntor? Não tem como confirmar que está sem tensão? Pare aqui." | "3" gigante + SABER PARAR · checklist com 2 itens que ganham "?" em laranja · placa "PARE" · morador guarda a chave de fenda |
| Mito | "Resistência é tudo igual? Não. Uma de 127 V ligada em 220 esquenta três vezes mais… e pode queimar na hora." | Card "⚠ atenção" · resistência com etiqueta "127 V" encaixada num chuveiro "220 V" · comparação de escala: barra `5.500 W` (o certo) × barra `16.500 W` (3×) · card `3× · (220 ÷ 127)²` · resistência fica laranja e solta faísca · vinheta vermelha |
| Norma | "A NBR 5410 exige um circuito só pro chuveiro, com proteção DR." | Tags: `NBR 5410` · `circuito exclusivo` · `DR 30 mA` · close no DR do quadro |
| CTA | "Na dúvida, chame um eletricista qualificado. E segue o Grupo ECASI: no próximo episódio, o que ele confere no seu quadro." | Entra o **eletricista de colete ECASI** com o detector de tensão na mão, ao lado do morador · card final: logo + "Série Energia Elétrica" + "Próximo: o que o eletricista confere no quadro" + @grupoecasi |
| Loop | "Vai trocar a resistência? Confira as três camadas… antes de encostar." | Volta ao plano do início (o fim emenda no começo: "…antes de encostar" → "Fechou o chuveiro…") |

**Sons das entradas** (mais altos que no NR-10, sempre abaixo da voz): whoosh nos números gigantes 1, 2 e 3 · "tum" do disjuntor descendo · pop nos cards · faísca/zap curto no mito e na resistência queimando · chime no "✓" dos fios desligados.

---

## 3. Fontes técnicas (para conferir antes de gravar)

- **Corrente do chuveiro:** I = P ÷ V = 7.500 W ÷ 220 V ≈ 34 A. Para comparar: geladeira (cerca de 150 W), TV (cerca de 100 W) e micro-ondas (cerca de 1.400 W) somam uns 13 A em 127 V. Os valores dos aparelhos variam por modelo, por isso a fala diz "uns".
- **Efeitos da corrente (IEC 60479, CA 50/60 Hz):** cerca de 10 mA é o limite em que a pessoa ainda consegue soltar. Na faixa de dezenas de mA há risco de fibrilação ventricular. Mesmos números do Reel NR-10.
- **Registro e chave de temperatura:** o chuveiro só liga a resistência quando a água passa (diafragma), e a chave de temperatura só escolhe o trecho da resistência. Nenhum dos dois desenergiza os fios que chegam da parede. Só o disjuntor do circuito faz isso. Atenção: o Reel NR-10 mostra que um disjuntor de 1 polo deixa a outra fase ligada em redes 127/220 V. Por isso, a camada 3 diz para parar quando não houver como confirmar a ausência de tensão.
- **Resistência de tensão errada:** P = V² ÷ R. Uma resistência de 127 V em 220 V dissipa (220 ÷ 127)² ≈ 3,0 vezes a potência nominal (ex.: 5.500 W viram cerca de 16.500 W) e queima. O contrário (220 V em 127 V) dá cerca de 1/3 da potência e a água não esquenta.
- **ABNT NBR 5410:**
  - item 5.1.3.2.2: proteção diferencial-residual (DR) de no máximo 30 mA nos circuitos que atendem locais com banheira ou chuveiro;
  - item 9.5.3.2 (conferir a numeração na edição vigente): equipamento com corrente nominal acima de 10 A deve ter circuito independente.

> Peça para um técnico de segurança da ECASI revisar os números e os itens da NBR 5410 antes de gravar a voz.

---

## 4. Decisão pendente

- **CTA:** a versão acima convida a **seguir o Grupo ECASI** para o próximo episódio (gancho da série). Se a ECASI atende serviço residencial, dá para trocar por "Fale com o Grupo ECASI" + WhatsApp, igual ao NR-10.
