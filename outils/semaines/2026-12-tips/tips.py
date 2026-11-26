import re,json
N=" "
def fr(s): s=re.sub(r" ([?!:;»])", N+r"\1", s); s=re.sub(r"« ", "«"+N, s); return s
T=[
("2026-12-01","budget","Budget","Le budget cadeaux, <em>tu le fixes quand</em> ?","Avant le premier achat. Sinon, jamais.","Écris une somme par personne sur une liste. Tu coches au fur et à mesure."),
("2026-12-02","ecole","École","Le spectacle de Noël, <em>c'est quel jour</em> ?","Le mot est arrivé il y a deux semaines.","Dès qu'une date arrive de l'école, elle va dans l'agenda familial. Le papier peut partir."),
("2026-12-03","sante","Santé","Les vaccins des enfants, <em>à jour</em> ?","La question tombe toujours au mauvais moment.","Photographie les pages vaccins du carnet de santé. Tu les as sur toi, partout."),
("2026-12-04","maison","Maison","Tu pars <em>pour les fêtes</em> ?","La maison reste seule quelques jours.","Relève tes compteurs avant de partir et prends-les en photo. En cas de souci, tu as ta preuve."),
("2026-12-05","organisation","Organisation","La liste de cadeaux, <em>dans ta tête</em> ?","Elle se perd entre deux magasins.","Une note partagée « Cadeaux » : qui, quoi, acheté ou pas. Toute la famille la voit."),
("2026-12-06","charge-mentale","Charge mentale","Noël, <em>c'est encore toi</em> ?","Les autres attendent qu'on leur dise.","Confie une mission entière : le repas, les cadeaux des cousins ou la déco. Du début à la fin."),
("2026-12-07","papiers","Papiers","La facture du gros achat, <em>rangée</em> ?","Elle prouve la garantie et la valeur.","Un dossier « Achats importants » : facture, garantie, notice. Il sert le jour d'un sinistre."),
("2026-12-08","budget","Budget","Les petits achats <em>de décembre</em> ?","Ce sont eux qui font déborder le mois.","Chaque soir, note ce que tu as dépensé dans la journée. Deux minutes, et tu vois venir."),
("2026-12-09","ecole","École","La liste de fournitures <em>de janvier</em> ?","Elle arrive toujours la veille.","Demande-la avant les vacances et range-la dans l'album « École »."),
("2026-12-10","sante","Santé","Ton ordonnance <em>expire pendant les fêtes</em> ?","Les cabinets ferment, les rendez-vous se raréfient.","Regarde dès maintenant la date de tes ordonnances en cours et prends rendez-vous si besoin."),
("2026-12-11","maison","Maison","Le détecteur de fumée, <em>testé</em> ?","Un bouton, trois secondes.","Appuie sur le bouton test de chaque détecteur. Pas de bip ? Change la pile."),
("2026-12-12","organisation","Organisation","Les courses du réveillon, <em>au dernier moment</em> ?","Les rayons seront vides le 24.","Fais la liste maintenant et achète ce qui se garde. Le reste, en drive."),
("2026-12-13","charge-mentale","Charge mentale","Tu dis oui <em>à tout</em> en décembre ?","Les invitations s'enchaînent.","Choisis deux soirées qui comptent vraiment. Pour les autres, un non poli suffit."),
("2026-12-14","papiers","Papiers","Tes avis d'impôt, <em>tu les retrouves</em> ?","On te les demande souvent : logement, crédit, aides.","Télécharge-les sur ton espace impots.gouv.fr et range-les dans un dossier « Impôts », une année par fichier."),
("2026-12-15","budget","Budget","Un cadeau payé <em>en plusieurs fois</em> ?","Les prélèvements arrivent en janvier.","Note chaque échéance dans ton agenda dès l'achat. Janvier ne te surprendra pas."),
("2026-12-16","ecole","École","Le bulletin du trimestre, <em>rangé</em> ?","On te le redemandera pour une inscription.","Scanne chaque bulletin dès réception, dans un dossier par enfant et par année."),
("2026-12-17","sante","Santé","La trousse à pharmacie <em>des vacances</em> ?","On l'oublie toujours.","Une petite trousse prête : pansements, thermomètre, traitements en cours et leur ordonnance."),
("2026-12-18","maison","Maison","Un colis <em>livré abîmé</em> ?","Tout se joue à la réception.","Prends des photos du carton tout de suite et signale le problème au vendeur sans attendre."),
("2026-12-19","organisation","Organisation","La valise, <em>la veille au soir</em> ?","Et toujours un oubli.","Une liste de valise enregistrée dans ton téléphone. Tu la reprends à chaque départ."),
("2026-12-20","charge-mentale","Charge mentale","Noël parfait, <em>ou Noël serein</em> ?","Personne ne remarquera la nappe.","Raye une chose de ta liste aujourd'hui. Ce qui compte, c'est d'être là."),
("2026-12-21","papiers","Papiers","Ta carte cadeau, <em>valable jusqu'à quand</em> ?","Elle a une date de fin.","Photographie chaque carte cadeau avec sa date limite, dans un album « Cartes cadeaux »."),
("2026-12-22","budget","Budget","Un cadeau <em>en double</em> ?","Ça arrive à chaque Noël.","Garde le ticket cadeau avec le paquet, et échange-le vite, avant la date limite du magasin."),
("2026-12-23","ecole","École","Les devoirs de vacances, <em>quand</em> ?","Le dernier dimanche, comme toujours.","Fixe deux créneaux courts dans la semaine et note-les dans l'agenda familial."),
("2026-12-24","sante","Santé","Un souci <em>le soir du réveillon</em> ?","Ton médecin ne répond pas ce soir.","Note sur le frigo le 15 pour les urgences, et repère la pharmacie de garde avant d'en avoir besoin."),
("2026-12-25","maison","Joyeux Noël","Aujourd'hui, <em>ta tête est en congé.</em>","Les papiers attendront demain.","Profite de chaque minute. Kazaia garde tout en mémoire pour toi."),
("2026-12-26","organisation","Organisation","Les boîtes et les notices <em>à la poubelle</em> ?","Pas si vite.","Avant de jeter, garde la notice et la preuve d'achat de chaque appareil offert."),
("2026-12-27","charge-mentale","Charge mentale","Le bilan de l'année, <em>le tien</em> ?","Pas celui des papiers.","Écris trois choses que tu as réussies cette année. Rien d'autre."),
("2026-12-28","papiers","Papiers","Tes relevés de compte, <em>téléchargés</em> ?","Ils servent pour beaucoup de démarches.","Télécharge ceux de l'année depuis ton espace bancaire et range-les dans un dossier par année."),
("2026-12-29","budget","Budget","Le budget de janvier, <em>prêt</em> ?","Le mois le plus long de l'année.","Liste les prélèvements connus de janvier : assurances, impôts, abonnements. Le reste, tu le vois venir."),
("2026-12-30","ecole","École","La rentrée de janvier, <em>prête</em> ?","Lundi arrive vite.","Vérifie le cartable et le cahier de liaison dès aujourd'hui, pas dimanche soir."),
("2026-12-31","sante","Santé","Ta résolution santé, <em>une seule</em> ?","Pas une de plus.","Prends aujourd'hui le rendez-vous que tu repousses depuis des mois. C'est réglé avant minuit."),
]
tpl=open('tip-gabarit-noel.html').read()
for d,slug,theme,hook,sub,geste in T:
    h=tpl.replace("{THEME}",theme).replace("{HOOK}",fr(hook)).replace("{SUB}",fr(sub)).replace("{GESTE}",fr(geste))
    open(f"tip-{d}-{slug}.html","w").write(h)
json.dump(T,open('tips.json','w'),ensure_ascii=False,indent=0)
print(len(T))
