// Props de segurança do trabalho, engenharia, incêndio e saúde ocupacional (ECASI). Pacote inicial:
// a biblioteca cresce um vídeo de cada vez. Todos recebem THREE e devolvem THREE.Group com a base em y=0.
import { mat, sombras, texturaCanvas, PALETA } from "./nucleo.js";

const E = PALETA.ecasi;

export function capacete(THREE, { cor = E.amarelo } = {}) {
  const g = new THREE.Group();
  const casco = new THREE.Mesh(new THREE.SphereGeometry(0.12, 24, 14, 0, Math.PI * 2, 0, Math.PI / 2), mat(THREE, cor, 0.45));
  casco.scale.set(1, 0.85, 1.12); casco.position.y = 0.02; g.add(casco);
  const aba = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.15, 0.012, 28), mat(THREE, cor, 0.45)); aba.scale.z = 1.15; aba.position.set(0, 0.02, 0.015); g.add(aba);
  const crista = new THREE.Mesh(new THREE.BoxGeometry(0.025, 0.03, 0.22), mat(THREE, cor, 0.45)); crista.position.y = 0.115; g.add(crista);
  return sombras(g);
}

export function colete(THREE, { cor = E.laranja } = {}) {
  const g = new THREE.Group();
  const corpo = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.4, 0.04), mat(THREE, cor, 0.6)); corpo.position.y = 0.2; g.add(corpo);
  const refl = mat(THREE, "#e8edf2", 0.2, { metalness: 0.3 });
  for (const y of [0.12, 0.26]) { const f = new THREE.Mesh(new THREE.BoxGeometry(0.345, 0.035, 0.045), refl); f.position.y = y; g.add(f); }
  return sombras(g);
}

export function cone(THREE, { altura = 0.4 } = {}) {
  const g = new THREE.Group();
  const base = new THREE.Mesh(new THREE.BoxGeometry(altura * 0.65, 0.025, altura * 0.65), mat(THREE, E.laranja, 0.6)); base.position.y = 0.0125; g.add(base);
  const c = new THREE.Mesh(new THREE.ConeGeometry(altura * 0.25, altura, 24), mat(THREE, E.laranja, 0.55)); c.position.y = altura / 2 + 0.02; g.add(c);
  for (const [y, r] of [[0.45, 0.14], [0.7, 0.08]]) { const f = new THREE.Mesh(new THREE.CylinderGeometry(altura * r * 0.96, altura * (r + 0.03), altura * 0.1, 24, 1, true), mat(THREE, "#ffffff", 0.3)); f.position.y = altura * y; g.add(f); }
  return sombras(g);
}

export function extintor(THREE, { altura = 0.5, classe = "PQS" } = {}) {
  const g = new THREE.Group();
  const corpo = new THREE.Mesh(new THREE.CylinderGeometry(altura * 0.16, altura * 0.16, altura * 0.8, 24), mat(THREE, E.vermelho, 0.35)); corpo.position.y = altura * 0.4; g.add(corpo);
  const cupula = new THREE.Mesh(new THREE.SphereGeometry(altura * 0.16, 20, 10, 0, Math.PI * 2, 0, Math.PI / 2), mat(THREE, E.vermelho, 0.35)); cupula.position.y = altura * 0.8; g.add(cupula);
  const valv = new THREE.Mesh(new THREE.BoxGeometry(altura * 0.12, altura * 0.08, altura * 0.12), mat(THREE, "#2b2f3a", 0.4)); valv.position.y = altura * 0.98; g.add(valv);
  const gat = new THREE.Mesh(new THREE.BoxGeometry(altura * 0.04, altura * 0.02, altura * 0.22), mat(THREE, "#2b2f3a", 0.4)); gat.position.set(0, altura * 1.04, altura * 0.06); g.add(gat);
  const mang = new THREE.Mesh(new THREE.TorusGeometry(altura * 0.2, altura * 0.018, 8, 20, Math.PI * 0.9), mat(THREE, "#1d2129", 0.6)); mang.position.set(altura * 0.16, altura * 0.75, 0); mang.rotation.z = -Math.PI / 2; g.add(mang);
  const tex = texturaCanvas(THREE, 256, 128, (c, w, h) => { c.fillStyle = "#fff"; c.fillRect(0, 0, w, h); c.fillStyle = E.ink; c.font = "bold 64px sans-serif"; c.textAlign = "center"; c.fillText(classe, w / 2, h * 0.68); });
  const rot = new THREE.Mesh(new THREE.CylinderGeometry(altura * 0.162, altura * 0.162, altura * 0.22, 24, 1, true, -0.8, 1.6), new THREE.MeshStandardMaterial({ map: tex, roughness: 0.6 }));
  rot.position.y = altura * 0.42; g.add(rot);
  return sombras(g);
}

// placa: tipo "aviso" (triângulo amarelo), "proibido" (círculo vermelho), "obrigatorio" (círculo azul), "saida" (retângulo verde)
export function placa(THREE, { tipo = "aviso", simbolo = "!", texto = "", largura = 0.4, comPoste = false } = {}) {
  const g = new THREE.Group();
  const tex = texturaCanvas(THREE, 512, 512, (c, w, h) => {
    c.clearRect(0, 0, w, h); c.textAlign = "center"; c.textBaseline = "middle";
    if (tipo === "aviso") {
      c.fillStyle = E.amarelo; c.strokeStyle = "#111"; c.lineWidth = 26; c.lineJoin = "round";
      c.beginPath(); c.moveTo(w / 2, 40); c.lineTo(w - 30, h - 60); c.lineTo(30, h - 60); c.closePath(); c.fill(); c.stroke();
      c.fillStyle = "#111"; c.font = "bold 230px sans-serif"; c.fillText(simbolo, w / 2, h * 0.62);
    } else if (tipo === "saida") {
      c.fillStyle = E.verde; c.fillRect(0, h * 0.25, w, h * 0.5);
      c.fillStyle = "#fff"; c.font = "bold 120px sans-serif"; c.fillText(texto || "SAÍDA", w / 2, h * 0.5);
    } else {
      const cor = tipo === "proibido" ? E.vermelho : E.azul;
      c.fillStyle = tipo === "proibido" ? "#fff" : cor; c.beginPath(); c.arc(w / 2, h / 2, w * 0.45, 0, 7); c.fill();
      c.lineWidth = 40; c.strokeStyle = cor; c.stroke();
      c.fillStyle = tipo === "proibido" ? "#111" : "#fff"; c.font = "bold 200px sans-serif"; c.fillText(simbolo, w / 2, h * 0.53);
      if (tipo === "proibido") { c.beginPath(); c.moveTo(w * 0.2, h * 0.2); c.lineTo(w * 0.8, h * 0.8); c.lineWidth = 40; c.strokeStyle = cor; c.stroke(); }
    }
    if (texto && tipo !== "saida") { c.fillStyle = "#111"; c.font = "bold 60px sans-serif"; c.fillText(texto, w / 2, h - 22); }
  });
  const p = new THREE.Mesh(new THREE.PlaneGeometry(largura, largura), new THREE.MeshStandardMaterial({ map: tex, transparent: true, alphaTest: 0.1, roughness: 0.5, side: THREE.DoubleSide }));
  p.position.y = comPoste ? 1.1 : largura / 2; g.add(p);
  if (comPoste) { const h = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 1.1, 8), mat(THREE, "#9aa3ad", 0.4)); h.position.set(0, 0.55, -0.02); g.add(h); }
  return sombras(g, true, false);
}

export function maletaPrimeirosSocorros(THREE) {
  const g = new THREE.Group();
  const c = new THREE.Mesh(new THREE.BoxGeometry(0.36, 0.24, 0.12), mat(THREE, "#ffffff", 0.4)); c.position.y = 0.12; g.add(c);
  const m = mat(THREE, E.verde, 0.5);
  const v = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.14, 0.01), m); v.position.set(0, 0.12, 0.062); g.add(v);
  const h = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.05, 0.01), m); h.position.set(0, 0.12, 0.062); g.add(h);
  const alca = new THREE.Mesh(new THREE.TorusGeometry(0.05, 0.01, 6, 16, Math.PI), mat(THREE, "#2b2f3a")); alca.position.y = 0.24; g.add(alca);
  return sombras(g);
}

// quadro elétrico simples (porta abre com abertura 0..1)
export function quadroEletrico(THREE, { abertura = 0 } = {}) {
  const g = new THREE.Group();
  const cx = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.65, 0.14), mat(THREE, "#d9dee5", 0.4)); cx.position.y = 0.325; g.add(cx);
  const din = mat(THREE, "#ffffff", 0.5), alav = mat(THREE, E.ink, 0.5);
  for (let i = 0; i < 6; i++) { const d = new THREE.Mesh(new THREE.BoxGeometry(0.055, 0.1, 0.05), din); d.position.set(-0.15 + i * 0.06, 0.4, 0.06); g.add(d); const a = new THREE.Mesh(new THREE.BoxGeometry(0.015, 0.03, 0.02), alav); a.position.set(-0.15 + i * 0.06, 0.41, 0.09); g.add(a); }
  const porta = new THREE.Group(); porta.position.set(-0.25, 0, 0.075);
  const pp = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.65, 0.015), mat(THREE, "#c5ccd6", 0.4)); pp.position.set(0.25, 0.325, 0); porta.add(pp);
  const raio = new THREE.Mesh(new THREE.PlaneGeometry(0.16, 0.16), new THREE.MeshBasicMaterial({ map: texturaCanvas(THREE, 128, 128, (c, w, h) => { c.fillStyle = E.amarelo; c.beginPath(); c.moveTo(w / 2, 8); c.lineTo(w - 8, h - 12); c.lineTo(8, h - 12); c.closePath(); c.fill(); c.fillStyle = "#111"; c.font = "bold 70px sans-serif"; c.textAlign = "center"; c.fillText("⚡", w / 2, h * 0.78); }), transparent: true }));
  raio.position.set(0.25, 0.45, 0.009); porta.add(raio);
  porta.rotation.y = -abertura * 1.9; g.add(porta); g.userData.porta = porta;
  return sombras(g);
}

export function luvas(THREE, { cor = E.amarelo } = {}) {
  const g = new THREE.Group();
  for (const s of [-1, 1]) {
    const p = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.025, 0.12), mat(THREE, cor, 0.8)); p.position.set(s * 0.06, 0.013, 0); p.rotation.y = s * 0.2; g.add(p);
    const d = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.022, 0.05), mat(THREE, cor, 0.8)); d.position.set(s * 0.1, 0.012, -0.05); g.add(d);
  }
  return sombras(g);
}

export function oculosProtecao(THREE) {
  const g = new THREE.Group();
  const lente = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.05, 0.02), new THREE.MeshStandardMaterial({ color: "#bfe3ff", roughness: 0.1, transparent: true, opacity: 0.6 })); lente.position.y = 0.03; g.add(lente);
  const arm = mat(THREE, E.ink);
  for (const s of [-1, 1]) { const h = new THREE.Mesh(new THREE.BoxGeometry(0.01, 0.01, 0.12), arm); h.position.set(s * 0.08, 0.04, -0.06); g.add(h); }
  return sombras(g);
}
