# task-10: Script de score viral (`scripts/score.py`)

**Fase:** Captura · **Depende de:** task-03, task-04 · **Status:** ⬜

## Objetivo
Calcular o "score viral" de cada post a partir do JSON bruto da Apify.

## Passos
1. Criar `scripts/score.py` (Python 3.12, sem dependências pesadas). Ele lê `data/raw/<data>/*.json` e gera `data/processed/<data>/posts.csv`.
2. Métricas:
   - **Reels/vídeo IG:** `views/seguidores`, `outlier = views / mediana de views do perfil` e `(curtidas+comentários)/views`.
   - **Carrossel/foto IG:** `(curtidas+comentários)/seguidores` e o outlier sobre a mediana de curtidas do perfil.
   - **TikTok:** `shares/views`, `collects/views` e o outlier.
   - **Score final:** pesos configuráveis no topo do script, com o outlier pesando mais.
3. Testar com os JSONs de `data/raw/teste/` (task-03 e task-04).

## Critério de pronto
- [ ] Script roda sem erro nos dados de teste.
- [ ] CSV com uma linha por post e as colunas de score.
- [ ] Cálculo conferido à mão em 1 post.
