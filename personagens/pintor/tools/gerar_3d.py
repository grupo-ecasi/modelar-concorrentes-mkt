# Gera o modelo 3D (GLB com textura) a partir da imagem de conceito, via Space do Hugging Face.
# Uso: python gerar_3d.py <imagem> <pasta_saida> [trellis|hunyuan] [vista2.png vista3.png ...]
# Com vistas extras (lado, costas), o TRELLIS roda no modo multi-imagem e salva bruto_multi.glb.
# Padrão: trellis (em 01/11/2026 o /generation_all do Hunyuan3D-2 respondia com NameError).
import sys, shutil, os, json, time
from gradio_client import Client, handle_file

img, saida = sys.argv[1], sys.argv[2]
motor = sys.argv[3] if len(sys.argv) > 3 else "trellis"
extras = sys.argv[4:]
SIMPLIFY = float(os.environ.get("SIMPLIFY", "0.95"))   # fração removida; 0.95 deu ~8,5 mil faces
TEXTURA = int(os.environ.get("TEXTURA", "1024"))
os.makedirs(saida, exist_ok=True)
t0 = time.time()

if motor == "trellis":
    c = Client("trellis-community/TRELLIS", verbose=False)
    c.predict(api_name="/start_session")
    pre = c.predict(image=handle_file(img), api_name="/preprocess_image")
    multi = []
    if extras:
        # /lambda_1 = selecionar a aba "Multiple Images"; sem isso o Space ignora as vistas extras
        c.predict(api_name="/lambda_1")
        gal = [{"image": handle_file(x), "caption": None} for x in [img] + extras]
        prep = c.predict(images=gal, api_name="/preprocess_images")
        multi = [{"image": handle_file(g["image"]), "caption": None} for g in prep]
    res = c.predict(
        image=handle_file(pre), multiimages=multi, seed=0,
        ss_guidance_strength=7.5, ss_sampling_steps=12,
        slat_guidance_strength=3.0, slat_sampling_steps=12,
        multiimage_algo="stochastic", mesh_simplify=SIMPLIFY, texture_size=TEXTURA,
        api_name="/generate_and_extract_glb",
    )
    video, glb = res[0], res[2] or res[1]
    print("saídas:", res)
    nome = "bruto_multi" if extras else "bruto"
    shutil.copy(glb, os.path.join(saida, nome + ".glb"))
    if isinstance(video, dict) and video.get("video"):
        shutil.copy(video["video"], os.path.join(saida, nome + "_preview.mp4"))
else:
    c = Client("tencent/Hunyuan3D-2", verbose=False)
    res = c.predict(
        caption=None, image=handle_file(img),
        mv_image_front=None, mv_image_back=None, mv_image_left=None, mv_image_right=None,
        steps=30, guidance_scale=5.0, seed=1234, octree_resolution=256,
        check_box_rembg=True, num_chunks=8000, randomize_seed=False,
        api_name="/generation_all",
    )
    shutil.copy(res[1], os.path.join(saida, "bruto" + os.path.splitext(res[1])[1]))
    print("stats:", json.dumps(res[3], ensure_ascii=False)[:400])

print("motor:", motor, "tempo: %.0fs" % (time.time() - t0))
