# Narração — Reel NR-35 "As 3 camadas do trabalho em altura"

- **Formato:** Reel vertical 9:16, cerca de 70s, no estilo @raiox.tec com o design system do Grupo ECASI
- **Voz sugerida:** Esmeralda (porta-voz da marca), em tom calmo e explicativo, sem dramatizar
- **Tom (manual da marca):** técnico, direto e humano. Cita a norma e não usa medo como argumento.

---

## 1. Texto para colar na IA de voz (ElevenLabs / HeyGen)

Números e siglas estão escritos por extenso para a voz pronunciar certo. As reticências criam pausas.

```
Você está a três metros de altura, de cinto paraquedista. Isso basta? Não. A ene erre trinta e cinco organiza a sua proteção em três camadas.

Primeiro: trabalho em altura é qualquer atividade acima de dois metros do nível inferior, onde existe risco de queda. E uma queda de dois metros dura menos de um segundo... você chega embaixo a mais de vinte quilômetros por hora.

Camada um: evitar. Dá pra fazer do chão? Montar a peça embaixo e içar, usar uma ferramenta com cabo extensor. Se não precisa subir... não sobe.

Camada dois: eliminar a queda. Proteção coletiva: plataforma de trabalho e guarda-corpo, com o travessão superior a um metro e vinte do piso.

Camada três: reduzir as consequências. É aqui que entra o cinto. Ponto de ancoragem, talabarte com absorvedor de energia e cinturão paraquedista. Na queda, o absorvedor se abre e limita a força no seu corpo a seis quilonewtons.

E atenção: ancorou no pé? A queda livre pode chegar ao dobro do comprimento do talabarte. Sempre que possível, a ancoragem fica acima da cabeça.

Antes de subir, a ene erre trinta e cinco exige análise de risco, plano de resgate e treinamento de oito horas, com reciclagem a cada dois anos.

Sua equipe está em dia? Fale com o Grupo Ecási.

Vai trabalhar em altura? Confira as três camadas... antes de subir.
```

**Como exportar:**
- Um único arquivo, só com a voz (sem música), em MP3 ou WAV.
- Salve como `narracao-nr35.mp3` nesta pasta (`C:\app.Modelar-Concorrentes-MKT`) e me avise.
- Duração esperada: 65 a 75s. Se passar de 80s, aumente um pouco a velocidade da voz.
- Pronúncia: "Ecási" (com acento só no texto da IA, para a voz não errar).

---

## 2. Roteiro com o que aparece na tela

| Bloco | Fala | Na tela (cards / callouts) |
|---|---|---|
| Gancho | "Você está a três metros de altura, de cinto paraquedista. Isso basta? Não." | Título: "Só o cinto **basta**?" · card `3 m` · callout "cinturão paraquedista" |
| Promessa | "A NR-35 organiza a sua proteção em três camadas." | Barra no topo: **1 EVITAR · 2 ELIMINAR · 3 REDUZIR** |
| Problema | "Trabalho em altura é qualquer atividade acima de dois metros… menos de um segundo… mais de 20 km/h." | Linha de 2,00 m na parede · card `> 2,00 m · NR-35` · contadores `0,64 s` e `22 km/h` |
| Camada 1 | "Evitar. Dá pra fazer do chão?… Se não precisa subir, não sobe." | "1" gigante + EVITAR · peça montada no chão e içada · callout "cabo extensor" |
| Camada 2 | "Eliminar a queda. Proteção coletiva: plataforma e guarda-corpo, travessão superior a 1,20 m." | "2" gigante + ELIMINAR · guarda-corpo se montando · cota `1,20 m` · tag `NR-18` |
| Camada 3 | "Reduzir as consequências… ancoragem, talabarte com absorvedor, cinturão paraquedista… 6 kN." | "3" gigante + REDUZIR · as 3 peças do sistema com callouts · queda em câmera lenta · absorvedor abrindo · card `≤ 6 kN · NBR 14629` |
| Atenção | "Ancorou no pé? A queda livre pode chegar ao dobro do talabarte… ancoragem acima da cabeça." | Comparação lado a lado: ancoragem no pé (queda longa) x acima da cabeça (queda curta) · card `fator de queda 2 x 1` |
| Norma | "A NR-35 exige análise de risco, plano de resgate e treinamento de 8 h, com reciclagem a cada 2 anos." | 3 tags: `Análise de risco` · `Plano de resgate` · `8 h · reciclagem bienal` |
| CTA | "Sua equipe está em dia? Fale com o Grupo ECASI." | Card final: logo + "Treinamento NR-35 · 8 h com prática presencial" + botão laranja "Falar no WhatsApp" · (11) 95618-8608 · @grupoecasi |
| Loop | "Vai trabalhar em altura? Confira as três camadas antes de subir." | Volta ao plano do início (o fim emenda no começo) |

---

## 3. Fontes técnicas (para conferir antes de publicar)

- **NR-35:** trabalho em altura acima de 2,00 m do nível inferior com risco de queda. Ordem de medidas: evitar o trabalho em altura → eliminar o risco de queda → minimizar as consequências. Treinamento de 8 h e reciclagem bienal. Análise de risco e emergência/resgate obrigatórios.
- **NR-18:** guarda-corpo com travessão superior a 1,20 m.
- **ABNT NBR 14629:** absorvedor de energia limita a força de frenagem a no máximo 6 kN.
- **Física:** queda livre de 2 m dura cerca de 0,64 s e termina a cerca de 22,5 km/h (6,3 m/s).

> Peça para um técnico de segurança da ECASI revisar os números antes de publicar.
