# Vídeos virais animados — nicho Segurança do Trabalho (Instagram)

**Data da pesquisa:** 29/10/2026
**Ferramenta:** treg (API HTTP, conta `grupo-ecasi`)
**Objetivo:** encontrar Reels animados / motion graphics de Segurança do Trabalho que viralizaram e que possamos replicar.

> **Ressalva importante:** os vídeos animados com mais views do nicho **não são dos últimos dias**. Fora os dois do @raiox.tec (~15 dias), eles têm de 2 a 3 meses. O formato que mais viralizou nos últimos dias foi outro: vídeos **realistas feitos com IA** imitando câmera de segurança (ver seção no fim).

---

## Os 5 perfis

### 1. @raiox.tec — https://www.instagram.com/raiox.tec/

- **Estilo:** motion graphics em 3D low-poly, explicativo. Tem etiquetas e números na tela, barra de etapas no topo e legenda palavra por palavra.
- **Por que replicar:** é o mais próximo de motion graphics de verdade e o mais fácil de reproduzir.

| Vídeo | Views | Curtidas | Compart. | Data | Duração | Link |
|---|---|---|---|---|---|---|
| "E se o cabo do elevador arrebentar?" | 1.137.314 | 51.477 | — | 11/10/2026 | 85s | https://www.instagram.com/reel/DeXBQ4Yhu6h/ |
| "Choque no chuveiro pode matar?" (corrente, fio terra, DR 30 mA) | 212.330 | 12.652 | 1.821 | 13/10/2026 | 82s | https://www.instagram.com/reel/DecFNj3DeVk/ |

### 2. @hangar_treinamentos — https://www.instagram.com/hangar_treinamentos/

- **Estilo:** cartoon 2D ilustrado e animação de bonecos-palito.

| Vídeo | Views | Curtidas | Compart. | Data | Duração | Link |
|---|---|---|---|---|---|---|
| "Entenda a importância de usar óculos de proteção" | 802.503 | 18.006 | 4.169 | 11/08/2026 | 20s | https://www.instagram.com/reel/Db5-EcWAOni/ |
| Capacete (bonecos-palito) | 127.700 | 4.741 | 913 | 08/08/2026 | 20s | https://www.instagram.com/reel/Dbx_Gu7h2tH/ |

### 3. @teletoonzera — https://www.instagram.com/teletoonzera/

- **Estilo:** animação 2D de humor com um eletricista.

| Vídeo | Views | Curtidas | Compart. | Data | Duração | Link |
|---|---|---|---|---|---|---|
| Eletricista (humor) | 429.764 | 12.411 | 11.654 | 28/08/2026 | 15s | https://www.instagram.com/reel/DcmPYeqy4IP/ |

### 4. @rearouca (série ANIMASEG) — https://www.instagram.com/rearouca/

- **Estilo:** personagem 3D no estilo Pixar, falando sobre EPI.

| Vídeo | Views | Curtidas | Compart. | Data | Duração | Link |
|---|---|---|---|---|---|---|
| Óculos de proteção (ANIMASEG) | 100.504 | 6.609 | 1.324 | 21/08/2026 | 98s | https://www.instagram.com/reel/DcUIbOOO_Ge/ |

### 5. @ruannbpinho (mascote "Ruann TST") — https://www.instagram.com/ruannbpinho/

- **Estilo:** personagem 3D no estilo Pixar feito com IA, em série quase diária.
- **Observação:** tem poucas views, mas é o formato com mais posts recentes (vários nos últimos 5 dias).

| Vídeo | Views | Curtidas | Compart. | Data | Duração | Link |
|---|---|---|---|---|---|---|
| "A pior hora para errar é quando você está com pressa de ir embora" | 18.523 | 761 | 267 | 09/10/2026 | 121s | https://www.instagram.com/reel/DeRPtmTPemN/ |

---

## Outros animados encontrados (menor alcance)

| Perfil | Estilo | Views | Data | Link |
|---|---|---|---|---|
| @ddsnoinsta | 2D ilustrado — "Carga suspensa" | 15.651 | 08/10/2026 | https://www.instagram.com/reel/DePqostpM9w/ |
| @arrobamaiscursos | 3D técnico — "A importância da NR-35" | 9.496 | 18/09/2026 | https://www.instagram.com/reel/DdcRnu0NTqP/ |
| @mendes_treinamentos | Repost do vídeo dos óculos do @hangar_treinamentos | 8.025 | 03/10/2026 | https://www.instagram.com/reel/DeC1qPQp2vD/ |

---

## O que mais viralizou nos últimos dias

São vídeos realistas feitos com IA, imitando câmera de segurança. **Não são motion graphics**, mas servem de referência de formato.

| Perfil | Tema | Views | Data | Link |
|---|---|---|---|---|
| @secaf.adv | "Jogou gelo no óleo quente" | 8.506.441 | 13/09/2026 | https://www.instagram.com/reel/DdPcnpASZNQ/ |
| @ats_treinamentos | Queda em trabalho em altura | 426.195 | 27/10/2026 | https://www.instagram.com/reel/DfAC3KUxZmo/ |

---

## Como a pesquisa foi feita

- A CLI do treg não está instalada nesta máquina. A pesquisa usou a conta e o token já salvos em `~/.treg/config.json`, chamando a API do treg diretamente.
- Foram feitas mais de 40 buscas de Reels com termos do nicho (segurança do trabalho, EPI, NR-35, NR-10, CIPA, SIPAT, animação 3D, desenho animado etc.). Também foram consultados os Reels recentes dos perfis que produzem animação.
- Para separar o que é animação do que é filmagem real, os frames dos vídeos foram conferidos visualmente.
- **Custo total:** cerca de US$ 0,07. O saldo ficou em US$ 0,93.
- **Limitação:** a busca de Reels ordena por relevância, não por tendência. Por isso pode haver vídeos animados virais que não apareceram.

## Próximo passo sugerido

Decupar o vídeo do chuveiro do @raiox.tec (roteiro, ritmo e cenas) e montar a nossa versão no mesmo estilo de motion graphics.
