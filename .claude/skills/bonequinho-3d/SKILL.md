---
name: "bonequinho-3d"
description: "Cria bonequinhos 3D originais e sem marca, da imagem ao .glb animado (ChatGPT/Gemini via Chrome, conversor 3D, Mixamo, Blender, Three.js). Use para criar, animar ou reutilizar personagem 3D."
---

# Bonequinho 3D: da imagem ao personagem animado

Objetivo: criar personagens 3D originais, sem marca e reutilizáveis em qualquer vídeo, com aparência sempre idêntica e uma biblioteca padrão de animações.

**Princípio central:** o personagem é gerado UMA vez e vira arquivo. Um vídeo nunca regenera o personagem, só carrega `personagens/<slug>/final/<slug>.glb`. É isso que garante que ele seja sempre o mesmo.

## Regras

- Personagens sempre originais. Nunca recriar personagem, mascote ou figura conhecida, nem uma pessoa real identificável.
- O modelo base não tem marca nenhuma. Logos de cliente entram depois, como peça opcional por vídeo (seção 6).
- Nunca digitar senhas nem criar contas. Se um site pedir login, pare e peça para o usuário entrar.
- Antes de converter para 3D, mostre a imagem de conceito ao usuário e espere a aprovação. Ela é o rosto de todos os vídeos.
- Registre a ferramenta usada e a licença comercial dela em `character.json`.

## Estrutura de pastas

```
personagens/<slug>/
  ref/              imagens de referência recebidas
  conceito/         frente.png, turnaround.png (aprovadas)
  modelo/           bruto.glb (saída do conversor), base.fbx (para o Mixamo)
  rig/              00_idle.fbx (com malha) + animações .fbx (sem malha)
  final/<slug>.glb  modelo + todas as animações
  final/preview/    turntable e teste de animações
  character.json
```

```json
{
  "slug": "pintor",
  "descricao": "pintor latino, cabelo preto curto com laterais raspadas, macacão azul",
  "estilo": "3D vinil / toy art, sem contorno",
  "paleta": {"principal": "#2F6AE0", "secundaria": "#123986", "clara": "#609EF5"},
  "origem_imagem": "ChatGPT",
  "origem_3d": "Hunyuan3D-2 (Space Hugging Face)",
  "licenca": "conferir e anotar aqui",
  "altura_cena": 1.0,
  "animacoes": ["idle", "andar", "apontar", "acenar", "explicar", "pensar", "joinha", "comemorar", "olhar_em_volta", "pegar", "sentado"],
  "ossos": {"mao_direita": "mixamorigRightHand", "mao_esquerda": "mixamorigLeftHand", "costas": "mixamorigSpine2", "cabeca": "mixamorigHead"},
  "pecas_opcionais": []
}
```

## Etapa 0: verificar o ambiente e escolher a rota

Rode `blender --version`, `ffmpeg -version`, `node -v` e `python3 --version`.

- Sem o Blender: peça para instalar a versão estável em blender.org (grátis, 4.2 ou mais nova). Ele é obrigatório para as etapas 2 a 4.
- Veja se as ferramentas do Claude in Chrome (`mcp__claude-in-chrome__*`) estão disponíveis. Se estiverem, carregue a skill do navegador antes do primeiro uso.

Rotas:
- **A, navegador (preferida):** o Claude usa o Chrome para gerar a imagem (ChatGPT ou Gemini), converter para 3D e fazer o rig no Mixamo. O Blender local faz as conversões e a montagem.
- **B, assistida:** sem o Chrome, o Claude passa ao usuário o passo a passo exato das etapas web e processa os arquivos baixados.
- **C, 3D local (opcional):** rodar o Hunyuan3D-2 na máquina. Exige placa NVIDIA com bastante VRAM. O rig continua no Mixamo.

No Chrome, os downloads caem na pasta Downloads do usuário. Mova-os para a pasta do personagem logo em seguida.

## Etapa 1: imagem de conceito

Se o usuário mandou uma imagem, confira os requisitos abaixo. Se ela não servir (personagem de lado, cortado, segurando objeto, com contorno 2D), gere uma nova usando a imagem dele como referência.

**Requisitos da imagem:** corpo inteiro; vista frontal sem perspectiva; pose em A (braços a ~45°, sem encostar no tronco); mãos vazias e abertas; pernas levemente afastadas; fundo branco liso; sem sombra no chão; sem contorno preto; sem texto ou logo; nada pendurado ou solto (capa, cachecol, alça, cabelo longo solto). Acessórios colados ao corpo (óculos, boné) são aceitos.

**Prompt 1, frente** (troque os colchetes):

```
Use as imagens anexadas apenas como referência de estilo, rosto e cabelo.

Crie um personagem mascote ORIGINAL: [idade aproximada, profissão/papel, tom de pele, cabelo, traços marcantes, expressão].

Estilo: personagem 3D estilizado de animação, aparência de boneco de vinil / toy art, superfícies lisas e arredondadas, materiais foscos, cores sólidas. SEM contorno preto, SEM traço de desenho 2D, SEM textura de pincel.

Proporções: cabeça grande (cerca de 1/4 da altura total), corpo compacto, braços e pernas longos o suficiente para as mãos alcançarem a cabeça. Mãos com 5 dedos, levemente separados.

Roupa: [roupa] nas cores [paleta com hex]. Roupa ajustada ao corpo, sem peças soltas ou penduradas. Sem logos, marcas ou textos.

POSE (a imagem será convertida em modelo 3D e animada):
- Corpo inteiro, da cabeça aos pés, nada cortado
- Vista exatamente frontal, câmera na altura do peito, sem perspectiva
- Pose em A: em pé, ereto, braços abertos para baixo a uns 45° do corpo, sem encostar no tronco
- Pernas levemente afastadas, pés apontando para frente
- Mãos vazias e abertas, sem segurar nenhum objeto

Fundo branco liso e uniforme, sem cenário, sem sombra no chão, iluminação suave de estúdio. Formato vertical, personagem centralizado ocupando a maior parte da imagem.
```

**Prompt 2, turnaround** (na mesma conversa):

```
Perfeito. Agora gere o MESMO personagem, idêntico em rosto, cabelo, proporções, cores e roupa, na mesma pose em A e com o mesmo fundo branco liso, numa folha de personagem com 3 vistas lado a lado, na mesma escala e alinhadas pelos pés: 1. Frente  2. Lateral direita (perfil)  3. Costas. Sem sombras, sem cenário, sem texto.
```

**Pelo Chrome:** abra uma aba nova em chatgpt.com ou gemini.google.com (o usuário precisa estar logado). Anexe as referências com a ferramenta de upload, cole o Prompt 1, espere a geração (1 a 2 min) e baixe a imagem. Para corrigir um detalhe, peça só a correção ("mantenha tudo igual e mude apenas X"); um pedido do zero muda o rosto. Salve em `conceito/` e mostre ao usuário para aprovação.

## Etapa 2: imagem para 3D

| Ferramenta | Custo | Observações |
|---|---|---|
| Hunyuan3D-2 (Tencent): Space no Hugging Face ou local | grátis | open source; no Space pode haver fila e cota diária |
| TRELLIS (Microsoft): Space no Hugging Face | grátis | open source; bom para personagens estilizados |
| Tripo / Meshy | plano grátis com créditos | aceitam várias vistas (use o turnaround recortado); confira a licença comercial do plano |

Configurações: saída GLB com textura, entre ~20 mil e 50 mil triângulos, simetria ligada se houver. Use a imagem da frente, ou as 3 vistas recortadas se a ferramenta aceitar várias.

Salve como `modelo/bruto.glb` e inspecione com o Blender em modo headless:

```python
# blender -b -P inspecionar.py -- personagens/<slug>/modelo/bruto.glb
import bpy, sys
arq = sys.argv[sys.argv.index("--") + 1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=arq)
malhas = [o for o in bpy.data.objects if o.type == "MESH"]
tris = sum(len(p.vertices) - 2 for o in malhas for p in o.data.polygons)
print("malhas:", len(malhas), "triangulos:", tris)
print("materiais:", [m.name for m in bpy.data.materials], "imagens:", [i.name for i in bpy.data.images])
for o in malhas: print(o.name, "dimensoes:", tuple(round(d, 3) for d in o.dimensions))
```

Ajustes antes do Mixamo, todos feitos em script no Blender:
- Juntar todas as malhas em uma (`bpy.ops.object.join()`).
- Se passar de ~80 mil triângulos, aplicar o modificador Decimate até ficar perto de 40 mil.
- Origem nos pés (base em Z = 0), personagem centralizado e de frente para a vista Front do Blender (olhando para -Y).
- Exportar `modelo/base.fbx` com `bpy.ops.export_scene.fbx(filepath=..., path_mode='COPY', embed_textures=True)`.
- Renderizar uma prévia de 4 vistas (frente, lado, costas, 3/4) e mostrar ao usuário.

## Etapa 3: esqueleto e animações (Mixamo)

O Mixamo (mixamo.com, da Adobe) é gratuito e exige login. Ele aceita FBX, OBJ ou ZIP; GLB não.

1. Upload Character → `modelo/base.fbx`.
2. No auto-rigger, posicione os marcadores: queixo, pulsos, cotovelos, joelhos e virilha. Use o esqueleto padrão completo (com dedos).
3. Confira a prévia. Se os braços ou os ombros deformarem, refaça os marcadores. Se persistir, volte à etapa 1 e gere o conceito com os braços mais abertos.
4. Baixe as animações da biblioteca padrão:

| Nome no projeto | Buscar no Mixamo | Observação |
|---|---|---|
| idle | Breathing Idle | baixar primeiro, **With Skin** → `rig/00_idle.fbx` |
| andar | Walking | marcar **In Place** |
| apontar | Pointing | |
| acenar | Waving | |
| explicar | Talking | |
| pensar | Thinking | |
| joinha | Thumbs Up | |
| comemorar | Victory | |
| olhar_em_volta | Looking Around | |
| pegar | Picking Up | |
| sentado | Sitting Idle | |

Download: formato FBX Binary, 30 fps, sem redução de keyframes. Só o idle vai **With Skin**; os outros vão **Without Skin** e são salvos como `rig/<nome>.fbx`. Toda animação de deslocamento vai com **In Place**: quem move o personagem pelo cenário é o código.

Alternativa: o Tripo e o Meshy têm rig e animações embutidos. Podem ser usados, mas o padrão é o Mixamo, porque os nomes dos ossos ficam iguais em todos os personagens e o código de cena funciona com qualquer um.

## Etapa 4: montar o GLB final (Blender headless)

```python
# blender -b -P montar_glb.py -- personagens/<slug>
import bpy, sys, os, glob
pasta = os.path.normpath(sys.argv[sys.argv.index("--") + 1])
slug = os.path.basename(pasta)
bpy.ops.wm.read_factory_settings(use_empty=True)

def importar(fbx):
    antes = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=fbx)
    return [o for o in bpy.data.objects if o not in antes]

base = os.path.join(pasta, "rig", "00_idle.fbx")
arm = next(o for o in importar(base) if o.type == "ARMATURE")
if arm.animation_data and arm.animation_data.action:
    arm.animation_data.action.name = "idle"
    arm.animation_data.action.use_fake_user = True

for fbx in sorted(glob.glob(os.path.join(pasta, "rig", "*.fbx"))):
    if os.path.basename(fbx).startswith("00_"):
        continue
    novos = importar(fbx)
    a = next(o for o in novos if o.type == "ARMATURE")
    acao = a.animation_data.action
    acao.name = os.path.splitext(os.path.basename(fbx))[0]
    acao.use_fake_user = True
    for o in novos:
        bpy.data.objects.remove(o, do_unlink=True)

arm.animation_data.action = bpy.data.actions["idle"]
saida = os.path.join(pasta, "final", slug + ".glb")
os.makedirs(os.path.dirname(saida), exist_ok=True)
bpy.ops.export_scene.gltf(filepath=saida, export_format="GLB",
                          export_animations=True, export_animation_mode="ACTIONS")
print("OK", saida, sorted(a.name for a in bpy.data.actions))
```

Valide com `npx @gltf-transform/cli inspect personagens/<slug>/final/<slug>.glb`: todas as animações da tabela precisam aparecer com o nome certo.

Problemas conhecidos:
- Animações faltando ou vazias: troque `export_animation_mode` para `"NLA_TRACKS"`, colocando cada ação numa trilha NLA, e confira a versão do Blender.
- Textura perdida no Mixamo: copie os materiais de `modelo/bruto.glb` para a malha final no Blender antes de exportar.
- Personagem minúsculo ou gigante: o Mixamo trabalha em centímetros. Normalize a altura na cena (seção 5), não no arquivo.

## Etapa 5: usar nas cenas (Three.js / HyperFrames)

```js
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const gltf = await new GLTFLoader().loadAsync('personagens/pintor/final/pintor.glb');
const boneco = gltf.scene;
boneco.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } });

// normaliza a altura para o valor de character.json
const caixa = new THREE.Box3().setFromObject(boneco);
boneco.scale.multiplyScalar(1.0 / (caixa.max.y - caixa.min.y));

const mixer = new THREE.AnimationMixer(boneco);
const acoes = Object.fromEntries(gltf.animations.map(c => [c.name, mixer.clipAction(c)]));
Object.values(acoes).forEach(a => a.play());

// Render determinístico: a pose depende só do tempo t, nunca do relógio real.
// Funciona com renderizador que pula para qualquer frame.
// timeline: [{ ini: 0, clip: 'idle' }, { ini: 3.2, clip: 'apontar', loop: false }, ...]
const FADE = 0.4;
function tempoNoClipe(seg, t) {
  const d = acoes[seg.clip].getClip().duration, dt = t - seg.ini;
  return seg.loop === false ? Math.min(dt, d - 1e-3) : dt % d;
}
function poseNoTempo(t, timeline) {
  Object.values(acoes).forEach(a => a.setEffectiveWeight(0));
  const i = timeline.findLastIndex(s => s.ini <= t);
  const seg = timeline[i], ant = timeline[i - 1];
  const k = ant ? Math.min(1, (t - seg.ini) / FADE) : 1;
  if (ant && k < 1 && ant.clip !== seg.clip) {
    acoes[ant.clip].time = tempoNoClipe(ant, t);
    acoes[ant.clip].setEffectiveWeight(1 - k);
  }
  acoes[seg.clip].time = tempoNoClipe(seg, t);
  acoes[seg.clip].setEffectiveWeight(ant && ant.clip !== seg.clip ? k : 1);
  mixer.update(0);
}
```

**Objetos na mão:** pincel, rolo, ferramenta etc. são modelos separados, presos ao osso: `boneco.getObjectByName('mixamorigRightHand').add(rolo)`. O Three.js remove o ":" dos nomes do Mixamo, então `mixamorig:RightHand` vira `mixamorigRightHand`. Ajuste a posição e a rotação do objeto uma vez e salve em `character.json`.

**Receita de luz (visual de animação 3D):**
- `renderer.toneMapping = THREE.ACESFilmicToneMapping`, `outputColorSpace = THREE.SRGBColorSpace`, `shadowMap.type = THREE.PCFSoftShadowMap`.
- Ambiente: `RoomEnvironment` passado pelo `PMREMGenerator` em `scene.environment`. É grátis e não exige baixar HDRI.
- Sol: `DirectionalLight` quente com sombra (mapSize 2048) + `HemisphereLight` fraca (céu azul, chão esverdeado).
- Pós-processamento: `GTAOPass` (sombra de contato) sempre; `BokehPass` (fundo desfocado) nos closes.
- Materiais foscos (roughness entre 0.7 e 0.9). Câmera vertical 1080×1920, fov entre 30 e 40.
- Cenário: kits low-poly CC0 (Kenney, Quaternius, Poly Pizza). Registre a origem de cada kit.

No Blender, o caminho é o mesmo: Eevee, mesmos princípios de luz, renderizar sequência de imagens e juntar com o ffmpeg.

## Etapa 6: peças opcionais e marcas de cliente

O modelo base fica sempre sem marca. Para um cliente específico:
- **Logo nas costas:** um plano fino com o PNG do logo, preso ao osso `mixamorigSpine2`, levemente afastado das costas. Ele acompanha o tronco e fica nítido, ao contrário do logo borrado que o conversor 3D gera. Para mais qualidade, projete o logo na textura no Blender (Texture Paint com estêncil) e salve como uma variante: `final/<slug>__<cliente>.glb`.
- **Boné, crachá, uniforme:** o mesmo esquema, como peças presas a ossos, registradas em `pecas_opcionais`.

## Etapa 7: controle de qualidade (antes de dar como pronto)

Gere e mostre ao usuário:
1. Um turntable de 360° do personagem em idle.
2. Uma grade de vídeo com todas as animações rodando lado a lado.

Confira:
- [ ] O rosto se reconhece em tamanho de celular
- [ ] Os pés não deslizam (In Place) e as mãos não atravessam o corpo
- [ ] Ombros e cotovelos deformam sem quebrar
- [ ] Todas as animações estão no GLB com os nomes da tabela
- [ ] As texturas estão corretas, sem marca no modelo base
- [ ] O `character.json` está preenchido (origem, licença, ossos, peças)

## Limites (avise o usuário quando pesar)

- O Mixamo anima o corpo, não o rosto. Piscar, sorrir e falar exigem olhos e boca como peças separadas ou troca de textura. Para narração em off, isso não é necessário.
- O conversor por IA funde cabelo, óculos e roupa numa malha só: essas peças não se separam depois.
- A proporção muito cartoon (cabeça enorme, braço curto) pode fazer o auto-rig errar. Teste antes de produzir em série.