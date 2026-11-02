// Figurantes simples (low-poly, sem rosto detalhado) para cenas com equipe. Altura ~ 1 (mesma escala do pintor/Ecasio).
// Recebem THREE, devolvem Group com base em y=0 e userData.atualizar(t) para um balanço leve (só depende de t).
import { mat, sombras, PALETA } from "./nucleo.js";

export function colega(THREE, { camisa = "#1f6fd1", calca = "#2b3445", pele = "#c98b62", capacete = PALETA.ecasi.amarelo, colete = null, seed = 1, altura = 0.95 } = {}) {
  const g = new THREE.Group(), s = altura;
  const corpo = new THREE.Group(); g.add(corpo);
  const perna = new THREE.CapsuleGeometry(0.045 * s, 0.32 * s, 4, 10);
  for (const x of [-0.06, 0.06]) { const p = new THREE.Mesh(perna, mat(THREE, calca, 0.8)); p.position.set(x * s, 0.21 * s, 0); corpo.add(p); const b = new THREE.Mesh(new THREE.BoxGeometry(0.09 * s, 0.05 * s, 0.14 * s), mat(THREE, "#22262e", 0.7)); b.position.set(x * s, 0.025 * s, 0.02 * s); corpo.add(b); }
  const tronco = new THREE.Mesh(new THREE.CapsuleGeometry(0.12 * s, 0.22 * s, 6, 14), mat(THREE, camisa, 0.75)); tronco.position.y = 0.55 * s; tronco.scale.z = 0.75; corpo.add(tronco);
  if (colete) { const v = new THREE.Mesh(new THREE.CapsuleGeometry(0.125 * s, 0.16 * s, 6, 14), mat(THREE, colete, 0.6)); v.position.y = 0.55 * s; v.scale.z = 0.8; corpo.add(v); }
  const braco = new THREE.CapsuleGeometry(0.04 * s, 0.26 * s, 4, 10);
  const bracos = [-1, 1].map((l) => { const piv = new THREE.Group(); piv.position.set(l * 0.16 * s, 0.68 * s, 0); const m = new THREE.Mesh(braco, mat(THREE, camisa, 0.75)); m.position.y = -0.16 * s; piv.add(m); const mao = new THREE.Mesh(new THREE.SphereGeometry(0.04 * s, 10, 8), mat(THREE, pele, 0.7)); mao.position.y = -0.33 * s; piv.add(mao); piv.rotation.z = l * 0.12; corpo.add(piv); return piv; });
  const cabeca = new THREE.Mesh(new THREE.SphereGeometry(0.105 * s, 20, 14), mat(THREE, pele, 0.7)); cabeca.position.y = 0.86 * s; corpo.add(cabeca);
  for (const x of [-0.035, 0.035]) { const o = new THREE.Mesh(new THREE.SphereGeometry(0.012 * s, 8, 6), mat(THREE, "#1b1f27", 0.4)); o.position.set(x * s, 0.875 * s, 0.098 * s); corpo.add(o); }
  if (capacete) {
    const c = new THREE.Mesh(new THREE.SphereGeometry(0.115 * s, 20, 10, 0, Math.PI * 2, 0, Math.PI / 2), mat(THREE, capacete, 0.45)); c.position.y = 0.9 * s; corpo.add(c);
    const aba = new THREE.Mesh(new THREE.CylinderGeometry(0.135 * s, 0.135 * s, 0.01 * s, 24), mat(THREE, capacete, 0.45)); aba.position.set(0, 0.9 * s, 0.015 * s); corpo.add(aba);
  }
  const fase = seed * 1.7;
  g.userData.atualizar = (t, aceno = 0) => {
    corpo.position.y = 0.004 * Math.sin(t * 2 + fase);
    corpo.rotation.y = 0.08 * Math.sin(t * 0.6 + fase);
    bracos[1].rotation.z = 0.12 + aceno * (2.4 + 0.35 * Math.sin(t * 9));
  };
  g.userData.atualizar(0);
  return sombras(g);
}
