# Componentes 3D

Biblioteca de objetos 3D (Three.js) reaproveitáveis nos vídeos da **ECASI** (segurança do trabalho, engenharia, incêndio e saúde ocupacional) e da **House** (pintura). Cresce um vídeo de cada vez: quando um vídeo precisar de um objeto novo, ele é criado aqui, não dentro do projeto.

## Arquivos

| Módulo | O que tem |
|---|---|
| `nucleo.js` | `PALETA` (House, ECASI, natureza, flores, vivas), `mat`, `rnd`, `sm`, `lerp`, `pop` e `aplicarPop` (entrada com mola), `sombras`, `palco` (renderer + luz padrão), `texturaCanvas` |
| `cenario.js` | `ceu`, `sol`, `nuvem`, `arvore`, `arbusto`, `canteiro`, `cerca`, `casaVizinha`, `chao`, `calcada`, `rua`, `poste`, `caixaCorreio`, `vaso`, `passaros` |
| `props-pintura.js` | `lata`, `balde`, `broxa`, `rolo`, `bandeja`, `lixa`, `espatula`, `bisnaga`, `escada`, `lona`, `fitaCrepe` |
| `props-seguranca.js` | `capacete`, `colete`, `cone`, `extintor`, `placa` (aviso, proibido, obrigatório, saída), `maletaPrimeirosSocorros`, `quadroEletrico`, `luvas`, `oculosProtecao`, `prancheta` (checklist com `userData.marcar(n)`), `tambor` (produto químico) |
| `efeitos.js` | `chuva`, `poeira`, `respingos`, `confete`, `brilhos` (cada um devolve `{ obj, atualizar(t, k) }`) |
| `pessoas.js` | `colega` (figurante low-poly com camisa, colete e capacete opcionais; `userData.atualizar(t, aceno)`) |
| `personagens/pintor-rig.js` | esqueleto em código do pintor (`criarPintor`, `POSES`, `misturar`) |
| `personagens/ecasio-rig.js` | esqueleto em código do Ecasio, mascote da ECASI (`criarEcasio`, mesmas `POSES` do pintor + `prancheta`) |

Os modelos dos personagens ficam em `personagens/<slug>/final/<slug>.glb` (na raiz do repositório).

## Regras de todos os componentes

- Recebem `THREE` como primeiro parâmetro e **não** importam `"three"`. Assim funcionam em qualquer projeto, sem importmap.
- Devolvem um `THREE.Group` (ou `Mesh`) com a base em `y = 0`. A escala segue a do personagem: altura do pintor = 1.
- Todo movimento depende **só do tempo `t`**: nada de `Math.random()` nem relógio em tempo de execução. Para variedade, use `rnd(semente)`.
- As ferramentas de mão têm o punho na origem e a ponta para `-Y`, prontas para `pintor.osso("maoD").add(...)`.

## Usar num vídeo (HyperFrames)

O HyperFrames só serve arquivos de dentro da pasta do projeto, então cada vídeo leva uma cópia:

```bash
python componentes-3d/instalar.py house/videos/fachada-do-zero pintor
```

Isso copia os módulos para `<projeto>/assets/c3d/` e o personagem para `assets/c3d/personagens/pintor.glb`. Rode de novo sempre que a biblioteca mudar. Na composição:

```js
import * as CEN from "./assets/c3d/cenario.js";
import * as PIN from "./assets/c3d/props-pintura.js";
import { criarPintor, POSES } from "./assets/c3d/personagens/pintor-rig.js";
const arvore = CEN.arvore(THREE, { seed: 3, altura: 2.4 });
```

## Catálogo

`catalogo/` é uma página HyperFrames que mostra todos os componentes com o nome. Para ver depois de mudar algo:

```bash
python componentes-3d/instalar.py componentes-3d/catalogo pintor
cd componentes-3d/catalogo && npx --yes hyperframes@0.8.217 snapshot --at 1.5,2.5,3.5,4.5 --no-end -o shots
```
