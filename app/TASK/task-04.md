# task-04: Teste do TikTok Scraper

**Fase:** Setup · **Depende de:** task-02 · **Status:** ⬜

## Objetivo
Validar a coleta do TikTok e confirmar que **shares** e **saves (collects)** vêm nos dados.

## Passos
1. Verificar se o Grupo Ecasi tem perfil no TikTok. Se não tiver, usar um perfil público de SST.
2. Mostrar o custo estimado e pedir confirmação.
3. Rodar o TikTok Scraper (`clockworks`) com limite de **5 vídeos**.
4. Salvar em `data/raw/teste/tiktok-<perfil>.json`.
5. Documentar os campos: plays, curtidas, comentários, shares, collects, duração, legenda e URL.

## Critério de pronto
- [ ] JSON salvo com 5 vídeos.
- [ ] Campos `shareCount` e `collectCount` (ou equivalentes) confirmados.
- [ ] Campos documentados em `docs/campos-apify.md`.
