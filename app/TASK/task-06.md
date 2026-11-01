# task-06: Mapa de nichos e hashtags (`config/nichos.json`)

**Fase:** Base · **Depende de:** task-05 · **Status:** ⬜

## Objetivo
Definir os termos de busca de cada nicho, que o agente descobridor vai usar.

## Passos
1. Criar `config/nichos.json` com os 6 nichos. Cada nicho tem hashtags do Instagram, hashtags do TikTok e palavras-chave para a bio:
   - SST: `segurancadotrabalho, sst, tecnicoemsegurancadotrabalho, nr35, nr10, nr12, epi`
   - Saúde ocupacional: `saudeocupacional, medicinadotrabalho, pcmso, esocial`
   - Engenharia civil: `engenhariacivil, obras, construcaocivil`
   - Engenharia elétrica: `engenhariaeletrica, nr10, eletricista`
   - Incêndio: `avcb, prevencaodeincendio, brigadadeincendio, combateaincendio`
   - Ambiental: `licenciamentoambiental, engenhariaambiental, meioambiente`
2. Incluir os parâmetros padrão: posts por hashtag, mínimo de seguidores (5 mil) e janela de atividade (30 dias).
3. O usuário revisa e ajusta as hashtags.

## Critério de pronto
- [ ] `config/nichos.json` válido (JSON) e aprovado pelo usuário.
