# task-11: Skill e agente `capturar-virais` (coleta)

**Fase:** Captura · **Depende de:** task-09, task-10 · **Status:** ⬜

## Objetivo
Criar a skill principal, que coleta os posts recentes dos concorrentes aprovados e roda o score.

## Passos
1. Criar `.claude/skills/capturar-virais/SKILL.md` com o `skill-creator`. Fluxo:
   1. Ler `config/concorrentes.json`. Aceitar filtros por nicho e rede e o N de posts (padrão 12).
   2. Calcular o custo estimado (perfis × N × preço/1 mil) e pedir confirmação.
   3. Rodar os Actors do Instagram e do TikTok e salvar em `data/raw/<data>/`.
   4. Remover dados de quem comenta antes de salvar (LGPD).
   5. Rodar `scripts/score.py`.
2. Criar `.claude/agents/cacador-virais.md`, o subagente que executa a skill.

## Critério de pronto
- [ ] Skill e agente criados e listados.
- [ ] A estimativa de custo aparece antes de qualquer execução.
