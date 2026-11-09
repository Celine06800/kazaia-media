# Kazaia · semaine du 9 novembre 2026

Statut : préparés le 09/11/2026 dans la conversation avec Céline. La tâche du lundi a tourné de 6 h 38 à 7 h 01 sans rien produire ni prévenir, comme le 02/11. Brouillons Metricool marque 7477853, à valider par Céline.

## Analyse (28 jours, Metricool, reels Instagram)
- Nos reels progressent : « Message de A. » 445 de portée / 541 vues, « 3 questions » 372 / 466, « 23:47 » 378 / 438. « Contrôle technique » reste plus bas : 211 / 234.
- Les extraits de podcasts gardent l'essentiel de la portée (le burn-out : 38 709 le 03/11). Ils sont comptés à part.
- Décisions :
  - garder le récit de nuit à la 1re personne, le format qui marche le mieux chez nous (« Message de A. ») ;
  - montrer une interface du quotidien (note, jauge, écran) plutôt que du texte seul ;
  - une révélation courte avant Kazaia.

## Tendances
Aucune tendance précise retenue cette semaine : la recherche web n'a donné que des synthèses génériques sur 2026. On garde le format « écran du quotidien » (notes, notifications), en continuité de « Message de A. ».

## Lundi 09/11 · 18:00 · La charge invisible · reel 17,5 s · musique « nuit »
- Fichier : `media/2026-11-09-la-liste.mp4` (source `lundi-la-liste.html`).
- Rendu : `node outils/render-reel.mjs outils/semaines/2026-11-09/lundi-la-liste.html 17.5 media/2026-11-09-la-liste.mp4 --musique nuit --accents 2.9,10.0,12.4,15.0`
- Déroulé :
  - 02:47 : « Je fais juste une petite liste. »
  - La note « À ne pas oublier » se remplit et déborde : 23 lignes, compteur rouge, « 03:31. Elle écrit encore. »
  - « Ce n'est pas une liste. C'est ta nuit. »
  - Rappel Kazaia J-30 : « Carte d'identité de Noé ».
  - Fin : test sur kazaia.fr/verifier.
- Prénoms fictifs.

## Mercredi 11/11 · 12:00 · Fais le test · reel 17 s · musique « elan »
- Fichier : `media/2026-11-09-jour-ferie.mp4` (source `mercredi-jour-ferie.html`).
- Rendu : `node outils/render-reel.mjs outils/semaines/2026-11-09/mercredi-jour-ferie.html 17 media/2026-11-09-jour-ferie.mp4 --musique elan --accents 2.8,5.2,8.4,11.4,13.8`
- Déroulé :
  - « Jour férié. Sauf pour ta tête. »
  - Une jauge de charge mentale monte au fil de la journée : 8 h, 12 h, 16 h, 21 h. Elle passe au rouge et affiche « ? ».
  - « Un jour de repos. Pas pour elle. »
  - Fin : « Le vrai chiffre ? Fais le test. »
- Les chiffres de la jauge sont illustratifs. Ce ne sont pas ceux du quiz.

## Vendredi 13/11 · 18:00 · Le papier qui coûte cher · reel 18 s · musique « nuit »
- Fichier : `media/2026-11-09-garantie.mp4` (source `vendredi-garantie.html`).
- Rendu : `node outils/render-reel.mjs outils/semaines/2026-11-09/vendredi-garantie.html 18 media/2026-11-09-garantie.mp4 --musique nuit --accents 3.1,7.1,11.0,13.0,15.8`
- Situation fictive (Julie) :
  - le lave-linge affiche E21 ;
  - facture du 14/10/2024 : garantie finie depuis un mois ;
  - les règles : 2 ans de garantie légale de conformité sur un produit neuf ; réparation ou remplacement sans frais pendant ces 2 ans ; après, souvent à ses frais, sauf garantie commerciale ;
  - « Elle avait la facture. Pas la date. » ;
  - rappel Kazaia J-30 « Fin de garantie » ;
  - fin : 30 jours d'essai sans carte bancaire.
- Source : service-public.fr, « Achat d'un produit : garantie légale de conformité » (F11094), page vérifiée le 17/08/2026, consultée le 09/11/2026.
- Fin de garantie dans Kazaia : événement `warranty_end` dans src/lib/events.ts. Plan Essentiel : « Achats, Garanties & Avoirs + alertes » et e-mails J-30 / J-7 (src/lib/plans.ts).

## Dimanche 15/11 · 10:00 · À garder · carrousel 8 diapositives
- Fichiers : `media/2026-11-09-kit-urgence-1.png` à `-8.png` (source `dimanche-kit-urgence.html`).
- Rendu : `node outils/render-slides.mjs outils/semaines/2026-11-09/dimanche-kit-urgence.html media 2026-11-09-kit-urgence`
- « Les 6 papiers à retrouver en 2 minutes » :
  1. carte Vitale et attestation de droits ;
  2. carnet de santé de chaque enfant ;
  3. carte de mutuelle ;
  4. pièces d'identité de toute la famille ;
  5. contrat d'assurance habitation et son numéro ;
  6. ordonnances en cours.
- Pas de règle chiffrée, donc pas de source réglementaire.

## Story « Ton score ? » (à publier par Céline, sticker lien vers https://kazaia.fr/verifier)
« Ta liste de 2 h du matin fait combien de lignes ? 🌙 Ton score de charge mentale sur 100, en 2 minutes. »
