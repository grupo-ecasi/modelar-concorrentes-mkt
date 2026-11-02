# Fachada do zero (House Pinturas) · formato Escada do Zero

Primeiro vídeo no formato `roteiro-escada-do-zero`, com o bonequinho 3D `pintor` (`personagens/pintor/`).

## A. Resumo

- **Tema:** proteger a fachada da casa contra sol e chuva.
- **Resultado final:** fachada pintada que aguenta sol e chuva, feita por um pintor profissional.
- **Selos:** 1 · Cal · 2 · Tinta PVA · 3 · Tinta acrílica · 4 · Lixa e selador · 5 · Trincas vedadas · 6 · Elastomérica · 7 · Projeto da fachada
- **Versão:** longa, 7 degraus.
- **Duração estimada:** cerca de 2:10 (ritmo da voz de IA dos vídeos anteriores, ~2,6 palavras/s).
- **Palavras:** 353 (faixa da versão longa: 300 a 380).
- **Loop:** por retorno (o recap volta ao balde de cal, que é a primeira imagem).

## B. Narração limpa (com marcação de degraus)

```
Se você quiser uma fachada que aguenta sol e chuva, começando do zero,
[1] pegue um balde, misture cal com água
e passe na parede com uma broxa.
A casa vai ficar branquinha,
mas a cada chuva a cal vai lavando e manchando a parede.
[2] Então, troque a cal por uma tinta látex PVA.
A resina cola o pigmento na parede
e a cor fica firme.
Entretanto, essa tinta foi feita para dentro de casa:
na fachada, ela absorve a chuva e começa a esfarelar.
[3] Para aguentar o tempo, use tinta acrílica.
A resina acrílica forma uma película contínua
que faz a água da chuva escorrer.
Porém, passada direto no reboco, ela descasca em poucos meses.
Agora você tem a tinta certa, mas ainda precisa de uma base firme.
[4] Antes de pintar, lixe a parede,
escove todo o pó
e aplique um selador acrílico.
O selador entra nos poros do reboco
e cria a base onde a tinta agarra.
Mas existe um problema:
a parede tem trincas finas,
e a água entra por elas.
[5] Abra cada trinca em V,
preencha com selante acrílico flexível
e alise por cima.
O selante estica e encolhe junto com a parede.
Só que o sol esquenta a fachada de dia,
a noite esfria,
e novas fissuras fininhas continuam aparecendo.
[6] Então, finalize com tinta elastomérica, em demãos cruzadas.
Ela forma uma camada grossa e elástica,
como uma borracha,
que estica por cima das fissuras sem rachar.
Agora você tem uma fachada vedada,
mas ainda precisa que ela dure.
[7] Mas não basta comprar a tinta mais cara e esperar que ela dure.
Meça cada parede,
considere o sol e a chuva que batem em cada lado da casa
e dimensione a tinta, as demãos e o tempo de secagem.
Faça isso com um pintor profissional.
Assim, você terá uma fachada projetada para atender às necessidades da sua casa.
E foi assim que você saiu de um balde de cal
e chegou a uma fachada que aguenta sol e chuva.
Agora me diga: o que mais você quer aprender a construir do zero?
Comente aqui embaixo e acompanhe o próximo vídeo!
```

### Para colar na IA de voz (sem marcações)

```
Se você quiser uma fachada que aguenta sol e chuva, começando do zero, pegue um balde, misture cal com água e passe na parede com uma broxa. A casa vai ficar branquinha, mas a cada chuva a cal vai lavando e manchando a parede. Então, troque a cal por uma tinta látex PVA. A resina cola o pigmento na parede e a cor fica firme. Entretanto, essa tinta foi feita para dentro de casa: na fachada, ela absorve a chuva e começa a esfarelar. Para aguentar o tempo, use tinta acrílica. A resina acrílica forma uma película contínua que faz a água da chuva escorrer. Porém, passada direto no reboco, ela descasca em poucos meses. Agora você tem a tinta certa, mas ainda precisa de uma base firme. Antes de pintar, lixe a parede, escove todo o pó e aplique um selador acrílico. O selador entra nos poros do reboco e cria a base onde a tinta agarra. Mas existe um problema: a parede tem trincas finas, e a água entra por elas. Abra cada trinca em V, preencha com selante acrílico flexível e alise por cima. O selante estica e encolhe junto com a parede. Só que o sol esquenta a fachada de dia, a noite esfria, e novas fissuras fininhas continuam aparecendo. Então, finalize com tinta elastomérica, em demãos cruzadas. Ela forma uma camada grossa e elástica, como uma borracha, que estica por cima das fissuras sem rachar. Agora você tem uma fachada vedada, mas ainda precisa que ela dure. Mas não basta comprar a tinta mais cara e esperar que ela dure. Meça cada parede, considere o sol e a chuva que batem em cada lado da casa e dimensione a tinta, as demãos e o tempo de secagem. Faça isso com um pintor profissional. Assim, você terá uma fachada projetada para atender às necessidades da sua casa. E foi assim que você saiu de um balde de cal e chegou a uma fachada que aguenta sol e chuva. Agora me diga: o que mais você quer aprender a construir do zero? Comente aqui embaixo e acompanhe o próximo vídeo!
```

## C. Decupagem (YAML)

```yaml
titulo: "Fachada que aguenta sol e chuva, do zero"
personagem: pintor
cenario_base: "casa térrea com fachada de reboco cru, calçada e rua; mesmo cenário externo do reboco-novo"
duracao_alvo_s: 130
loop: retorno
cenas:
  - id: 0
    tipo: gancho
    narracao: ["Se você quiser uma fachada", "que aguenta sol e chuva,", "começando do zero,"]
    visual: "flash de 1 s da fachada final pintada sob sol e chuva; corta para o reboco cru e o pintor de frente para a casa"
    camera: aberta
    animacao: idle
    ambiente: dia
  - id: 1
    tipo: degrau
    selo: "1 · Cal"
    narracao: ["pegue um balde,", "misture cal com água", "e passe na parede com uma broxa.", "A casa vai ficar branquinha,", "mas a cada chuva a cal vai lavando", "e manchando a parede."]
    visual: "pintor pega o balde e a broxa; a fachada fica branca; nuvem chega, chove, escorrem listras brancas e manchas"
    camera: media
    animacao: pegar
    animacao_nova: "pintar com broxa (caiação)"
    etiquetas: ["Cal + água"]
    objetos_novos: ["balde", "broxa"]
    ambiente: "dia → chuva"
  - id: 2
    tipo: degrau
    selo: "2 · Tinta PVA"
    narracao: ["Então, troque a cal", "por uma tinta látex PVA.", "A resina cola o pigmento na parede", "e a cor fica firme.", "Entretanto, essa tinta foi feita", "para dentro de casa:", "na fachada, ela absorve a chuva", "e começa a esfarelar."]
    visual: "lata PVA, fachada ganha a cor; chuva de novo; a superfície fica com pó e falhas"
    camera: media
    animacao: explicar
    etiquetas: ["Látex PVA", "Uso interno"]
    raio_x: "corte da tinta PVA: película porosa encharcando de água"
    objetos_novos: ["lata_pva"]
    ambiente: "dia → chuva"
  - id: 3
    tipo: degrau
    selo: "3 · Tinta acrílica"
    narracao: ["Para aguentar o tempo,", "use tinta acrílica.", "A resina acrílica forma uma película contínua", "que faz a água da chuva escorrer.", "Porém, passada direto no reboco,", "ela descasca em poucos meses.", "Agora você tem a tinta certa,", "mas ainda precisa de uma base firme."]
    visual: "gotas escorrem pela película; time-lapse de meses (calendário ou sol girando) e a tinta descasca em placas"
    camera: raio-x
    animacao: apontar
    etiquetas: ["Película acrílica"]
    raio_x: "gotas batendo e escorrendo na película; por baixo, pó solto no reboco"
    objetos_novos: ["lata_acrilica"]
    ambiente: "dia, time-lapse"
  - id: 4
    tipo: degrau
    selo: "4 · Lixa e selador"
    narracao: ["Antes de pintar, lixe a parede,", "escove todo o pó", "e aplique um selador acrílico.", "O selador entra nos poros do reboco", "e cria a base onde a tinta agarra.", "Mas existe um problema:", "a parede tem trincas finas,", "e a água entra por elas."]
    visual: "pintor lixa e escova (pó sobe); passa o selador; close numa trinca com gota entrando"
    camera: raio-x
    animacao: explicar
    animacao_nova: "lixar parede"
    etiquetas: ["Selador", "Poros do reboco"]
    raio_x: "selador penetrando nos poros e formando a base; água entrando pela trinca"
    objetos_novos: ["lixa", "escova", "lata_selador"]
    ambiente: dia
  - id: 5
    tipo: degrau
    selo: "5 · Trincas vedadas"
    narracao: ["Abra cada trinca em V,", "preencha com selante acrílico flexível", "e alise por cima.", "O selante estica e encolhe junto com a parede.", "Só que o sol esquenta a fachada de dia,", "a noite esfria,", "e novas fissuras fininhas continuam aparecendo."]
    visual: "trinca aberta em V e preenchida; ciclo dia → noite → dia com a parede 'respirando'; surgem fissuras finas em teia"
    camera: close
    animacao: pensar
    etiquetas: ["Selante flexível", "Fissuras"]
    objetos_novos: ["bisnaga_selante", "espatula"]
    ambiente: "dia → noite → dia"
  - id: 6
    tipo: degrau
    selo: "6 · Elastomérica"
    narracao: ["Então, finalize com tinta elastomérica,", "em demãos cruzadas.", "Ela forma uma camada grossa e elástica,", "como uma borracha,", "que estica por cima das fissuras sem rachar.", "Agora você tem uma fachada vedada,", "mas ainda precisa que ela dure."]
    visual: "rolo em demãos cruzadas; fachada fica com a cor final da House (creme e barrado azul); chuva escorre sem marcar"
    camera: raio-x
    animacao: joinha
    animacao_nova: "pintar com rolo"
    etiquetas: ["Elastomérica", "Demãos cruzadas"]
    raio_x: "camada elástica esticando por cima da fissura, sem romper"
    objetos_novos: ["rolo", "bandeja", "lata_elastomerica"]
    ambiente: "dia → chuva → sol"
  - id: 7
    tipo: degrau_final
    selo: "7 · Projeto da fachada"
    narracao: ["Mas não basta comprar a tinta mais cara", "e esperar que ela dure.", "Meça cada parede,", "considere o sol e a chuva", "que batem em cada lado da casa", "e dimensione a tinta, as demãos", "e o tempo de secagem.", "Faça isso com um pintor profissional.", "Assim, você terá uma fachada projetada", "para atender às necessidades da sua casa."]
    visual: "vista de cima da casa com a seta do sol e a da chuva; trena nas paredes; barras de HUD sobem"
    camera: aberta
    animacao: explicar
    hud: ["Sol", "Chuva", "Proteção"]
    etiquetas: ["Medição", "Demãos"]
    objetos_novos: ["trena", "prancheta"]
    ambiente: dia
  - id: 8
    tipo: recap
    narracao: ["E foi assim que você saiu", "de um balde de cal", "e chegou a uma fachada", "que aguenta sol e chuva."]
    visual: "câmera volta ao balde de cal no chão (primeira imagem), sobe e revela a fachada final"
    camera: media
    animacao: comemorar
  - id: 9
    tipo: cta
    narracao: ["Agora me diga:", "o que mais você quer aprender", "a construir do zero?", "Comente aqui embaixo", "e acompanhe o próximo vídeo!"]
    camera: close
    animacao: acenar
```

### Animações novas (fora da biblioteca padrão)

- **pintar com broxa**, **lixar parede** e **pintar com rolo**: procurar no Mixamo algo próximo ("Painting", "Wiping", "Scrubbing"); se não houver, usar `pegar` ou `explicar` com a ferramenta presa ao osso da mão e o movimento feito pelo código (IK do braço, como no reboco-novo).

### Variante de CTA (funil)

"Comenta FACHADA que eu te mando o passo a passo para escolher a tinta certa."

## Checklist

- [x] O gancho mostra o resultado final concreto em até 3 s (flash da fachada final)
- [x] Todo degrau termina com limitação, exceto o último
- [x] Conectores sem repetição seguida: mas · Entretanto · Porém · Mas existe um problema · Só que · (degrau 6 termina em respiro) · Mas não basta
- [x] 4 raio-x (PVA, acrílica, selador, elastomérica) e 1 HUD de barras
- [x] O recap cita o balde de cal
- [x] O CTA tem pergunta aberta
- [x] Sem marcas de tinta, sem personagem conhecido, sem promessa de resultado
- [x] Mecanismos simplificados e corretos; o degrau final manda fazer com um pintor profissional (fachada envolve altura e andaime)
