// Kazaia — animations déterministes des reels (tout dépend de t, aucune horloge).
// render-reel.mjs appelle window.render(t) pour chaque image (30 i/s).
//
// Sur n'importe quel élément :
//   data-in="1.2"   entrée (s)          data-out="6"   sortie (s, facultatif)
//   data-dur="0.6"  durée d'entrée       data-anim=...  type d'animation :
//     up      monte en fondu (défaut)         fade   fondu simple
//     scale   grossit légèrement              left   glisse depuis la gauche
//     blur    sort du flou (élégant)          wipe   se dévoile de gauche à droite (masque)
//     words   mots un par un (flou → net)     type   machine à écrire
//     drop    tombe et rebondit doucement (cartes, notifications)
//   data-shine="2.5" : reflet doré qui balaie l'élément à t=2.5 (texte ou carte)
//   data-shake="7,9" : tremble légèrement entre 7 s et 9 s (surcharge)
//
// Sur .scene : data-zoom="1.00,1.08" zoom lent de caméra sur toute la durée de la scène
//   (avec data-in / data-out pour la scène elle-même).
// .poussiere : particules dorées dans la lumière (canvas automatique).
(function () {
  const clamp = (x) => Math.max(0, Math.min(1, x));
  const easeOut = (x) => 1 - Math.pow(1 - clamp(x), 3);
  const easeInOut = (x) => { x = clamp(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
  const back = (x) => { x = clamp(x); const c = 1.4; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
  const words = new Map(), typed = new Map();

  function splitWords(el) {
    if (words.has(el)) return words.get(el);
    const parts = [];
    const walk = (node) => {
      for (const ch of Array.from(node.childNodes)) {
        if (ch.nodeType === 3) {
          const frag = document.createDocumentFragment();
          ch.textContent.split(/(\s+)/).forEach((w) => {
            if (!w) return;
            if (/^\s+$/.test(w)) { frag.appendChild(document.createTextNode(w)); return; }
            const s = document.createElement("span"); s.textContent = w; s.style.display = "inline-block";
            frag.appendChild(s); parts.push(s);
          });
          ch.replaceWith(frag);
        } else if (ch.nodeType === 1) walk(ch);
      }
    };
    walk(el); words.set(el, parts); return parts;
  }

  function particles(t) {
    document.querySelectorAll("canvas.poussiere").forEach((c) => {
      const ctx = c.getContext("2d"); const W = c.width = c.offsetWidth; const H = c.height = c.offsetHeight;
      ctx.clearRect(0, 0, W, H);
      for (let i = 0; i < 70; i++) {
        const r1 = Math.sin(i * 12.9898) * 43758.5453 % 1, r2 = Math.sin(i * 78.233) * 12345.678 % 1;
        const x = (Math.abs(r1) * W + Math.sin(t * .3 + i) * 30) % W;
        const y = (Math.abs(r2) * H - t * (8 + (i % 7) * 3) + H * 10) % H;
        const a = .25 + .35 * Math.abs(Math.sin(t * .8 + i));
        ctx.fillStyle = `rgba(230,211,163,${a})`;
        ctx.beginPath(); ctx.arc(x, y, 1 + (i % 3), 0, Math.PI * 2); ctx.fill();
      }
    });
  }

  window.render = function (t) {
    for (const el of document.querySelectorAll("[data-in]")) {
      const tin = parseFloat(el.dataset.in);
      const tout = el.dataset.out ? parseFloat(el.dataset.out) : Infinity;
      const dur = el.dataset.dur ? parseFloat(el.dataset.dur) : 0.7;
      const anim = el.dataset.anim || "up";
      const p = clamp((t - tin) / dur), a = easeOut(p);
      const b = easeInOut((t - tout) / 0.5);
      const vis = 1 - b;
      let tf = "";
      if (anim === "words") {
        const ws = splitWords(el); el.style.opacity = t < tin ? 0 : vis;
        const step = dur / Math.max(ws.length, 1);
        ws.forEach((w, i) => { const q = easeOut((t - tin - i * step * .85) / .45);
          w.style.opacity = q; w.style.filter = `blur(${(1 - q) * 10}px)`; w.style.transform = `translateY(${(1 - q) * 18}px)`; });
      } else if (anim === "type") {
        if (!typed.has(el)) typed.set(el, el.textContent);
        const full = typed.get(el); el.textContent = full.slice(0, Math.round(full.length * p));
        el.style.opacity = t < tin ? 0 : vis;
      } else if (anim === "wipe") {
        el.style.opacity = t < tin ? 0 : vis;
        el.style.clipPath = `inset(0 ${100 - 100 * easeInOut(p)}% 0 0)`;
      } else {
        el.style.opacity = a * vis;
        if (anim === "up") tf = `translateY(${46 * (1 - a) - 24 * b}px)`;
        else if (anim === "left") tf = `translateX(${-70 * (1 - a)}px)`;
        else if (anim === "scale") tf = `scale(${.86 + .14 * a})`;
        else if (anim === "drop") tf = `translateY(${-70 * (1 - back(p))}px) scale(${.94 + .06 * back(p)})`;
        else if (anim === "blur") { el.style.filter = `blur(${(1 - a) * 18 + b * 12}px)`; tf = `scale(${1.04 - .04 * a})`; }
      }
      if (el.dataset.shake) {
        const [s0, s1] = el.dataset.shake.split(",").map(parseFloat);
        if (t > s0 && t < s1) { const k = clamp((t - s0) / (s1 - s0)); tf += ` translate(${Math.sin(t * 61) * 4 * k}px, ${Math.cos(t * 47) * 3 * k}px)`; }
      }
      if (tf) el.style.transform = tf;
      if (el.dataset.shine) {
        const s = parseFloat(el.dataset.shine), q = clamp((t - s) / 1.1);
        el.style.setProperty("--shine", `${-30 + 160 * easeInOut(q)}%`);
      }
    }
    for (const sc of document.querySelectorAll(".scene[data-zoom]")) {
      const [z0, z1] = sc.dataset.zoom.split(",").map(parseFloat);
      const tin = parseFloat(sc.dataset.in || 0), tout = parseFloat(sc.dataset.out || 30);
      const k = clamp((t - tin) / Math.max(tout - tin, .1));
      sc.style.setProperty("--zoom", z0 + (z1 - z0) * k);
    }
    const halo = document.querySelector(".halo");
    if (halo) halo.style.transform = `scale(${1 + .05 * Math.sin(t * 1.1)})`;
    particles(t);
    if (window.onRender) window.onRender(t);
  };
  document.addEventListener("DOMContentLoaded", () => window.render(0));
})();
