// Cenário externo low-poly colorido: céu, sol, nuvens, árvores, arbustos, flores, cerca, casas vizinhas,
// calçada, rua, poste, caixa de correio, pássaros. Tudo recebe THREE e devolve THREE.Group.
import { mat, rnd, PALETA, sombras } from "./nucleo.js";

// céu em degradê (esfera grande com shader); u.topo/u.base podem ser animados (dia/noite/chuva)
export function ceu(THREE, { topo = "#5fb2ee", base = "#d9f0ff" } = {}) {
  const u = { topo: { value: new THREE.Color(topo) }, base: { value: new THREE.Color(base) } };
  const m = new THREE.ShaderMaterial({
    uniforms: u, side: THREE.BackSide, depthWrite: false,
    vertexShader: "varying vec3 vP; void main(){ vP = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }",
    fragmentShader: `uniform vec3 topo; uniform vec3 base; varying vec3 vP;
      void main(){ float k = smoothstep(-0.05, 0.55, vP.y); gl_FragColor = vec4(mix(base, topo, k), 1.0);
      #include <colorspace_fragment>
      }`,
  });
  const esf = new THREE.Mesh(new THREE.SphereGeometry(60, 32, 16), m);
  esf.userData.cores = u;
  return esf;
}

export function sol(THREE, { raio = 1.2 } = {}) {
  const g = new THREE.Group();
  g.add(new THREE.Mesh(new THREE.CircleGeometry(raio, 40), new THREE.MeshBasicMaterial({ color: "#ffe27a" })));
  const halo = new THREE.Mesh(new THREE.CircleGeometry(raio * 1.8, 40), new THREE.MeshBasicMaterial({ color: "#fff3c4", transparent: true, opacity: 0.35 }));
  halo.position.z = -0.01; g.add(halo);
  return g;
}

export function nuvem(THREE, { seed = 1, escala = 1, cor = "#ffffff" } = {}) {
  const g = new THREE.Group(), r = rnd(seed);
  const m = new THREE.MeshStandardMaterial({ color: cor, roughness: 1, transparent: true, opacity: 1 });
  for (let i = 0; i < 5; i++) {
    const s = new THREE.Mesh(new THREE.SphereGeometry(0.45 + r() * 0.3, 14, 10), m);
    s.position.set((i - 2) * 0.5, r() * 0.25 + (i === 2 ? 0.25 : 0), r() * 0.2);
    s.scale.y = 0.75; g.add(s);
  }
  g.scale.setScalar(escala);
  g.userData.material = m;
  return g;
}

export function arvore(THREE, { seed = 1, altura = 2.2, cor } = {}) {
  const g = new THREE.Group(), r = rnd(seed);
  const tronco = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.11, altura * 0.45, 8), mat(THREE, PALETA.natureza.tronco));
  tronco.position.y = altura * 0.225; g.add(tronco);
  const folhas = [cor || PALETA.natureza.folha, PALETA.natureza.folha2, "#4caf50"];
  for (let i = 0; i < 4; i++) {
    const c = new THREE.Mesh(new THREE.IcosahedronGeometry(altura * (0.22 + r() * 0.1), 1), mat(THREE, folhas[i % 3], 0.9, { flatShading: true }));
    c.position.set((r() - 0.5) * altura * 0.3, altura * (0.55 + r() * 0.25), (r() - 0.5) * altura * 0.25);
    g.add(c);
  }
  return sombras(g, true, false);
}

export function arbusto(THREE, { seed = 2, raio = 0.3, cor = PALETA.natureza.folha2, flores = true } = {}) {
  const g = new THREE.Group(), r = rnd(seed);
  for (let i = 0; i < 3; i++) {
    const b = new THREE.Mesh(new THREE.IcosahedronGeometry(raio * (0.7 + r() * 0.4), 1), mat(THREE, cor, 0.9, { flatShading: true }));
    b.position.set((i - 1) * raio * 0.8, raio * 0.6, (r() - 0.5) * raio * 0.4); g.add(b);
  }
  if (flores) for (let i = 0; i < 7; i++) {
    const f = new THREE.Mesh(new THREE.SphereGeometry(raio * 0.12, 8, 6), mat(THREE, PALETA.flores[i % PALETA.flores.length], 0.6));
    const a = r() * Math.PI * 2; f.position.set(Math.cos(a) * raio * 1.1, raio * (0.6 + r() * 0.7), Math.sin(a) * raio * 0.6 + raio * 0.3); g.add(f);
  }
  return sombras(g, true, false);
}

// canteiro com muitas flores (instanciado: barato para renderizar)
export function canteiro(THREE, { largura = 2, profundidade = 0.35, n = 60, seed = 3 } = {}) {
  const g = new THREE.Group(), r = rnd(seed);
  const terra = new THREE.Mesh(new THREE.BoxGeometry(largura, 0.06, profundidade), mat(THREE, PALETA.natureza.terra));
  terra.position.y = 0.03; terra.receiveShadow = true; g.add(terra);
  const caule = new THREE.InstancedMesh(new THREE.CylinderGeometry(0.006, 0.006, 0.14, 4), mat(THREE, "#3f8f3a"), n);
  const flor = new THREE.InstancedMesh(new THREE.IcosahedronGeometry(0.035, 0), new THREE.MeshStandardMaterial({ roughness: 0.6 }), n);
  const m4 = new THREE.Matrix4(), cor = new THREE.Color();
  for (let i = 0; i < n; i++) {
    const x = (r() - 0.5) * largura * 0.95, z = (r() - 0.5) * profundidade * 0.8, h = 0.08 + r() * 0.08;
    m4.makeTranslation(x, 0.06 + h / 2, z); caule.setMatrixAt(i, m4);
    m4.makeTranslation(x, 0.06 + h, z); flor.setMatrixAt(i, m4);
    flor.setColorAt(i, cor.set(PALETA.flores[Math.floor(r() * PALETA.flores.length)]));
  }
  flor.castShadow = true; g.add(caule, flor);
  return g;
}

export function cerca(THREE, { comprimento = 3, altura = 0.45, cor = "#ffffff", passo = 0.16 } = {}) {
  const g = new THREE.Group(), n = Math.floor(comprimento / passo);
  const ripa = new THREE.InstancedMesh(new THREE.BoxGeometry(0.06, altura, 0.025), mat(THREE, cor, 0.7), n);
  const m4 = new THREE.Matrix4();
  for (let i = 0; i < n; i++) { m4.makeTranslation(-comprimento / 2 + i * passo, altura / 2, 0); ripa.setMatrixAt(i, m4); }
  ripa.castShadow = true; g.add(ripa);
  for (const y of [altura * 0.3, altura * 0.75]) { const t = new THREE.Mesh(new THREE.BoxGeometry(comprimento, 0.04, 0.03), mat(THREE, cor, 0.7)); t.position.set(-passo / 2, y, -0.02); g.add(t); }
  return g;
}

// casa simples colorida (para o fundo)
export function casaVizinha(THREE, { cor = "#ffb84d", telhado = "#c2553c", largura = 2.4, altura = 1.6, seed = 4 } = {}) {
  const g = new THREE.Group();
  const corpo = new THREE.Mesh(new THREE.BoxGeometry(largura, altura, 1.8), mat(THREE, cor)); corpo.position.y = altura / 2; g.add(corpo);
  const s = new THREE.Shape(); s.moveTo(-largura / 2 - 0.15, 0); s.lineTo(0, 0.8); s.lineTo(largura / 2 + 0.15, 0); s.lineTo(-largura / 2 - 0.15, 0);
  const tel = new THREE.Mesh(new THREE.ExtrudeGeometry(s, { depth: 2.0, bevelEnabled: false }), mat(THREE, telhado)); tel.position.set(0, altura, -1.0); g.add(tel);
  const jan = mat(THREE, "#bfe3ff", 0.4), mold = mat(THREE, "#ffffff", 0.6);
  for (const x of [-largura * 0.25, largura * 0.25]) {
    const m = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.5, 0.04), mold); m.position.set(x, altura * 0.6, 0.91); g.add(m);
    const j = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.4, 0.05), jan); j.position.set(x, altura * 0.6, 0.92); g.add(j);
  }
  return sombras(g, true, true);
}

export function chao(THREE, { tamanho = 60, cor = PALETA.natureza.grama } = {}) {
  const m = new THREE.Mesh(new THREE.PlaneGeometry(tamanho, tamanho), mat(THREE, cor));
  m.rotation.x = -Math.PI / 2; m.receiveShadow = true; return m;
}

export function calcada(THREE, { largura = 6, profundidade = 1.8, cor = "#d8d2c6" } = {}) {
  const g = new THREE.Group();
  const p = new THREE.Mesh(new THREE.BoxGeometry(largura, 0.04, profundidade), mat(THREE, cor)); p.position.y = 0.02; p.receiveShadow = true; g.add(p);
  const junta = mat(THREE, "#c2bbad");
  for (let x = -largura / 2 + 0.6; x < largura / 2; x += 0.6) { const j = new THREE.Mesh(new THREE.BoxGeometry(0.012, 0.042, profundidade), junta); j.position.set(x, 0.021, 0); g.add(j); }
  return g;
}

export function rua(THREE, { largura = 30, profundidade = 3 } = {}) {
  const g = new THREE.Group();
  const a = new THREE.Mesh(new THREE.PlaneGeometry(largura, profundidade), mat(THREE, "#555b66")); a.rotation.x = -Math.PI / 2; a.position.y = 0.005; a.receiveShadow = true; g.add(a);
  for (let x = -largura / 2; x < largura / 2; x += 1.2) { const f = new THREE.Mesh(new THREE.PlaneGeometry(0.6, 0.08), mat(THREE, "#ffe066")); f.rotation.x = -Math.PI / 2; f.position.set(x, 0.007, 0); g.add(f); }
  const guia = new THREE.Mesh(new THREE.BoxGeometry(largura, 0.1, 0.12), mat(THREE, "#e9e5dc")); guia.position.set(0, 0.05, -profundidade / 2); g.add(guia);
  return g;
}

export function poste(THREE, { altura = 3 } = {}) {
  const g = new THREE.Group();
  const p = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.05, altura, 8), mat(THREE, "#9aa3ad", 0.5)); p.position.y = altura / 2; g.add(p);
  const b = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.06, 0.08), mat(THREE, "#9aa3ad", 0.5)); b.position.set(0.22, altura - 0.05, 0); g.add(b);
  const l = new THREE.Mesh(new THREE.SphereGeometry(0.07, 12, 8), new THREE.MeshStandardMaterial({ color: "#fff6c8", emissive: "#ffe27a", emissiveIntensity: 0.6 })); l.position.set(0.45, altura - 0.1, 0); g.add(l);
  g.userData.lampada = l.material;
  return sombras(g, true, false);
}

export function caixaCorreio(THREE, { cor = "#d7263d" } = {}) {
  const g = new THREE.Group();
  const p = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.6, 0.05), mat(THREE, "#8a5a35")); p.position.y = 0.3; g.add(p);
  const c = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.16, 0.28), mat(THREE, cor, 0.5)); c.position.y = 0.66; g.add(c);
  const f = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.1, 0.03), mat(THREE, "#ffc928")); f.position.set(0.11, 0.7, 0.05); g.add(f);
  return sombras(g, true, false);
}

export function vaso(THREE, { cor = "#e8743b", planta = PALETA.natureza.folha2, seed = 5 } = {}) {
  const g = new THREE.Group();
  const v = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.08, 0.18, 14), mat(THREE, cor, 0.7)); v.position.y = 0.09; g.add(v);
  const a = arbusto(THREE, { seed, raio: 0.12, cor: planta }); a.position.y = 0.14; g.add(a);
  return sombras(g, true, false);
}

// pássaros voando (posição depende só de t)
export function passaros(THREE, { n = 3, seed = 6 } = {}) {
  const g = new THREE.Group(), r = rnd(seed), aves = [];
  const m = mat(THREE, "#2b2f3a", 0.8, { side: THREE.DoubleSide });
  for (let i = 0; i < n; i++) {
    const ave = new THREE.Group();
    for (const s of [-1, 1]) { const asa = new THREE.Mesh(new THREE.PlaneGeometry(0.16, 0.05), m); asa.position.x = s * 0.08; ave.add(asa); }
    ave.userData = { fase: r() * 6, vel: 0.5 + r() * 0.3, y: r() * 0.6, z: r() * 0.8 };
    g.add(ave); aves.push(ave);
  }
  g.userData.atualizar = (t) => aves.forEach((a) => {
    const u = a.userData; a.position.set(((t * u.vel + u.fase) % 12) - 6, u.y, u.z);
    const bat = Math.sin(t * 12 + u.fase) * 0.6; a.children[0].rotation.z = bat; a.children[1].rotation.z = -bat;
  });
  return g;
}
