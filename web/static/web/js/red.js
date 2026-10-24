// Cauce — grafo decorativo de la portada: municipios (aqua) conectados con recursos (lavanda).
// Lee los colores de tokens.css. Con "reducir movimiento" se dibuja un solo cuadro estático.
(() => {
  const lienzo = document.getElementById("red-hero");
  if (!lienzo) return;
  const ctx = lienzo.getContext("2d");
  if (!ctx) return;

  const estilos = getComputedStyle(document.documentElement);
  const token = (nombre) => estilos.getPropertyValue(nombre).trim();
  const colorNodo = token("--color-aqua");
  const colorRecurso = token("--color-cifra");
  const colorLinea = token("--rejilla-grafica");

  const reducido = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const TOTAL = 60;
  const DISTANCIA = 140;
  const VELOCIDAD = 0.3;
  let ancho = 0;
  let alto = 0;
  let nodos = [];

  function crearNodos() {
    nodos = Array.from({ length: TOTAL }, (_, i) => ({
      x: Math.random() * ancho,
      y: Math.random() * alto,
      vx: (Math.random() - 0.5) * 2 * VELOCIDAD,
      vy: (Math.random() - 0.5) * 2 * VELOCIDAD,
      radio: 1.5 + Math.random() * 1.5,
      recurso: i % 8 === 0,
    }));
  }

  function ajustarTamano() {
    const escala = window.devicePixelRatio || 1;
    const caja = lienzo.getBoundingClientRect();
    ancho = caja.width;
    alto = caja.height;
    lienzo.width = Math.round(ancho * escala);
    lienzo.height = Math.round(alto * escala);
    ctx.setTransform(escala, 0, 0, escala, 0, 0);
    if (nodos.length === 0) crearNodos();
  }

  function dibujar() {
    ctx.clearRect(0, 0, ancho, alto);
    ctx.lineWidth = 1;
    ctx.strokeStyle = colorLinea;
    for (let i = 0; i < nodos.length; i += 1) {
      for (let j = i + 1; j < nodos.length; j += 1) {
        const dx = nodos[i].x - nodos[j].x;
        const dy = nodos[i].y - nodos[j].y;
        if (dx * dx + dy * dy < DISTANCIA * DISTANCIA) {
          ctx.beginPath();
          ctx.moveTo(nodos[i].x, nodos[i].y);
          ctx.lineTo(nodos[j].x, nodos[j].y);
          ctx.stroke();
        }
      }
    }
    for (const nodo of nodos) {
      ctx.beginPath();
      ctx.fillStyle = nodo.recurso ? colorRecurso : colorNodo;
      ctx.arc(nodo.x, nodo.y, nodo.recurso ? nodo.radio + 1 : nodo.radio, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  function mover() {
    for (const nodo of nodos) {
      nodo.x += nodo.vx;
      nodo.y += nodo.vy;
      if (nodo.x < 0 || nodo.x > ancho) nodo.vx *= -1;
      if (nodo.y < 0 || nodo.y > alto) nodo.vy *= -1;
    }
  }

  function cuadro() {
    if (!document.hidden) {
      mover();
      dibujar();
    }
    window.requestAnimationFrame(cuadro);
  }

  ajustarTamano();
  window.addEventListener("resize", () => {
    ajustarTamano();
    dibujar();
  });

  if (reducido) {
    dibujar();
  } else {
    window.requestAnimationFrame(cuadro);
  }
})();
