// Rend une page HTML de reel (1080×1920, window.render(t)) en MP4 30 i/s, avec bande-son originale.
// Usage : node outils/render-reel.mjs <page.html> <durée_s> <sortie.mp4> [--musique nuit|lumineux|elan] [--accents 10.6,13.8] [--graine 7] [--son <fichier.mp3>] [--synthe]
// Depuis le 23/11/2026 : --musique prend un VRAI morceau choisi par Céline (Pixabay) dans outils/sons/<style>/
// (nuit → lumineux), voir outils/sons/SONS.md. L'extrait change selon le nom du fichier de sortie (ou --graine).
// --son impose un extrait ; --synthe garde l'ancienne musique composée par musique.py.
// Sans --musique : MP4 muet. La musique est composée par outils/musique.py (originale, libre de droits),
// puis normalisée à -14 LUFS (niveau des réseaux sociaux).
import { chromium } from "playwright";
import { spawn, execFileSync } from "node:child_process";
import path from "node:path";
import fs from "node:fs";
import os from "node:os";

const args = process.argv.slice(2);
const opt = (k) => { const i = args.indexOf(k); return i >= 0 ? args.splice(i, 2)[1] : undefined; };
const musique = opt("--musique"), accents = opt("--accents") || "", graineOpt = opt("--graine"), graine = graineOpt || "7";
let son = opt("--son"); const synthe = args.includes("--synthe"); if (synthe) args.splice(args.indexOf("--synthe"), 1);
const [page, dureeArg, sortie] = args;
if (!page || !dureeArg || !sortie) {
  console.error("Usage : node outils/render-reel.mjs <page.html> <durée_s> <sortie.mp4> [--musique nuit|lumineux|elan] [--accents t1,t2]");
  process.exit(1);
}
const fps = 30, duree = parseFloat(dureeArg), n = Math.round(duree * fps);
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "reel-"));
const video = musique ? path.join(tmp, "video.mp4") : sortie;

const navigateur = await chromium.launch();
const p = await navigateur.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
await p.goto("file://" + path.resolve(page), { waitUntil: "networkidle" });
await p.evaluate(() => document.fonts.ready);
const ff = spawn("ffmpeg", ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(fps), "-i", "-",
  "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-crf", "17", "-preset", "slow", "-movflags", "+faststart", video],
  { stdio: ["pipe", "inherit", "inherit"] });
const ecran = await p.$(".reel");
for (let i = 0; i < n; i++) {
  await p.evaluate((t) => window.render(t), i / fps);
  const img = await (ecran ?? p).screenshot({ type: "jpeg", quality: 93 });
  if (!ff.stdin.write(img)) await new Promise((r) => ff.stdin.once("drain", r));
}
ff.stdin.end();
await new Promise((r, j) => ff.on("close", (c) => (c === 0 ? r() : j(new Error("ffmpeg " + c)))));
await navigateur.close();

const dossierSons = path.join(path.dirname(new URL(import.meta.url).pathname), "sons");
if (!son && musique && !synthe) {
  const style = musique === "nuit" ? "lumineux" : musique;
  const d = path.join(dossierSons, style);
  const liste = fs.existsSync(d) ? fs.readdirSync(d).filter((f) => f.endsWith(".mp3")).sort() : [];
  if (liste.length) {
    let g = graineOpt !== undefined ? +graineOpt : [...path.basename(sortie)].reduce((h, c) => (h * 31 + c.charCodeAt(0)) >>> 0, 7);
    son = path.join(d, liste[g % liste.length]);
  }
}
if (son) {
  const fin = Math.max(0, duree - 1).toFixed(2);
  execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-i", video, "-i", son, "-map", "0:v", "-map", "1:a",
    "-af", `atrim=0:${duree},afade=t=in:st=0:d=0.2,afade=t=out:st=${fin}:d=1,loudnorm=I=-14:TP=-1.5:LRA=9`, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", sortie]);
} else if (musique) {
  const wav = path.join(tmp, "musique.wav");
  const script = path.join(path.dirname(new URL(import.meta.url).pathname), "musique.py");
  execFileSync("python3", [script, "--style", musique, "--duree", String(duree), "--accents", accents, "--graine", graine, wav], { stdio: "inherit" });
  execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-i", video, "-i", wav, "-map", "0:v", "-map", "1:a",
    "-af", "loudnorm=I=-14:TP=-1.5:LRA=9", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", sortie]);
}
fs.rmSync(tmp, { recursive: true, force: true });
console.log(`OK ${sortie} (${n} images, ${duree} s${son ? ", son " + path.basename(son) : musique ? ", musique synthétique " + musique : ", muet"})`);
