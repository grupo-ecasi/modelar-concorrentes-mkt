# task-15: Dashboard HTML

**Fase:** Relatórios · **Depende de:** task-14 · **Status:** ⬜

## Objetivo
Ter uma visão visual e rápida dos virais para a equipe.

## Passos
1. Estender `scripts/build_report.py` para gerar `relatorios/dashboard.html` em arquivo único, sem servidor. Ele mostra:
   - cards do top 10 (miniatura, perfil, score, link)
   - filtros por nicho, rede e formato
   - gráfico de score por nicho e formato
   - comparação Ecasi × média do mercado
2. Opcional: publicar como Artifact privado no claude.ai para compartilhar com a equipe (só com aprovação do usuário).

## Critério de pronto
- [ ] `dashboard.html` abre no navegador e os filtros funcionam.
- [ ] Funciona no celular (largura pequena).
