// Núcleo da biblioteca de componentes 3D (Three.js) para os vídeos da ECASI e da House.
// Regra de todos os módulos: recebem THREE por parâmetro (não importam "three"), devolvem THREE.Group
// e todo movimento depende só do tempo t (render determinístico: qualquer quadro, em qualquer ordem).

export const PALETA = {
  house: { azul: "#2457d6", marinho: "#1b2f8a", ink: "#0b1220", claro: "#8db4f6", creme: "#efd6a0", verde: "#1a9e4b" },
  ecasi: { laranja: "#f28c28", amarelo: "#ffc928", vermelho: "#d7263d", verde: "#1a9e4b", azul: "#1f6fd1", cinza: "#5b6573", ink: "#121826" },
  natureza: { grama: "#7fbf4d", gramaEsc: "#5f9e3a", folha: "#3f9d4a", folha2: "#62b85a", tronco: "#8a5a35", terra: "#8c6a4a", ceu: "#9fd3f5", agua: "#7fb6ff" },
  flores: ["#ff5d8f", "#ffc928", "#ff8a3d", "#b05cff", "#ffffff", "#ff4d4d"],
  vivas: ["#ff6b6b", "#ffb84d", "#ffe066", "#7bd389", "#4dabf7", "#9775fa", "#f783ac"],
};

// cache de materiais por cor (menos objetos na GPU)
const _mats = new Map();
export function mat(THREE, cor, rough = 0.85, extra = {}) {
  const k = cor + "|" + rough + "|" + JSON.stringify(extra);
  if (!_mats.has(k)) _mats.set(k, new THREE.MeshStandardMaterial({ color: cor, roughness: rough, metalness: 0, ...extra }));
  return _mats.get(k);
}

export function rnd(seed) { let s = seed >>> 0 || 1; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }
export const sm = (a, b, t) => { const x = Math.min(1, Math.max(0, (t - a) / (b - a))); return x * x * (3 - 2 * x); };
export const lerp = (a, b, k) => a + (b - a) * k;
export const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));

// "pop" com mola: 0 antes de t0, passa de 1 e assenta (para objetos que entram em cena)
export function pop(t, t0, dur = 0.55) {
  if (t <= t0) return 0;
  const x = (t - t0) / dur;
  if (x >= 1) return 1;
  return 1 + Math.sin(x * Math.PI * 1.5) * Math.exp(-x * 4) * 0.35 - (1 - x) ** 3;
}
// aplica o pop na escala de um objeto (guarda a escala original na primeira chamada)
export function aplicarPop(obj, t, t0, dur) {
  if (!obj.userData.escala0) obj.userData.escala0 = obj.scale.clone();
  const k = Math.max(0.0001, pop(t, t0, dur));
  obj.scale.copy(obj.userData.escala0).multiplyScalar(k);
  obj.visible = t > t0;
}

export function sombras(obj, lanca = true, recebe = true) {
  obj.traverse((o) => { if (o.isMesh) { o.castShadow = lanca; o.receiveShadow = recebe; } });
  return obj;
}

// renderer + luz padrão "animação 3D" (ACES, sombra suave, ambiente RoomEnvironment)
export function palco(THREE, RoomEnvironment, canvas, { largura = 1080, altura = 1920, sombra = 2048 } = {}) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1);
  renderer.setSize(largura, altura, false);
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  const scene = new THREE.Scene();
  scene.environment = new THREE.PMREMGenerator(renderer).fromScene(new RoomEnvironment(), 0.04).texture;
  scene.environmentIntensity = 0.55;
  const sol = new THREE.DirectionalLight("#fff0d8", 2.4);
  sol.castShadow = true; sol.shadow.mapSize.set(sombra, sombra); sol.shadow.bias = -0.0005;
  Object.assign(sol.shadow.camera, { left: -5, right: 5, top: 5, bottom: -2, near: 0.5, far: 25 });
  const hemi = new THREE.HemisphereLight("#cfe3ff", "#9fb27a", 0.6);
  scene.add(sol, sol.target, hemi);
  const camera = new THREE.PerspectiveCamera(36, largura / altura, 0.05, 120);
  return { renderer, scene, camera, sol, hemi };
}

// textura desenhada em canvas 2D (placas, rótulos, paredes)
export function texturaCanvas(THREE, w, h, desenhar) {
  const cv = document.createElement("canvas"); cv.width = w; cv.height = h;
  const g = cv.getContext("2d"); desenhar(g, w, h);
  const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
  return tex;
}
