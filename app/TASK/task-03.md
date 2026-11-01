# task-03: Teste do Instagram Scraper no @grupoecasi

**Fase:** Setup · **Depende de:** task-02 · **Status:** ⬜

## Objetivo
Validar a coleta do Instagram e descobrir quais campos o Actor realmente devolve.

## Passos
1. Mostrar o custo estimado (5 posts, poucos centavos) e pedir confirmação.
2. Rodar `apify/instagram-scraper` no perfil `grupoecasi` com limite de **5 posts**.
3. Salvar o JSON bruto em `data/raw/teste/instagram-grupoecasi.json`.
4. Listar os campos úteis: tipo (Reel/carrossel/foto), curtidas, comentários, views/plays, data, legenda, URL, duração e seguidores do perfil.
5. Abrir o perfil no Chrome e conferir os números de 2 posts.

## Critério de pronto
- [ ] JSON salvo com 5 posts.
- [ ] Lista de campos documentada em `docs/campos-apify.md`.
- [ ] Números conferidos com o Instagram (diferença pequena, por causa do horário, é aceitável).
