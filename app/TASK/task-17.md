# task-17: Skill e agente `roteiros-ecasi`

**Fase:** Roteiros · **Depende de:** task-13, task-16 · **Status:** ⬜

## Objetivo
Transformar os padrões virais em roteiros prontos para o Ecasi gravar ou publicar.

## Passos
1. Criar `.claude/skills/roteiros-ecasi/SKILL.md` com o `skill-creator`. Fluxo:
   1. Ler a análise mais recente (`relatorios/analise-*.md`) e `docs/ecasi-contexto.md`.
   2. Gerar 5 a 10 roteiros. Cada roteiro traz:
      - formato (Reels ou carrossel)
      - gancho dos 3 primeiros segundos
      - cenas ou slides
      - texto na tela
      - legenda
      - CTA de salvar/compartilhar
      - hashtags
      - post concorrente que inspirou o roteiro (link)
   3. Salvar em `relatorios/roteiros-<data>.md`.
2. Opcional: criar o agente `.claude/agents/roteirista-ecasi.md`.

## Critério de pronto
- [ ] Roteiros gerados a partir da captura piloto.
- [ ] O usuário considera pelo menos 3 roteiros prontos para produzir.
