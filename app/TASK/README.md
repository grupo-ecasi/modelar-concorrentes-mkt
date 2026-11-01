# Tarefas: Agente de captura de criativos virais (Grupo Ecasi)

Este é o plano completo de `PLAN/plano-agente-virais.md`, dividido em tarefas pequenas.
**Execute uma tarefa por vez.** Cada uma tem objetivo, passos, critério de pronto e dependências.
Ao terminar uma tarefa, marque o status aqui e no arquivo dela.

| # | Tarefa | Fase | Depende de | Status |
|---|--------|------|------------|--------|
| 01 | Criar conta na Apify | Setup | — | ⬜ |
| 02 | Instalar plugin Apify e autenticar MCP | Setup | 01 | ⬜ |
| 03 | Teste do Instagram Scraper no @grupoecasi | Setup | 02 | ⬜ |
| 04 | Teste do TikTok Scraper | Setup | 02 | ⬜ |
| 05 | Estrutura de pastas e CLAUDE.md do projeto | Base | — | ⬜ |
| 06 | Mapa de nichos e hashtags (`config/nichos.json`) | Base | 05 | ⬜ |
| 07 | Skill e agente `descobrir-concorrentes` | Descoberta | 03, 04, 06 | ⬜ |
| 08 | Descoberta piloto: nicho SST | Descoberta | 07 | ⬜ |
| 09 | Descoberta dos demais nichos e lista final | Descoberta | 08 | ⬜ |
| 10 | Script de score viral (`scripts/score.py`) | Captura | 03, 04 | ⬜ |
| 11 | Skill e agente `capturar-virais` (coleta) | Captura | 09, 10 | ⬜ |
| 12 | Captura piloto em 3 concorrentes e conferência | Captura | 11 | ⬜ |
| 13 | Análise qualitativa do top 20 | Captura | 12 | ⬜ |
| 14 | Planilha de ranking (`ranking.xlsx`) | Relatórios | 12 | ⬜ |
| 15 | Dashboard HTML | Relatórios | 14 | ⬜ |
| 16 | Contexto de serviços do Ecasi (site) | Roteiros | 05 | ⬜ |
| 17 | Skill e agente `roteiros-ecasi` | Roteiros | 13, 16 | ⬜ |
| 18 | Rodada completa ponta a ponta + custos | Validação | 15, 17 | ⬜ |

Legenda: ⬜ pendente · 🟨 em andamento · ✅ concluída · ⛔ bloqueada

## Regras gerais para todas as tarefas
- Fonte de dados: **somente Apify** (Instagram + TikTok), no plano grátis (US$ 5/mês).
- **Antes de qualquer execução paga na Apify**, mostrar a estimativa de custo e pedir confirmação.
- Guardar só métricas públicas dos posts. **Não guardar dados de quem comenta (LGPD).**
- Textos e comentários em português. Nomes de arquivos, variáveis e funções em inglês ou kebab-case.
- Senhas e logins ficam com o usuário. O agente não digita credenciais.
