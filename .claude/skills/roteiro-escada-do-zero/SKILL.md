---
name: "roteiro-escada-do-zero"
description: "Escreve roteiros de vídeo de bonequinho 3D no formato Escada do Zero (gancho, degraus com 'mas', raio-x, recap, CTA, loop). Use para roteiro, gancho ou decupagem desses vídeos."
---

# Roteiro "Escada do Zero"

Formato de vídeo vertical narrado, com um bonequinho 3D como protagonista. O personagem constrói algo do zero, degrau por degrau, e cada degrau resolve a limitação do anterior. Serve para qualquer nicho que tenha uma evolução natural do primitivo ao completo.

O narrador fala com o espectador ("você") no imperativo, e o bonequinho executa na tela o que o narrador manda.

## 1. Teste do tema (antes de escrever)

O tema só passa se der para listar de 5 a 7 degraus em que:
1. o primeiro é algo que qualquer pessoa faria com as mãos (balde, manivela, panela, fogueira);
2. cada degrau tem uma limitação concreta e fácil de mostrar;
3. o último é o sistema completo e profissional que o espectador reconhece da vida real.

Se não passar, proponha um tema vizinho que passe e explique em uma linha por quê.

Exemplos que passam: energia elétrica, água encanada, banho quente, iluminação, internet em casa, irrigação de horta, refrigeração, aquecimento, segurança da casa, esgoto, telhado, forno de pão.

## 2. Estrutura (ordem fixa)

1. **Gancho (0–3 s).** "Se você quiser [resultado final concreto] [para sua casa / no seu negócio], começando do zero,"
   - O resultado final é desejável e visual. Nunca revele o caminho no gancho.
2. **Degrau 1, o primitivo.** Ação no imperativo e um resultado pequeno e visível: "pegue uma manivela… Você verá uma lâmpada acender,"
3. **Virada.** Conector + limitação: "mas isso ainda está muito longe de alimentar uma casa inteira!"
4. **Degraus do meio (2 a N-1).** Sempre no padrão:
   - Ponte: "Então," / "Para [superar a limitação],"
   - Ação no imperativo: pegue, conecte, instale, substitua, acrescente, ligue
   - Mecanismo: 1 ou 2 frases sobre por que funciona (é aqui que entra o raio-x)
   - Ganho: o que melhorou
   - Nova limitação (virada)
   - A cada 2 ou 3 degraus, use a frase de respiro: "Agora você tem [X], mas ainda precisa [Y]."
5. **Degrau final, o "profissional".** "Mas não basta [instalar X] e esperar que [funcione]." Depois: "Calcule…, considere… e dimensione…" e por fim: "Assim, você terá um sistema projetado para atender às necessidades da [casa / família / empresa]."
6. **Fechamento (recap).** "E foi assim que você saiu de [objeto do degrau 1] e chegou a [resultado final]."
7. **CTA.** "Agora me diga: o que mais você quer aprender a construir do zero? Comente aqui embaixo e acompanhe o próximo vídeo!"
   - Variante de funil (ManyChat): "Comenta [PALAVRA] que eu te mando [isca]."
8. **Loop.**
   - Padrão (por retorno): no recap, a câmera volta ao objeto do degrau 1, que é a primeira imagem do vídeo.
   - Costurado (opcional): a última frase fica aberta e emenda no gancho. Exemplo: "…e acompanhe o próximo vídeo, porque tudo começa do mesmo jeito:" e corta para "Se você quiser…".

### Conectores de virada

Use em rodízio e nunca repita o mesmo duas vezes seguidas: "Mas", "Entretanto,", "Porém,", "Mas existe um problema:", "Só que", "Mas isso ainda está muito longe de…", "Porém, [X] não resolve tudo:".

## 3. Ritmo e tamanho

| Versão | Degraus | Duração | Palavras |
|---|---|---|---|
| Longa (padrão) | 6 a 8 | 2:00 a 2:40 | ~300 a 380 |
| Curta | 4 a 5 | 60 a 80 s | ~150 a 190 |

- Uma virada a cada 10 a 15 s. Cada degrau dura de 12 a 22 s.
- Frases curtas, de até ~10 palavras. A legenda quebra em blocos de 3 a 5 palavras.
- Vocabulário leigo. O termo técnico aparece como etiqueta na tela, não como explicação longa.
- Na versão curta, o degrau "profissional" é opcional.

## 4. Gramática visual (anotar no roteiro)

- **Cenário único que acumula.** Todo objeto instalado continua na cena até o fim. O espectador vê a casa "crescer".
- **Selo numerado no topo** a cada degrau: "N · Nome do degrau" (1 a 4 palavras).
- **Etiquetas** apontando peças, de 1 a 3 palavras e de 1 a 3 por degrau.
- **Raio-x (corte)** mostrando o mecanismo por dentro em pelo menos 2 degraus.
- **Barras de HUD** no degrau final, 3 barras (ex.: Consumo / Sol da região / Geração).
- **Mudança de ambiente** quando a limitação é de tempo ou clima: dia → noite, nuvens, vento parando.
- **Close no rosto** do personagem no CTA, olhando para a câmera.
- **Animações do personagem**: use só nomes da biblioteca padrão (skill bonequinho-3d): idle, andar, apontar, acenar, explicar, pensar, joinha, comemorar, olhar_em_volta, pegar, sentado. Se precisar de outra, sinalize como "animação nova".

## 5. Precisão e segurança

- Todo mecanismo explicado precisa estar tecnicamente correto. Na dúvida, simplifique em vez de inventar.
- Em temas com risco (eletricidade da rede, gás, estrutura, água para beber), o degrau final inclui "com um profissional habilitado" ou equivalente. Nunca ensine um procedimento perigoso como faça-você-mesmo.
- Sem promessa de resultado financeiro ou de saúde. Sem marcas nem personagens conhecidos.

## 6. Formato de saída

Entregue sempre as 3 partes:

**A. Resumo.** Tema, resultado final, lista de selos, duração estimada e contagem de palavras.

**B. Narração limpa.** Só o texto falado, uma frase por linha, com [N] marcando o início de cada degrau. Pronta para o TTS.

**C. Decupagem em YAML** para o pipeline de render:

```yaml
titulo: "Energia para sua casa do zero"
personagem: <slug do personagem>
cenario_base: "casa térrea, quintal, rua"
duracao_alvo_s: 150
loop: retorno   # retorno | costurado
cenas:
  - id: 0
    tipo: gancho
    narracao: ["Se você quiser gerar energia", "para sua casa, começando do zero,"]
    visual: "plano aberto da casa, personagem no quintal"
    camera: aberta          # aberta | media | close | raio-x
    animacao: idle
  - id: 1
    tipo: degrau
    selo: "1 · Manivela"
    narracao: ["pegue uma manivela,", "conecte-a a um pequeno gerador", "e comece a girar."]
    visual: "personagem gira a manivela, lâmpada acende"
    camera: media
    animacao: pegar
    etiquetas: ["Manivela"]
    raio_x: "ímãs e bobinas dentro do gerador"
    objetos_novos: ["mesa", "gerador", "lampada"]   # ficam nas cenas seguintes
    ambiente: dia
  - id: 9
    tipo: cta
    narracao: ["Agora me diga:", "..."]
    camera: close
    animacao: explicar
```

## 7. Checklist final (rode antes de entregar)

- [ ] O gancho mostra o resultado final concreto em até 3 s
- [ ] Todo degrau termina com limitação, exceto o último
- [ ] Nenhum conector de virada repetido em sequência
- [ ] Pelo menos 2 raio-x e 1 HUD de barras (versão longa)
- [ ] O recap cita pelo nome o objeto do degrau 1
- [ ] O CTA tem pergunta aberta
- [ ] A contagem de palavras está dentro da faixa da versão
- [ ] Sem marcas, personagens conhecidos ou promessa de resultado
- [ ] Os mecanismos estão corretos; os temas de risco citam um profissional

## 8. Exemplo de referência (versão curta)

```
Se você quiser água encanada na sua casa, começando do zero,
[1] pegue um balde e vá até o rio.
Você terá água para cozinhar,
mas cada litro custa uma caminhada.
[2] Então, cave um poço perto da casa
até alcançar o lençol freático.
Entretanto, ainda vai puxar balde por balde!
[3] Substitua o balde por uma bomba manual.
A cada movimento da alavanca,
o pistão cria sucção
e a água sobe pelo cano.
Mas existe um problema:
a água só sai enquanto você bombeia.
[4] Bombeie para uma caixa d'água no alto da casa
e deixe a gravidade levar a água até as torneiras.
Porém, encher a caixa à mão continua cansativo.
[5] Instale uma bomba elétrica e uma boia:
quando o nível baixa, a bomba liga sozinha;
quando a caixa enche, ela desliga.
E foi assim que você saiu de um simples balde
e chegou à água encanada na sua casa.
Agora me diga: o que mais você quer aprender a construir do zero?
Comente aqui embaixo e acompanhe o próximo vídeo!
```