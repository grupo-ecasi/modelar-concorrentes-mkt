# task-02: Instalar plugin Apify e autenticar MCP

**Fase:** Setup · **Depende de:** task-01 · **Status:** ⬜

## Objetivo
Deixar o Claude Code deste projeto com acesso à Apify pelo plugin oficial.

## Passos
1. Instalar o plugin com os comandos abaixo. Se a versão em CLI (`claude plugin ...`) não funcionar, o usuário digita os comandos no prompt.
   - `/plugin marketplace add apify/apify-claude-code-plugin`
   - `/plugin install apify@apify`
   - `/reload-plugins`
2. Rodar `/mcp` → `plugin:apify:apify` → **Authenticate**. O login é OAuth no navegador, sem colar token.
3. Confirmar que as ferramentas da Apify aparecem (buscar Actor, rodar Actor, ler dataset).

## Critério de pronto
- [ ] Plugin `apify` instalado e listado.
- [ ] MCP da Apify autenticado (status "connected").
- [ ] Uma busca simples no Apify Store funciona (ex.: "instagram scraper").

## Referência
https://docs.apify.com/agents/plugins.md
