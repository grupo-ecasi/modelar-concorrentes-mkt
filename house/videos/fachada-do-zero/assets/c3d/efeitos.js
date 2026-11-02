// Efeitos animados: chuva, poeira, respingos de tinta, confete, brilhos. Cada um devolve
// { obj, atualizar(t, k) } — k (0..1) é a intensidade; tudo determinístico em função de t.
import { rnd, PALETA } from "./nucleo.js";

export function chuva(THREE, { n = 700, area = [6, 4, 3.2], centro = [0, 0, 1.4], vel = 6, cor = "#d6e6f5" } = {}) {
  const r = rnd(5), base = new Float32Array(n * 3);
  for (let i = 0; i < n; i++) { base[i * 3] = (r() - 0.5) * area[0]; base[i * 3 + 1] = r() * area[1]; base[i * 3 + 2] = (r() - 0.5) * area[2]; }
  const geo = new THREE.BufferGeometry(), pos = new Float32Array(n * 6);
  geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  const obj = new THREE.LineSegments(geo, new THREE.LineBasicMaterial({ color: cor, transparent: true, opacity: 0.7 }));
  obj.position.set(...centro); obj.frustumCulled = false;
  function atualizar(t, k) {
    obj.visible = k > 0.02; if (!obj.visible) return;
    obj.material.opacity = 0.7 * k;
    for (let i = 0; i < n; i++) {
      const y = area[1] - ((base[i * 3 + 1] + t * vel) % area[1]);
      pos[i * 6] = base[i * 3]; pos[i * 6 + 1] = y; pos[i * 6 + 2] = base[i * 3 + 2];
      pos[i * 6 + 3] = base[i * 3] - 0.01; pos[i * 6 + 4] = y - 0.12; pos[i * 6 + 5] = base[i * 3 + 2];
    }
    geo.attributes.position.needsUpdate = true;
  }
  return { obj, atualizar };
}

// partículas que sobem e se espalham a partir de um ponto (pó de lixa, vapor)
export function poeira(THREE, { n = 140, cor = "#e9e1d0", tamanho = 0.025, subida = 0.6, espalha = 0.5 } = {}) {
  const geo = new THREE.BufferGeometry(), pos = new Float32Array(n * 3), r = rnd(9), sem = Array.from({ length: n }, () => [r(), r(), r()]);
  geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  const obj = new THREE.Points(geo, new THREE.PointsMaterial({ color: cor, size: tamanho, transparent: true, opacity: 0.8, depthWrite: false }));
  obj.frustumCulled = false;
  function atualizar(t, k) {
    obj.visible = k > 0.02; if (!obj.visible) return;
    obj.material.opacity = 0.8 * k;
    sem.forEach(([a, b, c], i) => { const f = (a + t * 0.35) % 1; pos[i * 3] = (b - 0.5) * espalha * (0.3 + f); pos[i * 3 + 1] = f * subida; pos[i * 3 + 2] = (c - 0.5) * espalha * 0.4 * (0.3 + f); });
    geo.attributes.position.needsUpdate = true;
  }
  return { obj, atualizar };
}

// respingos de tinta saindo de um ponto (gotas em arco, caem e somem); "cor" pode mudar a cada uso
export function respingos(THREE, { n = 40, tamanho = 0.022 } = {}) {
  const geo = new THREE.BufferGeometry(), pos = new Float32Array(n * 3), r = rnd(13), sem = Array.from({ length: n }, () => [r(), r(), r(), r()]);
  geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  const mat = new THREE.PointsMaterial({ color: "#ffffff", size: tamanho, transparent: true, opacity: 1, depthWrite: false });
  const obj = new THREE.Points(geo, mat); obj.frustumCulled = false;
  function atualizar(t, k, cor) {
    obj.visible = k > 0.02; if (!obj.visible) return;
    if (cor) mat.color.set(cor);
    sem.forEach(([a, b, c, d], i) => {
      const f = (a + t * 1.6) % 1, vx = (b - 0.5) * 0.6, vy = 0.5 + c * 0.6, vz = 0.15 + d * 0.3;
      pos[i * 3] = vx * f; pos[i * 3 + 1] = vy * f - 1.6 * f * f; pos[i * 3 + 2] = vz * f;
    });
    mat.opacity = k; geo.attributes.position.needsUpdate = true;
  }
  return { obj, atualizar };
}

// confete colorido caindo (comemoração)
export function confete(THREE, { n = 220, area = [3, 3, 2] } = {}) {
  const r = rnd(21), inst = new THREE.InstancedMesh(new THREE.PlaneGeometry(0.035, 0.02), new THREE.MeshBasicMaterial({ side: THREE.DoubleSide }), n);
  const sem = Array.from({ length: n }, () => [r(), r(), r(), r(), r()]), cor = new THREE.Color(), m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), e = new THREE.Euler(), v = new THREE.Vector3(), s = new THREE.Vector3(1, 1, 1);
  sem.forEach((_, i) => inst.setColorAt(i, cor.set(PALETA.vivas[i % PALETA.vivas.length])));
  inst.frustumCulled = false;
  function atualizar(t, k) {
    inst.visible = k > 0.02; if (!inst.visible) return;
    sem.forEach(([a, b, c, d, f], i) => {
      const y = area[1] - ((a * area[1] + t * (0.5 + d * 0.4)) % area[1]);
      v.set((b - 0.5) * area[0] + Math.sin(t * 2 + f * 6) * 0.1, y, (c - 0.5) * area[2]);
      e.set(t * (2 + d * 3), t * (1 + f * 2), f * 6); q.setFromEuler(e); s.setScalar(k);
      inst.setMatrixAt(i, m4.compose(v, q, s));
    });
    inst.instanceMatrix.needsUpdate = true;
  }
  return { obj: inst, atualizar };
}

// brilhos (estrelinhas) que piscam em volta de um ponto — "ficou novo"
export function brilhos(THREE, { n = 14, raio = 1.2 } = {}) {
  const g = new THREE.Group(), r = rnd(31), est = [];
  const m = new THREE.MeshBasicMaterial({ color: "#fff6c8", transparent: true });
  const forma = new THREE.Shape(); for (let i = 0; i < 8; i++) { const a = (i / 8) * Math.PI * 2, rr = i % 2 ? 0.012 : 0.05; i ? forma.lineTo(Math.cos(a) * rr, Math.sin(a) * rr) : forma.moveTo(Math.cos(a) * rr, Math.sin(a) * rr); }
  const geo = new THREE.ShapeGeometry(forma);
  for (let i = 0; i < n; i++) { const s = new THREE.Mesh(geo, m); s.position.set((r() - 0.5) * raio * 2, r() * raio, (r() - 0.5) * 0.2); s.userData.f = r() * 6; g.add(s); est.push(s); }
  function atualizar(t, k) {
    g.visible = k > 0.02; if (!g.visible) return;
    est.forEach((s) => { const p = Math.max(0, Math.sin(t * 4 + s.userData.f)); s.scale.setScalar(p * k + 0.0001); s.rotation.z = t; });
  }
  return { obj: g, atualizar };
}
