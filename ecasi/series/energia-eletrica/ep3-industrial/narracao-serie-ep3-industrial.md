# Narração — Série Energia Elétrica · EP3/4 "Desligou o inversor. Já pode abrir?"

- **Público:** eletricistas e técnicos de manutenção industrial, além de supervisores e técnicos de segurança da fábrica. O EP2 terminou com a frase "No próximo episódio: a indústria, onde desligar não basta".
- **Formato:** Reel vertical 9:16, de 85 a 90s, no molde do EP1 e do EP2: gancho, 3 camadas, problema com números, mito, norma, CTA e loop.
- **Voz:** "Will" no ElevenLabs, a mesma do EP1 e do EP2, com tom calmo e explicativo, sem dramatizar.
- **Tom (manual da marca):** técnico, direto e humano. Cita a norma e não usa medo como argumento.
- **Cena:** chão de fábrica com um motor e uma bomba, e um painel de comando de 380 V com inversor de frequência. O display do inversor mostra a tensão do barramento CC. Do lado de fora fica a chave geral com a garra de multibloqueio.
- **Protagonista:** o **eletricista do Grupo ECASI**, de colete com o logo nas costas, capacete e óculos. O EPI do EP3 inclui **luvas isolantes e roupa FR** (antichama). Entra um segundo colega da manutenção para mostrar o "cada um com o seu cadeado".
- **Regra de conteúdo:** o eletricista ECASI só abre o painel depois das 3 camadas e nunca faz a prática errada. No mito, o display apaga sozinho enquanto o contador mostra que o barramento ainda tem tensão, e ele espera de braços cruzados.

---

## 1. Texto para colar na IA de voz (ElevenLabs)

Os números estão escritos por extenso. As reticências criam pausas. "PIE" está como "pê-i-é" para a voz não ler como a palavra em inglês.

```
Desligou o inversor do motor. Já pode abrir o painel? Não. Desligar não é desenergizar. Existem três camadas antes de abrir.

Primeiro, o problema. Num painel de trezentos e oitenta volts, o inversor guarda energia nos capacitores... e o barramento fica com uns quinhentos e quarenta volts, por minutos, depois de desligar. Alguém pode dar partida no motor sem saber. E um curto aqui dentro vira arco elétrico.

Camada um: planejar. Análise de risco, permissão de trabalho... e o diagrama atualizado na mão.

Camada dois: bloquear. Todas as fontes, não só a chave geral. E cada pessoa da equipe põe o próprio cadeado... que só ela tira.

Camada três: testar. Espere o tempo da etiqueta do inversor. Tente dar partida no motor. E meça zero volt no barramento, com o instrumento testado antes e depois.

Display apagou, então descarregou? Não. O display apaga com o barramento ainda em centenas de volts. E quinhentos e quarenta volts, pela NR dez, ainda é baixa tensão... mas baixa tensão não quer dizer baixo risco.

A NR dez exige o prontuário, o pê-i-é, acima de setenta e cinco quilowatts. A NR doze exige bloqueio na manutenção. E a NR um põe esses riscos no PGR.

Faça o treinamento NR dez com o Grupo Ecási. No próximo episódio: a cabine de média tensão, onde abrir a chave não basta.

Desligou o inversor? Confira as três camadas... antes de abrir.
```

**Como exportar:**
- Um único arquivo, só com a voz (sem música), em MP3 ou WAV, com as mesmas configurações do EP2.
- Me mande o caminho do arquivo, como no EP2.
- Duração esperada: 85 a 90s (cerca de 205 palavras, como o EP2, que deu 90,8s). Se passar de 95s, aumente um pouco a velocidade.
- Pronúncia: "Ecási", "NR dez", "NR doze" e "NR um" (ene-erre), "PGR" (pê-gê-erre) e "pê-i-é". Se a voz ler alguma sigla como palavra, troque pela forma soletrada.

---

## 2. Roteiro com o que aparece na tela

| Bloco | Fala | Na tela (cards e callouts) |
|---|---|---|
| Gancho | "Desligou o inversor do motor. Já pode abrir o painel? Não." | Título: "Desligou o inversor. **Já pode abrir?**" · o motor para e o eletricista ECASI vira o seletor do painel para "0" · o display do inversor continua aceso · selo "Série Energia Elétrica · EP 3/4" · "Não." gigante |
| Promessa | "Desligar não é desenergizar. Existem três camadas antes de abrir." | Card "desligar ≠ desenergizar" · barra no topo: **1 PLANEJAR · 2 BLOQUEAR · 3 TESTAR** |
| Problema | "O inversor guarda energia nos capacitores... e o barramento fica com uns 540 V, por minutos." | O painel fica em raio-x · capacitores do inversor brilhando · contador `barramento CC · 540 V` parado · card `380 V × √2 ≈ 540 V` |
| Problema | "Alguém pode dar partida no motor sem saber. E um curto aqui dentro vira arco elétrico." | Um sinal de partida remota chega pelo cabo e o eixo do motor gira sozinho (sem pessoa) · callout `partida inesperada` · clarão de arco dentro do painel e card `arco elétrico · energia incidente` |
| Camada 1 | "Planejar. Análise de risco, permissão de trabalho e o diagrama atualizado na mão." | "1" gigante + PLANEJAR · prancheta na mão do eletricista · 3 itens com ✓: `APR` · `permissão de trabalho` · `diagrama unifilar atualizado` |
| Camada 2 | "Bloquear. Todas as fontes, não só a chave geral. E cada pessoa põe o próprio cadeado." | "2" gigante + BLOQUEAR · as fontes acendem uma a uma: chave geral, alimentação do comando e ar comprimido do freio · garra de multibloqueio na chave geral · cadeado laranja do eletricista ECASI e cadeado azul do colega, cada um com etiqueta de nome · callout "só quem pôs tira" |
| Camada 3 | "Testar. Espere o tempo da etiqueta. Tente dar partida. Meça zero volt, com o instrumento testado antes e depois." | "3" gigante + TESTAR · etiqueta do inversor `⚠ aguarde 10 min` e relógio girando · o colega aperta "liga" e o motor não gira ✓ · multímetro nos bornes DC+ e DC− mostrando `0 V` · ícones `testa · mede · testa` |
| Mito | "Display apagou, então descarregou? Não. O display apaga com o barramento ainda em centenas de volts." | Card "⚠ mito" · o display apaga, mas o contador do barramento continua (540 V caindo devagar até uns 300 V) · callout `display apagado ≠ 0 V` · o eletricista espera do lado de fora |
| Mito | "540 V, pela NR-10, ainda é baixa tensão... mas baixa tensão não quer dizer baixo risco." | Régua da NR-10: `BT até 1.000 V CA · 1.500 V CC` com o marcador em 540 V · frase "baixa tensão ≠ baixo risco" |
| Norma | "A NR-10 exige o PIE acima de 75 kW. A NR-12, bloqueio na manutenção. E a NR-1, os riscos no PGR." | Tags `NR-10 · PIE > 75 kW` · `NR-12 · bloqueio` · `NR-01 · PGR` · o contador chega a 0 V e o eletricista abre o painel de luvas e roupa FR |
| CTA | "Faça o treinamento NR-10 com o Grupo ECASI. No próximo episódio: a cabine de média tensão, onde abrir a chave não basta." | Eletricista de costas, logo ECASI no colete · card final: logo + "Treinamento NR-10" + WhatsApp (11) 95618-8608 + "EP 4/4 · Próximo: na cabine, abrir a chave não basta" |
| Loop | "Desligou o inversor? Confira as três camadas... antes de abrir." | Volta ao plano do início ("...antes de abrir" emenda em "Desligou o inversor do motor...") |

**Sons das entradas** (3 a 8 dB abaixo da voz, mediana perto de −7 dB, conferido com `measure_mix.py`): motor desacelerando no gancho · zumbido dos capacitores · faísca curta no arco · whoosh nos números gigantes 1, 2 e 3 · clique de cadeado (2×) · tique do relógio · bipe do multímetro em 0 V · pop nos cards · chime nos ✓.

---

## 3. Fontes técnicas (para conferir antes de gravar)

- **Barramento CC do inversor:** o inversor retifica a rede e guarda a energia em capacitores. Em 380 V CA o barramento fica perto do pico, 380 × √2 ≈ **537 V** ("uns 540" na fala). Em 440 V, ≈ 622 V.
- **Tempo de descarga:** os manuais dos fabricantes mandam esperar antes de abrir. A WEG, por exemplo, pede pelo menos 10 minutos na linha CFW. Outros fabricantes falam em 5 a 15 minutos, por isso a fala diz "o tempo da etiqueta". Os manuais também avisam que o **display e os LEDs apagados não garantem que o barramento descarregou**: a fonte do comando desliga quando a tensão do barramento ainda é perigosa.
- **Faixa de baixa tensão (NR-10, glossário):** acima de 50 V CA ou 120 V CC, até **1.000 V CA ou 1.500 V CC**. Por isso 540 V CC ainda é baixa tensão.
- **Desenergização (NR-10, item 10.5.1):** seccionamento, impedimento de reenergização, constatação da ausência de tensão, aterramento temporário com equipotencialização, proteção dos elementos energizados na zona controlada e sinalização de impedimento de reenergização.
- **Planejamento (NR-10):** análise de risco (item 10.2.1), esquemas unifilares atualizados (item 10.2.3) e ordem de serviço (item 10.11.2). A permissão de trabalho é a prática usual das empresas para formalizar isso.
- **PIE (NR-10, item 10.2.4):** o Prontuário de Instalações Elétricas é obrigatório para estabelecimentos com carga instalada acima de **75 kW**.
- **NR-12 (bloqueio na manutenção):** a manutenção é feita com a máquina parada, com isolamento e descarga de todas as fontes de energia e bloqueio na posição desligado (item 12.11.3 na redação de 2019; conferir a numeração no texto vigente).
- **Bloqueio individual:** cada trabalhador põe o próprio cadeado na garra de multibloqueio, e só ele retira. É a prática de LOTO ("lockout/tagout") presente nos procedimentos de bloqueio das empresas.
- **Teste do instrumento antes e depois:** confere que o multímetro ou detector funciona antes e depois da medição ("testa, mede, testa"). Usar instrumento de categoria adequada (CAT III ou CAT IV, 1.000 V).
- **NR-01 (PGR):** os riscos elétricos entram no inventário de riscos do Programa de Gerenciamento de Riscos (item 1.5).
- **EPI do arco:** roupa FR (resistente a chama) e luvas isolantes de classe adequada, conforme a análise de risco (NR-10, item 10.2.9.2).

> Peça para um técnico de segurança da ECASI revisar os números e os itens da NR-10, NR-12 e NR-01 antes de gravar a voz.

---

## 4. Decisões (resolvidas em 31/10/2026)

- **CTA:** fica "Treinamento NR-10 com o Grupo ECASI", igual ao EP2.
- **Tensão de referência:** fica 380 V (cerca de 540 V no barramento CC).
