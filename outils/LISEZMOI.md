# Outils des visuels Kazaia (réseaux sociaux)

Ce dépôt ne contient que des visuels de communication : jamais de donnée d'un foyer, jamais de vidéo ni de musique d'un autre créateur.

Installation (une fois par session) : `npm install` à la racine (Playwright ; le navigateur Chromium est déjà présent dans l'environnement). ffmpeg et Python 3 (numpy, scipy) sont requis.

## Niveau attendu

Très classe, animé, intrigant : on doit avoir envie de regarder jusqu'au bout. Nuit bleue, or en feuille, crème, typographie Fraunces (titres, souvent en italique pour l'accent) + Inter. Une seule idée par contenu, une accroche lisible à la 1re image, une révélation (tease → reveal), une fin qui renvoie au quiz. Exemples validés : `semaines/2026-10-26/`.

## Fichiers

- `base.css` : charte et composants — `.reel` (1080×1920), `.scene` (scènes plein écran avec zoom caméra), `.slide` / `.slide.sombre` (1080×1350, cadre doré), `.titre`, `.kicker`, `.or` (texte or en feuille), `.chrono`, `.notif` / `.notif.or` (cartes « rappel » en verre dépoli, fictives), `.pastille`, `.bouton`, `.filet`, `.halo`, `.rayon`, `.vignette`, `.grain`, `canvas.poussiere`.
- `base.js` : animations pilotées par le temps. Attributs : `data-in`, `data-out`, `data-dur`, `data-anim` (`up`, `fade`, `scale`, `left`, `blur`, `wipe`, `words`, `type`, `drop`), `data-shine` (reflet doré), `data-shake` (tremblement entre deux instants), `data-zoom` sur `.scene`. Accroche visible dès la 1re image : `data-in="0" data-dur="0.01"`.
- `musique.py` : bande-son originale composée par programme (libre de droits). Styles `nuit` (émotion, soir), `lumineux` (soulagement, solution), `elan` (listes, astuces). `--accents` = instants des changements de scène (montée + note cristalline).
- `render-reel.mjs` : `node outils/render-reel.mjs <page.html> <durée_s> <sortie.mp4> --musique nuit --accents 9.6,11.6` → MP4 1080×1920, 30 i/s, musique intégrée à -14 LUFS.
- `render-slides.mjs` : `node outils/render-slides.mjs <page.html> <dossier> <préfixe>` → un PNG par `<section class="slide">`.
- `kazaia-logo.png` (transparent, fonds sombres) · `kazaia-icone.png` (icône de l'app) · `fonts/` (Fraunces, Inter, licence SIL OFL).
- `semaines/AAAA-MM-JJ/` : pages HTML de la semaine (lundi) + `textes.md` (textes, hashtags, sources, commandes de rendu).

## Règles

- Reels 12 à 20 s ; accroche à la 1re image (une scène précise, une heure, un chiffre, une question qui intrigue) ; texte important entre y=200 et y=1450 ; rien dans les 400 px du bas ni les 120 px de droite ; logo + kazaia.fr/verifier en fin ; toujours une musique (`--musique`).
- Carrousels 6 à 8 diapositives : 1re = promesse intrigante, dernières = révélation + appel à l'action (kazaia.fr/verifier).
- Contrôle avant mise en ligne : 6 à 8 images par reel (`ffmpeg -ss <t> -i x.mp4 -frames:v 1 f.png`) et chaque diapositive regardées ; corriger tout chevauchement, débordement ou texte coupé.
- Fichiers finaux dans `media/` (`AAAA-MM-JJ-sujet.mp4`, `AAAA-MM-JJ-sujet-N.png`), servis par GitHub Pages : `https://celine06800.github.io/kazaia-media/media/<fichier>`.
