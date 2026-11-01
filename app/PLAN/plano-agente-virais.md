# Plano: Agente de captura de criativos virais — Grupo Ecasi

## Contexto
O Grupo Ecasi (www.grupoecasi.com.br, @grupoecasi) quer crescer no Instagram (e TikTok) estudando o que viraliza nos concorrentes dos nichos: SST/segurança do trabalho, saúde ocupacional, engenharia civil, engenharia elétrica, incêndio e ambiental — escopo **Brasil todo**.
O repositório `C:\app.Modelar-Concorrentes-MKT\app` está vazio. Node 24, Python 3.12 e Claude Code 2.1.312 já estão instalados.

Decisões já tomadas com o usuário:
- **Fonte de dados: somente treg** (substitui a Apify). O treg já está instalado e autenticado nesta máquina e já foi usado em 29/10/2026 na pesquisa `relatorio-virais-seguranca-trabalho-2026-10-29.md`. Instagram + TikTok.
- **Dois agentes:** um que **descobre** os concorrentes (o usuário ainda não conhece os perfis) e outro que **pesquisa e ranqueia** os criativos.
- **Entregas:** relatório sob demanda + dashboard/planilha + ideias de roteiro prontas para o Ecasi.

Situação do treg (conferida em 30/10/2026):
- CLI `treg` v0.27.0 em `%APPDATA%\Python\Python312\Scripts\treg.exe`, configuração em `~/.treg/config.json`.
- Conta `tecnologiagrupoecasi@gmail.com`, time `grupo-ecasi` (owner), saldo de **US$ 0,93**. Recarga com `treg topup` ou no dashboard (Team → Billing).
- A credencial fica no servidor do treg. Nenhum token ou chave vai para o repositório.

Limitações que o design precisa respeitar:
- **Instagram:** salvamentos de posts de terceiros **não são públicos**. Compartilhamentos às vezes vêm em Reels (vieram em parte dos posts do relatório de 29/10), mas não dá para contar com isso. Por isso o Score usa métricas indiretas e só usa compartilhamentos quando existirem.
- **TikTok:** shares e saves (collects) **são públicos**, então ali a medição é direta.
- **Custo:** o treg cobra **por chamada bem-sucedida** (uma página de resultados), não por item. Falha não é cobrada. Preços de partida das ferramentas roteadas:

  | Ferramenta treg | Uso | Preço de partida |
  |---|---|---|
  | `treg.instagram.user.profile` | perfil (seguidores, bio) | US$ 0,0009/chamada |
  | `treg.instagram.user.posts` | últimos posts do perfil | US$ 0,0009/chamada |
  | `treg.instagram.user.reels` | últimos Reels do perfil (com views) | US$ 0,0009/chamada |
  | `treg.instagram.hashtag.posts` | posts de uma hashtag | US$ 0,00188/chamada |
  | `treg.instagram.search.users` / `search.reels` | busca por palavra-chave | US$ 0,0015–0,00188/chamada |
  | `treg.tiktok.user.profile` | perfil (seguidores, secUid) | US$ 0,00035/chamada |
  | `treg.tiktok.user.videos` | últimos vídeos (por secUid) | US$ 0,0005/chamada |
  | `treg.tiktok.search.videos` / `search.users` | busca por palavra-chave | US$ 0,001/chamada |
  | `tikhub.tiktok.hashtag.videos` | vídeos de uma hashtag (por challengeID) | US$ 0,001/chamada |

  As ferramentas `treg.*` são **roteadas**: o treg escolhe o provedor mais barato e, se ele falhar, tenta o próximo, que pode ser mais caro. Por isso toda chamada sai com o cabeçalho `X-Treg-Route-Max-Cost: 0.05`, que impede uma chamada de passar de US$ 0,05.
  Uma rodada com 20 concorrentes custa da ordem de **US$ 0,05–0,15**. A skill estima o custo antes de cada rodada, pede confirmação e soma o `X-Treg-Cost-Micro` de cada resposta para reportar o total real.

## Etapa 1 — Verificar o treg (sem conta nova, sem plugin)
1. Rodar `treg` e conferir conta, time `grupo-ecasi` e saldo. Se o saldo estiver baixo, **você** recarrega com `treg topup`. Eu não digito dados de pagamento.
2. Conferir preços e parâmetros atuais com `treg catalog get <id>` para cada ferramenta da tabela acima. Os parâmetros são os do provedor que respondeu, então o `score.py` precisa normalizar os campos.
3. Teste rápido: `treg --json call treg.instagram.user.posts` em @grupoecasi e conferir os números com o perfil real.
4. No Windows, os corpos JSON vão por arquivo (`--data @body.json`), porque o PowerShell remove as aspas internas de JSON inline.

## Etapa 2 — Estrutura do projeto
```
app/
  CLAUDE.md                          # contexto do Ecasi, nichos, regras de custo/LGPD
  .claude/agents/
    descobridor-concorrentes.md      # subagente de descoberta
    cacador-virais.md                # subagente de captura + análise
  .claude/skills/
    descobrir-concorrentes/SKILL.md
    capturar-virais/SKILL.md         # skill principal
    roteiros-ecasi/SKILL.md          # transforma padrões virais em roteiros
  config/
    nichos.json                      # hashtags/termos PT-BR por nicho
    concorrentes.json                # lista aprovada (handle, rede, nicho, seguidores, secUid do TikTok)
  scripts/
    treg_client.py                   # chama `treg --json call`, aplica teto de custo e soma o gasto
    normalize.py                     # converte as respostas dos vários provedores num formato único
    score.py                         # calcula scores a partir dos dados normalizados
    build_report.py                  # gera planilha (.xlsx/.csv) + dashboard HTML
  data/raw/AAAA-MM-DD/               # respostas brutas do treg (com provedor e call id)
  relatorios/                        # ranking.xlsx, dashboard.html, roteiros.md
```
As skills são criadas com o `skill-creator` e os textos ficam em português, com nomes de arquivos em inglês ou kebab-case.

`scripts/treg_client.py`:
- Usa `treg --json call <id> --data @arquivo.json --header "X-Treg-Route-Max-Cost: 0.05"`. A saída é uma linha `{"result": ..., "_treg": {"http_status", "call_id", "charged_micro"}}`.
- Grava o resultado bruto, o provedor que respondeu (`_treg.served_by`) e o `call_id` em `data/raw/`.
- Mantém a soma do gasto e para antes de passar do valor que você aprovou.
- Erro 4xx: corrige a requisição, sem tentar outro provedor. Erro 429/5xx: tenta o próximo provedor e registra qual.
- Testa com 2–3 perfis antes de rodar a lista toda, porque um erro de parsing joga fora respostas já pagas.

## Etapa 3 — Agente descobridor (`descobrir-concorrentes`)
- `config/nichos.json` traz os termos por nicho. Exemplos:
  - SST: `#segurancadotrabalho #sst #tecnicoemsegurancadotrabalho #nr35 #nr10 #nr12 #epi`
  - Saúde ocupacional: `#saudeocupacional #medicinadotrabalho #pcmso #esocial`
  - Civil: `#engenhariacivil`
  - Elétrica: `#engenhariaeletrica #nr10`
  - Incêndio: `#avcb #prevencaodeincendio #brigadadeincendio`
  - Ambiental: `#licenciamentoambiental #engenhariaambiental`
- Fluxo:
  1. Coletar candidatos por dois caminhos:
     - **Hashtag:** `treg.instagram.hashtag.posts` e `tikhub.tiktok.hashtag.videos`, com uma página por hashtag para economizar.
     - **Palavra-chave:** `treg.instagram.search.users`, `treg.instagram.search.reels`, `treg.tiktok.search.users` e `treg.tiktok.search.videos` (ex.: "segurança do trabalho", "técnico em segurança", "NR 35").
  2. Agregar os autores.
  3. Buscar os perfis com `treg.instagram.user.profile` e `treg.tiktok.user.profile`.
  4. Filtrar: conta brasileira, seguidores ≥ ~5 mil, postou nos últimos 30 dias, conteúdo do nicho (o Claude classifica pela bio e pelas legendas).
- Saída: uma tabela de candidatos (nicho, seguidores, média de views, por que é relevante). **Você aprova**, e só então eles entram em `config/concorrentes.json`. O @grupoecasi também entra, como baseline.
- Ponto de partida: os perfis do relatório de 29/10 (@raiox.tec, @hangar_treinamentos, @teletoonzera, @rearouca, @ruannbpinho) entram direto como candidatos.

## Etapa 4 — Agente caçador de virais (`capturar-virais`)
- Para cada concorrente aprovado, buscar os últimos N posts (padrão 12, configurável):
  - Instagram: `treg.instagram.user.reels` (views dos Reels) e `treg.instagram.user.posts` (carrosséis e fotos).
  - TikTok: `treg.tiktok.user.videos`, usando o `secUid` guardado em `concorrentes.json`.
  - Antes de rodar, mostrar o custo estimado (número de chamadas × preço) e pedir confirmação.
- Salvar o bruto em `data/raw/<data>/` e normalizar com `scripts/normalize.py`. Guardar só dados públicos de cada post. **Não guardar dados de quem comenta (LGPD)**, então as ferramentas de comentários não são usadas.
- `scripts/score.py` calcula:
  - **Reels/vídeo:** `views ÷ seguidores`, **outlier** (`views ÷ mediana de views do próprio perfil`) e `(curtidas + comentários) ÷ views`. Se vier contagem de compartilhamentos, entra também `compartilhamentos ÷ views`.
  - **Carrossel/foto:** `(curtidas + comentários) ÷ seguidores` e o outlier sobre a mediana de curtidas do perfil.
  - **TikTok:** share rate e save rate diretos (`shares ÷ views`, `collects ÷ views`), mais o outlier.
  - **Score viral final:** combinação ponderada, com o outlier pesando mais, que é o melhor sinal de "o algoritmo empurrou esse post".
- Depois o Claude analisa o top 20 por:
  - gancho (primeira frase da legenda/texto)
  - formato e duração (incluindo o estilo visual: animação 2D, 3D, motion graphics, vídeo realista com IA, gravação real)
  - tema (NR, multa, acidente, mito × verdade, bastidor)
  - tipo de CTA ("salva", "manda pra alguém", "comenta")
  - motivo provável do compartilhamento
- `scripts/build_report.py` gera:
  - `relatorios/ranking.xlsx` (com links para os posts)
  - `relatorios/dashboard.html`: filtros por nicho, rede e formato. Opcionalmente eu publico como Artifact privado para compartilhar com a equipe.

## Etapa 5 — Roteiros (`roteiros-ecasi`)
A partir dos padrões do top ranking, gerar 5–10 roteiros adaptados aos serviços do Ecasi. O contexto vem de uma leitura do site. Cada roteiro traz:
- gancho dos primeiros 3 segundos
- estrutura cena a cena (Reels) ou slide a slide (carrossel)
- legenda e CTA de salvar/compartilhar
- referência ao post concorrente que inspirou o roteiro

Saída: `relatorios/roteiros-AAAA-MM-DD.md`.

## Uso no dia a dia
- "descobrir concorrentes" (rodar de vez em quando)
- "capturar virais" → ranking + dashboard
- "gerar roteiros"

Os agentes são chamados pelas skills ou direto pelo nome.

## Verificação
1. Teste do treg: a chamada devolve os posts do @grupoecasi e as contagens conferem com o perfil aberto no Chrome.
2. Descoberta em 1 nicho (SST) com poucas chamadas: a lista de candidatos faz sentido para você.
3. Captura em 3 concorrentes: conferir à mão 2–3 posts (views, curtidas, comentários) contra o Instagram e o TikTok. Conferir também que respostas de provedores diferentes foram normalizadas para os mesmos campos.
4. Rodar `python scripts/score.py` e `build_report.py`, abrir `dashboard.html` e o `.xlsx` e conferir que o top tem outliers reais.
5. Conferir o gasto com `treg balance` depois dos testes e comparar com a soma registrada pelo `treg_client.py`.
