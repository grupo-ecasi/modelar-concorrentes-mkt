# task-07: Skill e agente `descobrir-concorrentes`

**Fase:** Descoberta · **Depende de:** task-03, task-04, task-06 · **Status:** ⬜

## Objetivo
Criar a skill e o subagente que encontram perfis concorrentes por nicho.

## Passos
1. Criar `.claude/skills/descobrir-concorrentes/SKILL.md` com o `skill-creator`. Fluxo:
   1. Ler `config/nichos.json` e aceitar o nicho como argumento.
   2. Estimar o custo e pedir confirmação.
   3. Rodar os hashtag scrapers (Instagram e TikTok) com poucos posts por hashtag.
   4. Agregar os autores e rodar o profile scraper neles.
   5. Filtrar: Brasil, ≥ 5 mil seguidores, ativo nos últimos 30 dias, conteúdo do nicho (o Claude classifica pela bio e pelas legendas).
   6. Gerar a tabela de candidatos em `relatorios/candidatos-<nicho>-<data>.md`.
   7. **Não** gravar em `concorrentes.json` sem aprovação.
2. Criar `.claude/agents/descobridor-concorrentes.md`, o subagente que executa essa skill.

## Critério de pronto
- [ ] Skill e agente criados e listados no Claude Code.
- [ ] Teste a seco (sem rodar a Apify) explica corretamente o fluxo.
