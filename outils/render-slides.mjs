// Rend chaque <section class="slide"> (1080×1350) d'une page HTML en PNG.
// Usage : node outils/render-slides.mjs <page.html> <dossier_sortie> <préfixe>
// → <dossier_sortie>/<préfixe>-1.png, -2.png, …
import { chromium } from "playwright";
import path from "node:path";
import fs from "node:fs";

const [, , page, dossier, prefixe] = process.argv;
if (!page || !dossier || !prefixe) {
  console.error("Usage : node outils/render-slides.mjs <page.html> <dossier_sortie> <préfixe>");
  process.exit(1);
}
fs.mkdirSync(dossier, { recursive: true });
const navigateur = await chromium.launch();
const p = await navigateur.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
await p.goto("file://" + path.resolve(page), { waitUntil: "networkidle" });
await p.evaluate(() => document.fonts.ready);
const slides = await p.$$("section.slide");
for (let i = 0; i < slides.length; i++) {
  const f = path.join(dossier, `${prefixe}-${i + 1}.png`);
  await slides[i].screenshot({ path: f });
  console.log("OK", f);
}
await navigateur.close();
