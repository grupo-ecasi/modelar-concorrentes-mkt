// Esqueleto do Ecasio (coruja mascote do Grupo ECASI) feito em código, no mesmo esquema do pintor.
// Uso:  import { criarEcasio, POSES, misturar } from "./ecasio-rig.js";
//       const e = criarEcasio(THREE, gltf.scene);   // e.root vai para a cena (altura 1, pés em y=0, de frente para +Z)
//       e.pose({ ...POSES.idle(t), ...ajustes });    // determinístico: a pose depende só de t
//       e.osso("maoD").add(prancheta);              // objetos presos na ponta da asa
// Os nomes dos ossos e as POSES são os mesmos do pintor (pintor-rig.js), então os movimentos são reaproveitados.
// Lado: D = direita do personagem (fica em -X), E = esquerda (+X).
import { POSES as POSES_PINTOR, misturar } from "./pintor-rig.js";

// Articulações medidas na malha (personagens/ecasio/modelo/bruto_multi.glb, fatias horizontais; altura = 1).
// A cabeça com capacete vai de 0,58 a 1; as asas saem do tronco em y≈0,50 e terminam em y≈0,28, x≈0,37.
const J = {
  quadril: [0, 0.27, 0], coluna: [0, 0.36, 0], peito: [0, 0.46, 0], pescoco: [0, 0.555, 0], cabeca: [0, 0.60, 0.0],
  ombroE: [0.15, 0.495, 0], cotoveloE: [0.215, 0.425, 0.005], pulsoE: [0.285, 0.35, 0.01], pontaE: [0.355, 0.285, 0.015],
  coxaE: [0.085, 0.25, 0], joelhoE: [0.10, 0.16, 0], tornozeloE: [0.11, 0.085, -0.01], dedoE: [0.12, 0.03, 0.12],
};
for (const k of Object.keys(J)) if (k.endsWith("E")) { const b = k.slice(0, -1) + "D"; J[b] = [-J[k][0], J[k][1], J[k][2]]; }

const OSSOS = [
  ["quadril", null, "quadril", "coluna"],
  ["coluna", "quadril", "coluna", "peito"],
  ["peito", "coluna", "peito", "pescoco"],
  ["pescoco", "peito", "pescoco", "cabeca"],
  ["cabeca", "pescoco", "cabeca", null],
];
for (const L of ["E", "D"]) {
  OSSOS.push(
    ["braco" + L, "peito", "ombro" + L, "cotovelo" + L],
    ["antebraco" + L, "braco" + L, "cotovelo" + L, "pulso" + L],
    ["mao" + L, "antebraco" + L, "pulso" + L, "ponta" + L],
    ["coxa" + L, "quadril", "coxa" + L, "joelho" + L],
    ["canela" + L, "coxa" + L, "joelho" + L, "tornozelo" + L],
    ["pe" + L, "canela" + L, "tornozelo" + L, "dedo" + L],
  );
}

function distSeg(px, py, pz, a, b) {
  if (!b) return Math.hypot(px - a[0], py - a[1], pz - a[2]);
  const vx = b[0] - a[0], vy = b[1] - a[1], vz = b[2] - a[2];
  const t = Math.max(0, Math.min(1, ((px - a[0]) * vx + (py - a[1]) * vy + (pz - a[2]) * vz) / (vx * vx + vy * vy + vz * vz)));
  return Math.hypot(px - a[0] - vx * t, py - a[1] - vy * t, pz - a[2] - vz * t);
}

// Regiões permitidas para cada osso. Entre y 0,28 e 0,46 há um vão entre a asa (|x| > 0,15) e o tronco.
function permitido(nome, x, y) {
  const lado = nome.endsWith("E") ? 1 : nome.endsWith("D") ? -1 : 0;
  const ax = Math.abs(x);
  if (nome === "cabeca") return y > 0.575;
  if (nome === "pescoco") return y > 0.52 && y < 0.66;
  if (/^braco/.test(nome)) return x * lado > (y < 0.43 ? 0.178 : 0.145) && y < 0.56 && y > 0.24;
  if (/^(antebraco|mao)/.test(nome)) return x * lado > 0.185 && y < 0.47;
  if (/^(coxa|canela|pe)/.test(nome)) return x * lado > -0.01 && x * lado < 0.21 && y < 0.30;
  if (nome === "quadril") return y < 0.40 && ax < 0.175;
  // coluna e peito: tronco estreito embaixo, ombros largos em cima
  return y > 0.22 && y < 0.62 && (ax < 0.165 || y > 0.47);
}

export function criarEcasio(THREE, cena) {
  let malha = null;
  cena.traverse((o) => { if (o.isMesh && !malha) malha = o; });
  malha.updateWorldMatrix(true, false);
  const geo = malha.geometry.clone().applyMatrix4(malha.matrixWorld);
  geo.computeBoundingBox();
  const bb = geo.boundingBox, h = bb.max.y - bb.min.y;
  geo.translate(-(bb.max.x + bb.min.x) / 2, -bb.min.y, -(bb.max.z + bb.min.z) / 2);
  geo.scale(1 / h, 1 / h, 1 / h);
  geo.computeVertexNormals();

  const ossos = {}, lista = [];
  for (const [nome, pai, art] of OSSOS) {
    const b = new THREE.Bone(); b.name = nome;
    const p = J[art], pp = pai ? J[OSSOS.find((o) => o[0] === pai)[2]] : [0, 0, 0];
    b.position.set(p[0] - pp[0], p[1] - pp[1], p[2] - pp[2]);
    if (pai) ossos[pai].add(b);
    ossos[nome] = b; lista.push(b);
  }

  // pesos de pele por envelope: 1/d^4 entre os ossos permitidos, 4 maiores
  const pos = geo.attributes.position, n = pos.count;
  const idx = new Uint16Array(n * 4), pes = new Float32Array(n * 4);
  const segs = OSSOS.map(([nome, , a, b]) => [nome, J[a], b ? J[b] : null]);
  const cand = new Float32Array(segs.length);
  for (let i = 0; i < n; i++) {
    const x = pos.getX(i), y = pos.getY(i), z = pos.getZ(i);
    for (let s = 0; s < segs.length; s++) {
      const [nome, a, b] = segs[s];
      cand[s] = permitido(nome, x, y) ? 1 / Math.pow(distSeg(x, y, z, a, b) + 0.012, 4) : 0;
    }
    const ord = [...cand.keys()].sort((p, q) => cand[q] - cand[p]).slice(0, 4);
    let soma = 0; for (const s of ord) soma += cand[s];
    if (soma === 0) { idx[i * 4] = 1; pes[i * 4] = 1; continue; }
    ord.forEach((s, k) => { idx[i * 4 + k] = s; pes[i * 4 + k] = cand[s] / soma; });
  }
  geo.setAttribute("skinIndex", new THREE.Uint16BufferAttribute(idx, 4));
  geo.setAttribute("skinWeight", new THREE.Float32BufferAttribute(pes, 4));

  const mat = malha.material;
  mat.roughness = 0.8; mat.metalness = 0;
  const pele = new THREE.SkinnedMesh(geo, mat);
  pele.castShadow = true; pele.receiveShadow = true;
  const raiz = new THREE.Group();
  raiz.add(ossos.quadril); raiz.add(pele);
  raiz.updateMatrixWorld(true);
  pele.bind(new THREE.Skeleton(lista));

  const base = {}; for (const b of lista) base[b.name] = b.position.clone();
  return {
    root: raiz, malha: pele, ossos, J,
    osso: (nome) => ossos[nome],
    pose(p) {
      for (const b of lista) { b.rotation.set(0, 0, 0); b.position.copy(base[b.name]); }
      for (const [nome, r] of Object.entries(p)) {
        if (nome === "raiz") continue;
        if (ossos[nome]) ossos[nome].rotation.set(r[0] || 0, r[1] || 0, r[2] || 0);
      }
      const r = p.raiz || {};
      ossos.quadril.position.y = base.quadril.y + (r.y || 0);
      raiz.rotation.y = r.ry || 0;
      raiz.updateMatrixWorld(true);
    },
  };
}

// Mesmos movimentos do pintor (sem os de pintura). Ajustes só onde a coruja precisa.
const S = Math.sin;
export const POSES = {
  ...POSES_PINTOR,
  // perna curta: passo menor
  andar: (t) => {
    const f = t * 7.5, a = S(f);
    return {
      coxaE: [-0.35 * a, 0, 0], coxaD: [0.35 * a, 0, 0],
      canelaE: [Math.max(0, 0.45 * S(f + 1.2)), 0, 0], canelaD: [Math.max(0, -0.45 * S(f + 1.2)), 0, 0],
      bracoE: [0.3 * a, 0, 0.15], bracoD: [-0.3 * a, 0, -0.15],
      raiz: { y: 0.01 * Math.abs(S(f)) },
    };
  },
  // segurando a prancheta à frente do peito (asa direita)
  prancheta: (t) => ({
    bracoD: [-0.8, 0, 0.9], antebracoD: [0, 0, 1.2],
    cabeca: [0.04 * S(t * 1.6), 0.08 * S(t * 0.9), 0],
    peito: [0.015 * S(t * 2.1), 0, 0],
  }),
};
delete POSES.pintar_rolo; delete POSES.pintar_broxa; delete POSES.lixar;
export { misturar };

// Adesivo com o logo do Grupo ECASI na frente do capacete (como no mascote oficial).
// É uma faixa curva presa ao osso da cabeça: acompanha todos os movimentos e fica nítida
// (o conversor 3D borraria um logo pintado na textura).
// Uso: const img = await carregarImagem("assets/brand/logo-fundo-claro.png");
//      logoCapacete(THREE, ecasio, img);
// Medidas tiradas da malha (altura = 1): frente do casco em y 0,86–0,94, com z de 0,172 a 0,142.
export function logoCapacete(THREE, e, imagem, { largura = 0.17, altura = 0.062, y = 0.9, z = 0.163, inclinacao = -0.36, raio = 0.168 } = {}) {
  const cv = document.createElement("canvas"); cv.width = 768; cv.height = 280;
  const g = cv.getContext("2d");
  const r = 70, W = cv.width, H = cv.height;
  g.fillStyle = "#ffffff";
  g.beginPath(); g.moveTo(r, 0); g.arcTo(W, 0, W, H, r); g.arcTo(W, H, 0, H, r); g.arcTo(0, H, 0, 0, r); g.arcTo(0, 0, W, 0, r); g.closePath(); g.fill();
  const esc = Math.min((W * 0.86) / imagem.width, (H * 0.8) / imagem.height);
  const lw = imagem.width * esc, lh = imagem.height * esc;
  g.drawImage(imagem, (W - lw) / 2, (H - lh) / 2, lw, lh);
  const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
  const ang = largura / raio;
  const geo = new THREE.CylinderGeometry(raio, raio, altura, 32, 1, true, -ang / 2, ang);
  const m = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ map: tex, transparent: true, roughness: 0.45, polygonOffset: true, polygonOffsetFactor: -2 }));
  m.position.z = -raio + 0.005; // a superfície da faixa fica 5 mm à frente do casco
  const piv = new THREE.Group();
  piv.add(m);
  const cab = e.J.cabeca;
  piv.position.set(0 - cab[0], y - cab[1], z - cab[2]);
  piv.rotation.x = inclinacao;
  e.osso("cabeca").add(piv);
  return piv;
}

export function carregarImagem(url) {
  return new Promise((ok, erro) => { const i = new Image(); i.onload = () => ok(i); i.onerror = erro; i.src = url; });
}
