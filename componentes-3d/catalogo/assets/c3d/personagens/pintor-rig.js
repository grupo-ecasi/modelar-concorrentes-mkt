// Esqueleto do pintor feito em código (o auto-rigger do Mixamo recusou o modelo).
// Uso:  import { criarPintor } from "./pintor-rig.js";
//       const p = criarPintor(THREE, gltf.scene);   // p.root vai para a cena (altura 1, pés em y=0, de frente para +Z)
//       p.pose({ ...POSES.idle(t), ...ajustes });    // tudo determinístico: a pose depende só de t
//       p.osso("maoD").add(rolo);                    // objetos presos na mão
// Lado: D = direita do personagem (fica em -X), E = esquerda (+X).

// Articulações medidas na malha (unidades: altura do boneco = 1).
const J = {
  quadril: [0, 0.30, 0], coluna: [0, 0.40, 0], peito: [0, 0.50, 0], pescoco: [0, 0.60, -0.01], cabeca: [0, 0.64, 0.0],
  ombroE: [0.105, 0.555, -0.005], cotoveloE: [0.17, 0.46, 0], pulsoE: [0.235, 0.365, 0.005], pontaE: [0.285, 0.29, 0.01],
  coxaE: [0.065, 0.29, 0], joelhoE: [0.075, 0.17, 0], tornozeloE: [0.085, 0.07, -0.01], dedoE: [0.09, 0.03, 0.10],
};
for (const k of Object.keys(J)) if (k.endsWith("E")) { const b = k.slice(0, -1) + "D"; J[b] = [-J[k][0], J[k][1], J[k][2]]; }

// hierarquia: [nome, pai, articulação, ponta (para o envelope de pele)]
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

// regiões permitidas para cada osso (evita o braço puxar o tronco, a perna esquerda puxar a direita etc.)
function permitido(nome, x, y) {
  const lado = nome.endsWith("E") ? 1 : nome.endsWith("D") ? -1 : 0;
  if (nome === "cabeca") return y > 0.60;
  if (nome === "pescoco") return y > 0.56 && y < 0.70;
  if (/^braco/.test(nome)) return x * lado > 0.105 && y < 0.60;
  if (/^(antebraco|mao)/.test(nome)) return x * lado > 0.12 && y < 0.56;
  if (/^(coxa|canela|pe)/.test(nome)) return x * lado > -0.01 && y < 0.36;
  if (nome === "quadril") return y < 0.42;
  return y > 0.22 && y < 0.66; // coluna, peito
}

export function criarPintor(THREE, cena) {
  let malha = null;
  cena.traverse((o) => { if (o.isMesh && !malha) malha = o; });
  // normaliza: altura 1, pés em 0, centralizado
  malha.updateWorldMatrix(true, false);
  const geo = malha.geometry.clone().applyMatrix4(malha.matrixWorld);
  geo.computeBoundingBox();
  const bb = geo.boundingBox, h = bb.max.y - bb.min.y;
  geo.translate(-(bb.max.x + bb.min.x) / 2, -bb.min.y, -(bb.max.z + bb.min.z) / 2);
  geo.scale(1 / h, 1 / h, 1 / h);
  geo.computeVertexNormals();

  // ossos
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
    root: raiz, malha: pele, ossos,
    osso: (nome) => ossos[nome],
    // pose: { osso: [rx, ry, rz] em radianos } + raiz: { y, ry, x, z } (deslocamento do corpo)
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

// ---------- poses (todas em função de t, em segundos) ----------
// Convenções no osso em repouso (pose em A): braço: rx<0 levanta para a frente; rz levanta para o lado
// (E: rz>0 abre para +X... ajustado no teste visual). Antebraço: rx<0 dobra o cotovelo para a frente.
const S = Math.sin, PI = Math.PI;
export const POSES = {
  idle: (t) => ({
    peito: [0.02 * S(t * 2.1), 0, 0], cabeca: [0.03 * S(t * 1.3), 0.06 * S(t * 0.7), 0],
    bracoE: [0, 0, -0.03 * S(t * 2.1)], bracoD: [0, 0, 0.03 * S(t * 2.1)],
    raiz: { y: 0.003 * S(t * 2.1) },
  }),
  andar: (t) => {
    const f = t * 7.5, a = S(f);
    return {
      coxaE: [-0.45 * a, 0, 0], coxaD: [0.45 * a, 0, 0],
      canelaE: [Math.max(0, 0.6 * S(f + 1.2)), 0, 0], canelaD: [Math.max(0, -0.6 * S(f + 1.2)), 0, 0],
      bracoE: [0.35 * a, 0, 0.25], bracoD: [-0.35 * a, 0, -0.25],
      antebracoE: [-0.3, 0, 0], antebracoD: [-0.3, 0, 0],
      raiz: { y: 0.012 * Math.abs(S(f)) },
    };
  },
  apontar: (t) => ({
    bracoD: [-1.35, 0, 0.5], antebracoD: [-0.1, 0, 0],
    cabeca: [0, -0.25, 0], peito: [0, -0.12, 0],
  }),
  acenar: (t) => ({
    bracoD: [-0.35, 0, -1.45], antebracoD: [0, 0, -0.9 + 0.35 * S(t * 9)],
    cabeca: [0, -0.1, 0.06],
  }),
  explicar: (t) => ({
    bracoE: [-0.45, 0, -0.45], antebracoE: [-1.0 - 0.25 * S(t * 3.1), 0, 0],
    bracoD: [-0.45, 0, 0.45], antebracoD: [-1.0 - 0.25 * S(t * 3.1 + 1.4), 0, 0],
    cabeca: [0.04 * S(t * 2.3), 0.12 * S(t * 1.1), 0],
  }),
  pensar: (t) => ({
    bracoD: [-0.5, 0, 0.75], antebracoD: [-2.3, 0, 0], maoD: [0.3, 0, 0],
    bracoE: [-0.3, 0, -0.55], antebracoE: [-1.3, 0, 0],
    cabeca: [0.12, 0.15, 0.08 + 0.03 * S(t * 1.5)],
  }),
  joinha: (t) => ({
    bracoD: [-0.8, 0, 0.6], antebracoD: [-1.3, 0, 0],
    cabeca: [-0.05, 0, 0.08],
  }),
  comemorar: (t) => {
    const p = Math.abs(S(t * 6));
    return { bracoE: [-0.25, 0, 1.55], bracoD: [-0.25, 0, -1.55], antebracoE: [0, 0, 0.7], antebracoD: [0, 0, -0.7],
      cabeca: [-0.15, 0, 0], raiz: { y: 0.05 * p } };
  },
  olhar_em_volta: (t) => ({ cabeca: [0, 0.6 * S(t * 1.4), 0], peito: [0, 0.2 * S(t * 1.4), 0] }),
  pegar: (t) => ({
    coluna: [0.35, 0, 0], peito: [0.25, 0, 0], cabeca: [-0.3, 0, 0],
    bracoD: [-0.7, 0, -0.2], antebracoD: [-0.3, 0, 0],
    coxaE: [-0.35, 0, 0], coxaD: [-0.35, 0, 0], canelaE: [0.7, 0, 0], canelaD: [0.7, 0, 0],
    raiz: { y: -0.04 },
  }),
  // gestos de pintor (rolo/broxa à frente, sobe e desce)
  pintar_rolo: (t) => {
    const c = S(t * 4);
    return {
      bracoD: [-1.45 - 0.5 * c, 0, 0.6], antebracoD: [-0.45 + 0.25 * c, 0, 0],
      bracoE: [-1.35 - 0.5 * c, 0, -0.6], antebracoE: [-0.6 + 0.25 * c, 0, 0],
      peito: [-0.05 * c, 0, 0], raiz: { y: 0.004 * c },
    };
  },
  pintar_broxa: (t) => {
    const c = S(t * 5);
    return { bracoD: [-1.35 - 0.3 * c, 0, 0.55 + 0.2 * S(t * 2.5)], antebracoD: [-0.6 + 0.2 * c, 0, 0], cabeca: [0.05, 0, 0] };
  },
  lixar: (t) => {
    const c = S(t * 7);
    return { bracoD: [-1.3, 0, 0.55 + 0.25 * c], antebracoD: [-0.5, 0, 0], peito: [0, 0.06 * c, 0] };
  },
};

// mistura duas poses (k=0 → a, k=1 → b)
export function misturar(a, b, k) {
  const out = {};
  const nomes = new Set([...Object.keys(a), ...Object.keys(b)]);
  for (const n of nomes) {
    if (n === "raiz") {
      const ra = a.raiz || {}, rb = b.raiz || {}; out.raiz = {};
      for (const c of new Set([...Object.keys(ra), ...Object.keys(rb)])) out.raiz[c] = (ra[c] || 0) * (1 - k) + (rb[c] || 0) * k;
      continue;
    }
    const va = a[n] || [0, 0, 0], vb = b[n] || [0, 0, 0];
    out[n] = [0, 1, 2].map((i) => (va[i] || 0) * (1 - k) + (vb[i] || 0) * k);
  }
  return out;
}
