# Personagens 3D

Biblioteca de bonequinhos 3D originais e sem marca, criados com a skill `bonequinho-3d`.
Um personagem é gerado uma vez; os vídeos só carregam `personagens/<slug>/final/<slug>.glb`.

## Pastas de cada personagem

```
<slug>/
  ref/        imagens de referência
  conceito/   frente.png e turnaround.png aprovados
  modelo/     bruto.glb (conversor 3D) e base.zip (OBJ para o Mixamo)
  rig/        00_idle.fbx (com malha) e as animações .fbx (sem malha)
  final/      <slug>.glb (modelo e animações) e preview/
  character.json
```

## Ferramentas desta máquina (sem Blender)

A máquina tem 4 GB de RAM, então o Blender com tela foi trocado por ferramentas leves de terminal:

| Tarefa | Ferramenta |
|---|---|
| Imagem → 3D (Space `tencent/Hunyuan3D-2` ou `trellis-community/TRELLIS`) | `gradio_client` 2.7.2 (Python, sem `-I`: fica no site-packages do usuário) |
| Inspecionar, reduzir e centralizar o modelo | `gltf-transform` 4.5.1 (npm global) |
| GLB → OBJ em ZIP para o upload no Mixamo | `trimesh` 5.2.0 (Python) |
| FBX do Mixamo → GLB | `FBX2glTF` 0.9.7 (npm global `fbx2gltf`) |
| Prévias (giro de 360° e grade de animações) | Three.js renderizado pelo HyperFrames |

Contas (o usuário entra; o Claude não digita senhas): Adobe ID grátis no Mixamo e ChatGPT para a imagem de conceito.
