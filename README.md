# Marketing — vídeos e pesquisa de concorrentes

Índice do repositório. Cada pasta de vídeo é um projeto HyperFrames completo: `index.html`, `compositions/`, `assets/` (narração, sons e marca), `tools/` (scripts de sincronia e mixagem), `renders/` (MP4 final e capa) e a legenda do Instagram.

## Estrutura

```
app/                         Agente de captura de criativos virais (plano e tarefas)
ecasi/                       Grupo ECASI
  series/
    energia-eletrica/        Série Energia Elétrica (4 Reels, entregue em 31/10/2026)
      plano-serie-energia-eletrica.md
      ep1-morador/           "Vai trocar a resistência do chuveiro?"
      ep2-residencial/       "Terminou o quadro. Pode entregar?"
      ep3-industrial/        "Desligou o inversor. Já pode abrir?"
      ep4-media-tensao/      "Abriu a seccionadora. Já pode encostar?"
  videos/
    nr10-chuveiro/           Reel NR-10 (base viral da série, decupagem do @raiox.tec)
    nr35-altura/             Reel NR-35 trabalho em altura
    nr01-gestora/            Roteiro do talking head de NR-01 (a gestora grava)
  pesquisa/                  Relatórios de virais (segurança do trabalho, NR-01)
house/                       House Pinturas (@house_pintura10)
  series/
    massa/
      parte1-massa-corrida/  Luz rasante: massa corrida interna
      parte2-massa-externa/  Massa na área externa
  videos/
    sacada-madeira/          Antes e depois da sacada de madeira
    mofo-bonequinho/         Mofo na parede (low-poly)
  pesquisa/                  Relatório de virais de pintura
```

## Onde estão os arquivos de cada vídeo

| Arquivo | Onde fica |
|---|---|
| Roteiro e texto da narração | `.md` na raiz do projeto (`narracao-*.md` ou `roteiro-*.md`) |
| Áudio da narração | `assets/narracao-*.mp3` (original) e `assets/narracao-norm.mp3` (normalizado) |
| Vídeo final e capa | `renders/` |
| Legenda do Instagram | `legenda-instagram*.md` / `.txt` |

## Entregas

Os vídeos prontos da Série Energia Elétrica também ficam copiados na Área de Trabalho, na pasta `serie eletrica insta` (vídeo, capa e legenda de cada episódio).

## Comandos úteis (dentro da pasta de um projeto)

```bash
npx --yes hyperframes@0.8.217 check                 # valida o projeto
npx --yes hyperframes@0.8.217 snapshot --at 1,5,10  # quadros para revisar
npx --yes hyperframes@0.8.217 render -o renders/video.mp4
```
