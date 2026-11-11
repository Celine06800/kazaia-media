// Rend chaque <section class="story"> (1080×1920) ou <section class="couv"> (1080×1080) d'une page HTML en PNG.
// Usage : node outils/render-stories.mjs <page.html> <dossier_sortie> <préfixe> [story|couv]
// → <dossier_sortie>/<préfixe>-1.png, -2.png, …
import { chromium } from "playwright";
import path from "node:path";
import fs from "node:fs";

const [, , page, dossier, prefixe, type = "story"] = process.argv;
if (!page || !dossier || !prefixe) {
  console.error("Usage : node outils/render-stories.mjs <page.html> <dossier_sortie> <préfixe> [story|couv]");
  process.exit(1);
}
fs.mkdirSync(dossier, { recursive: true });
const navigateur = await chromium.launch();
const p = await navigateur.newPage({ viewport: { width: 1080, height: type === "couv" ? 1080 : 1920 }, deviceScaleFactor: 1 });
await p.goto("file://" + path.resolve(page), { waitUntil: "networkidle" });
await p.evaluate(() => document.fonts.ready);
const sections = await p.$$("section." + type);
for (let i = 0; i < sections.length; i++) {
  const f = path.join(dossier, `${prefixe}-${i + 1}.png`);
  await sections[i].screenshot({ path: f });
  console.log("OK", f);
}
await navigateur.close();
