// Props de pintura (House): latas, balde, broxa, rolo, bandeja, lixa, espátula, bisnaga, escada, lona, fita.
// Ferramentas de mão saem com o "punho" na origem e a ponta para -Y (para prender no osso da mão).
import { mat, sombras, texturaCanvas, PALETA } from "./nucleo.js";

// lata de tinta com rótulo colorido (rótulo desenhado: faixa + gota + texto curto opcional)
export function lata(THREE, { cor = PALETA.house.creme, rotulo = PALETA.house.azul, texto = "", altura = 0.16, raio = 0.075, aberta = false } = {}) {
  const g = new THREE.Group();
  const metal = mat(THREE, "#d8dde4", 0.35);
  const corpo = new THREE.Mesh(new THREE.CylinderGeometry(raio, raio, altura, 28), metal); corpo.position.y = altura / 2; g.add(corpo);
  const tex = texturaCanvas(THREE, 256, 128, (c, w, h) => {
    c.fillStyle = rotulo; c.fillRect(0, 0, w, h);
    c.fillStyle = cor; c.beginPath(); c.arc(w * 0.18, h * 0.5, h * 0.28, 0, 7); c.fill();
    c.fillStyle = "rgba(255,255,255,.9)"; c.fillRect(w * 0.36, h * 0.3, w * 0.5, h * 0.12); c.fillRect(w * 0.36, h * 0.55, w * 0.34, h * 0.1);
    if (texto) { c.fillStyle = "#fff"; c.font = "bold 40px sans-serif"; c.fillText(texto, w * 0.36, h * 0.92); }
  });
  const rot = new THREE.Mesh(new THREE.CylinderGeometry(raio * 1.005, raio * 1.005, altura * 0.62, 28, 1, true), new THREE.MeshStandardMaterial({ map: tex, roughness: 0.6 }));
  rot.position.y = altura * 0.5; g.add(rot);
  const aro = new THREE.Mesh(new THREE.TorusGeometry(raio * 0.97, 0.006, 6, 28), metal); aro.rotation.x = Math.PI / 2; aro.position.y = altura; g.add(aro);
  const topo = new THREE.Mesh(new THREE.CylinderGeometry(raio * 0.95, raio * 0.95, 0.008, 28), aberta ? mat(THREE, cor, 0.5) : metal); topo.position.y = altura - (aberta ? 0.01 : -0.002); g.add(topo);
  const alca = new THREE.Mesh(new THREE.TorusGeometry(raio * 0.95, 0.004, 6, 24, Math.PI), metal); alca.position.y = altura; alca.rotation.y = Math.PI / 2; g.add(alca);
  return sombras(g);
}

export function balde(THREE, { cor = "#e9eef5", conteudo = "#ffffff" } = {}) {
  const g = new THREE.Group();
  const b = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.08, 0.18, 24, 1, true), new THREE.MeshStandardMaterial({ color: cor, roughness: 0.6, side: THREE.DoubleSide }));
  b.position.y = 0.09; g.add(b);
  const fundo = new THREE.Mesh(new THREE.CircleGeometry(0.08, 24), mat(THREE, cor)); fundo.rotation.x = -Math.PI / 2; fundo.position.y = 0.002; g.add(fundo);
  const c = new THREE.Mesh(new THREE.CircleGeometry(0.095, 24), mat(THREE, conteudo, 0.95)); c.rotation.x = -Math.PI / 2; c.position.y = 0.15; g.add(c);
  const alca = new THREE.Mesh(new THREE.TorusGeometry(0.1, 0.004, 6, 24, Math.PI), mat(THREE, "#9aa3ad", 0.3)); alca.position.y = 0.18; g.add(alca);
  return sombras(g);
}

export function broxa(THREE, { cerda = "#f4f1e8" } = {}) {
  const g = new THREE.Group();
  const cabo = new THREE.Mesh(new THREE.CylinderGeometry(0.009, 0.009, 0.12, 8), mat(THREE, "#b07a45", 0.7)); cabo.position.y = -0.04; g.add(cabo);
  const vir = new THREE.Mesh(new THREE.BoxGeometry(0.075, 0.025, 0.032), mat(THREE, "#c9ced6", 0.3)); vir.position.y = -0.105; g.add(vir);
  const c = new THREE.Mesh(new THREE.BoxGeometry(0.072, 0.06, 0.028), mat(THREE, cerda)); c.position.y = -0.145; g.add(c);
  g.userData.ponta = c;
  return sombras(g);
}

export function rolo(THREE, { cabo = PALETA.house.azul, la = "#f6efe0" } = {}) {
  const g = new THREE.Group();
  const c = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 0.01, 0.16, 8), mat(THREE, cabo, 0.5)); c.position.y = -0.05; g.add(c);
  const h = new THREE.Mesh(new THREE.CylinderGeometry(0.004, 0.004, 0.09, 6), mat(THREE, "#9aa3ad", 0.3)); h.position.set(0, -0.15, 0.03); h.rotation.x = 0.6; g.add(h);
  const cil = new THREE.Mesh(new THREE.CylinderGeometry(0.028, 0.028, 0.12, 16), mat(THREE, la)); cil.rotation.z = Math.PI / 2; cil.position.set(0, -0.19, 0.06); g.add(cil);
  g.userData.la = cil;
  return sombras(g);
}

export function bandeja(THREE, { tinta = PALETA.house.creme } = {}) {
  const g = new THREE.Group();
  const b = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.03, 0.3), mat(THREE, "#2d3b55", 0.5)); b.position.y = 0.015; g.add(b);
  const t = new THREE.Mesh(new THREE.BoxGeometry(0.19, 0.005, 0.12), mat(THREE, tinta, 0.4)); t.position.set(0, 0.031, 0.07); g.add(t);
  return sombras(g);
}

export function lixa(THREE) {
  const g = new THREE.Group();
  const b = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.035, 0.045), mat(THREE, "#ffb84d")); b.position.y = -0.05; g.add(b);
  const l = new THREE.Mesh(new THREE.BoxGeometry(0.082, 0.004, 0.047), mat(THREE, "#c8a46a", 1)); l.position.y = -0.069; g.add(l);
  return sombras(g);
}

export function espatula(THREE) {
  const g = new THREE.Group();
  const cabo = new THREE.Mesh(new THREE.BoxGeometry(0.022, 0.08, 0.016), mat(THREE, PALETA.house.marinho)); cabo.position.y = -0.04; g.add(cabo);
  const lam = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.06, 0.003), mat(THREE, "#c9ced6", 0.25, { metalness: 0.4 })); lam.position.y = -0.11; g.add(lam);
  return sombras(g);
}

export function bisnaga(THREE, { cor = "#ffffff", rotulo = "#8a8f99" } = {}) {
  const g = new THREE.Group();
  const corpo = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.2, 16), mat(THREE, rotulo, 0.5)); corpo.position.y = 0.1; g.add(corpo);
  const bico = new THREE.Mesh(new THREE.ConeGeometry(0.012, 0.06, 10), mat(THREE, cor)); bico.position.y = 0.23; g.add(bico);
  return sombras(g);
}

// escada de abrir (altura em metros da cena)
export function escada(THREE, { altura = 1.0, cor = "#ffc928" } = {}) {
  const g = new THREE.Group(), m = mat(THREE, cor, 0.6), ang = 0.22;
  for (const lado of [1, -1]) {
    const f = new THREE.Group();
    for (const x of [-0.16, 0.16]) { const t = new THREE.Mesh(new THREE.BoxGeometry(0.03, altura, 0.03), m); t.position.set(x, altura / 2, 0); f.add(t); }
    if (lado === 1) for (let y = 0.2; y < altura; y += 0.22) { const d = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.02, 0.07), mat(THREE, "#9aa3ad", 0.4)); d.position.set(0, y, 0); f.add(d); }
    f.rotation.x = lado * ang; f.position.z = -lado * Math.sin(ang) * altura * 0.5 + lado * 0.0;
    g.add(f);
  }
  return sombras(g);
}

export function lona(THREE, { largura = 1.4, profundidade = 0.9, cor = "#cfe0f5" } = {}) {
  const geo = new THREE.PlaneGeometry(largura, profundidade, 12, 8);
  const p = geo.attributes.position;
  for (let i = 0; i < p.count; i++) p.setZ(i, Math.sin(p.getX(i) * 9) * 0.006 + Math.cos(p.getY(i) * 7) * 0.005);
  geo.computeVertexNormals();
  const tex = texturaCanvas(THREE, 256, 160, (c, w, h) => {
    c.fillStyle = cor; c.fillRect(0, 0, w, h);
    for (let i = 0; i < 40; i++) { c.fillStyle = PALETA.vivas[i % PALETA.vivas.length]; c.globalAlpha = 0.6; c.beginPath(); c.arc((i * 53) % w, (i * 37) % h, 2 + (i % 4), 0, 7); c.fill(); }
  });
  const m = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ map: tex, roughness: 0.95, side: THREE.DoubleSide }));
  m.rotation.x = -Math.PI / 2; m.position.y = 0.045; m.receiveShadow = true;
  return m;
}

export function fitaCrepe(THREE) {
  const m = new THREE.Mesh(new THREE.TorusGeometry(0.04, 0.018, 8, 20), mat(THREE, "#f2d28b", 0.8));
  m.rotation.x = Math.PI / 2; m.position.y = 0.018; return sombras(m);
}
