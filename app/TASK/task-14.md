# task-14: Planilha de ranking (`ranking.xlsx`)

**Fase:** Relatórios · **Depende de:** task-12 · **Status:** ⬜

## Objetivo
Gerar uma planilha que a equipe de marketing possa filtrar.

## Passos
1. Criar `scripts/build_report.py`, que lê `data/processed/<data>/posts.csv`.
2. Gerar `relatorios/ranking-<data>.xlsx` (com `openpyxl`; se não houver, CSV):
   - aba **Top virais** (ordenada por score, com o link clicável do post)
   - aba **Por nicho**
   - aba **Por perfil** (médias e mediana)
   - aba **Ecasi vs mercado** (baseline @grupoecasi)
3. Incluir as colunas da análise qualitativa (gancho, tema, CTA), quando existirem.

## Critério de pronto
- [ ] A planilha abre no Excel com links funcionando.
- [ ] Os filtros por nicho, rede e formato funcionam.
