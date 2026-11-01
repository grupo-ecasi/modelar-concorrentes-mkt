# Narração — Reel NR-10 "Desligou o disjuntor. Já pode encostar?"

- **Formato:** Reel vertical 9:16, cerca de 70s, no estilo @raiox.tec com o design system do Grupo ECASI (mesmo molde do Reel NR-35)
- **Voz sugerida:** a mesma do NR-35 ("Will" no ElevenLabs), para a série ter identidade. Tom calmo e explicativo, sem dramatizar
- **Tom (manual da marca):** técnico, direto e humano. Cita a norma e não usa medo como argumento.
- **Cena:** eletricista da manutenção trocando a resistência do chuveiro do vestiário da empresa

---

## 1. Texto para colar na IA de voz (ElevenLabs)

Números e siglas estão escritos por extenso para a voz pronunciar certo. As reticências criam pausas.

```
Você desligou o disjuntor pra trocar a resistência do chuveiro do vestiário. Já pode encostar? Não. A ene erre dez exige três camadas antes de tocar no fio.

Primeiro, o problema. O chuveiro trabalha em duzentos e vinte volts... e mão suada ou molhada conduz bem. Com uns dez miliampéres, o músculo trava e você não consegue soltar. Com uns cinquenta, o coração pode parar.

Camada um: desligar e bloquear. Desliga o circuito certo e coloca cadeado e etiqueta no quadro. Assim, ninguém religa enquanto você trabalha.

Camada dois: testar. Primeiro, testa o detector num ponto com energia. Depois, mede o chuveiro. Sem tensão? Agora sim.

Camada três: aterrar e se proteger. Aterramento temporário no circuito, luva isolante e ferramenta isolada.

E atenção: desligou o disjuntor, tá seguro? Nem sempre. Na rede de cento e vinte e sete e duzentos e vinte volts, o chuveiro usa duas fases. Se o disjuntor tem um polo só, ele desliga uma... e a resistência continua com cento e vinte e sete volts. Só o detector mostra isso.

Por isso, a ene erre dez exige procedimento de desenergização e treinamento de quarenta horas, com reciclagem a cada dois anos.

Sua equipe está em dia? Fale com o Grupo Ecási.

Vai mexer no chuveiro? Confira as três camadas... antes de encostar.
```

**Como exportar:**
- Um único arquivo, só com a voz (sem música), em MP3 ou WAV.
- Salve como `narracao-nr10.mp3` nesta pasta (`C:\app.Modelar-Concorrentes-MKT`) e me avise.
- Duração esperada: 65 a 75s. Se passar de 80s, aumente um pouco a velocidade da voz.
- Pronúncia: "Ecási" (com acento só no texto da IA, para a voz não errar) e "miliampéres".

---

## 2. Roteiro com o que aparece na tela

| Bloco | Fala | Na tela (cards / callouts) |
|---|---|---|
| Gancho | "Você desligou o disjuntor pra trocar a resistência do chuveiro do vestiário. Já pode encostar? Não." | Título: "Desligou o disjuntor. Já pode **encostar**?" · mão indo até o chuveiro · callout "resistência" · vinheta vermelha |
| Promessa | "A NR-10 exige três camadas antes de tocar no fio." | Barra no topo: **1 BLOQUEAR · 2 TESTAR · 3 ATERRAR** |
| Problema | "O chuveiro trabalha em 220 V… 10 mA… 50 mA…" | Raio-x da resistência · card `220 V` · bolinha vermelha da mão ao peito · cards `10 mA · o músculo trava` → `50 mA · o coração pode parar` |
| Camada 1 | "Desligar e bloquear… cadeado e etiqueta no quadro… ninguém religa." | "1" gigante + BLOQUEAR · quadro de luz com o disjuntor descendo · cadeado + etiqueta "NÃO RELIGUE" · callout "circuito identificado" |
| Camada 2 | "Testar. Primeiro testa o detector num ponto com energia. Depois mede o chuveiro." | "2" gigante + TESTAR · detector acende na tomada (✓ funciona) → encosta no chuveiro → card `0 V · sem tensão ✓` |
| Camada 3 | "Aterrar e se proteger. Aterramento temporário, luva isolante, ferramenta isolada." | "3" gigante + ATERRAR · grampos do aterramento temporário · callouts "luva isolante" e "ferramenta isolada" |
| Mito | "Desligou o disjuntor, tá seguro? Nem sempre… duas fases… um polo só… continua com 127 V." | Raio-x dos dois fios: F1 apaga, **F2 continua vermelho** · card `127 V · ainda energizado` · callouts "disjuntor de 1 polo" / "F2 ligada" · vinheta vermelha |
| Norma | "A NR-10 exige procedimento de desenergização e treinamento de 40 h, com reciclagem a cada 2 anos." | 3 tags: `Desenergização (10.5.1)` · `Curso básico 40 h` · `Reciclagem bienal` |
| CTA | "Sua equipe está em dia? Fale com o Grupo ECASI." | Card final: logo + "Treinamento NR-10 · 40 h" + botão laranja "Falar no WhatsApp" · (11) 95618-8608 · @grupoecasi |
| Loop | "Vai mexer no chuveiro? Confira as três camadas antes de encostar." | Volta ao plano do início (o fim emenda no começo) |

---

## 3. Fontes técnicas (para conferir antes de publicar)

- **NR-10, item 10.5.1:** sequência de desenergização: a) seccionamento; b) impedimento de reenergização; c) constatação da ausência de tensão; d) aterramento temporário com equipotencialização dos condutores; e) proteção dos elementos energizados na zona controlada; f) sinalização de impedimento de reenergização. No vídeo, as camadas agrupam os passos assim: 1 = a + b + f · 2 = c · 3 = d + e.
- **NR-10, treinamento:** curso básico de 40 h para quem trabalha com instalações elétricas, com reciclagem bienal.
- **Efeitos da corrente (IEC 60479, CA 50/60 Hz):** cerca de 10 mA é o limite em que a pessoa ainda consegue soltar. Na faixa de dezenas de mA há risco de fibrilação ventricular.
- **Rede 127/220 V:** 127 V entre fase e neutro e 220 V entre fases. Chuveiro de 220 V nessa rede é ligado em duas fases. Um disjuntor unipolar só interrompe uma delas, e a outra continua com 127 V em relação à terra. Ainda assim, o circuito do chuveiro deve ter **disjuntor bipolar**.

> Peça para um técnico de segurança da ECASI revisar os números e o agrupamento dos passos da 10.5.1 antes de publicar. Confirme também a carga horária do curso que a ECASI oferece, para o card do CTA.
