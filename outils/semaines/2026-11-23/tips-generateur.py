import re
N="\u202f"
def fr(s):  # espaces fines insécables
    s=re.sub(r" ([?!:;»])", N+r"\1", s); s=re.sub(r"« ", "«"+N, s); return s
tips=[
 ("2026-11-24","budget","Budget","Un achat en ligne <em>regretté</em> ?","En général, tu as <span class=\"nw\">14 jours</span> pour changer d'avis.","Le jour où le colis arrive, note la date. Les 14 jours partent du lendemain, sans avoir à te justifier."),
 ("2026-11-25","ecole","École","Le mot à signer, <em>retrouvé froissé</em> ?","Au fond du cartable. Comme toujours.","Une pochette transparente « À signer » dans le cartable. Chaque soir, tu l'ouvres. Rien d'autre à chercher."),
 ("2026-11-26","sante","Santé","Ton ordonnance, <em>tu la retrouves</em> ?","Jamais le jour où il faut la renouveler.","Avant de la tendre au comptoir, prends-la en photo. Elle file dans un album « Santé »."),
 ("2026-11-27","maison","Maison","Un dégât des eaux. <em>Et ta preuve</em> ?","Prouver ce que tu avais, c'est le plus dur.","Filme chaque pièce, placards ouverts. Garde la vidéo avec ton contrat d'assurance habitation."),
 ("2026-11-28","organisation","Organisation","Trois agendas, <em>zéro vue d'ensemble</em> ?","Le conflit de <span class=\"nw\">rendez-vous</span> se voit trop tard.","Un seul agenda partagé pour toute la famille. Chaque <span class=\"nw\">rendez-vous</span> y entre dès qu'il est fixé."),
 ("2026-11-29","charge-mentale","Charge mentale","« Dis-moi si <em>je peux t'aider.</em> »","Le vrai poids, c'est d'y penser.","Confie une tâche entière : y penser, la faire, la suivre. Les <span class=\"nw\">rendez-vous</span> chez le dentiste ? C'est l'autre, du début à la fin."),
 ("2026-11-30","papiers","Papiers","Tes factures d'énergie, <em>tu les gardes</em> ?","Électricité et gaz : <span class=\"nw\">5 ans.</span>","Un dossier « Énergie » : chaque facture y entre. Au-delà de <span class=\"nw\">5 ans</span>, tu peux trier."),
]
tpl=open('semaines/2026-11-23/tip-gabarit.html').read()
for d,slug,theme,hook,sub,geste in tips:
    h=tpl.replace("{THEME}",theme).replace("{HOOK}",fr(hook)).replace("{SUB}",fr(sub)).replace("{GESTE}",fr(geste))
    open(f"semaines/2026-11-23/tip-{d}-{slug}.html","w").write(h)
    print(f"semaines/2026-11-23/tip-{d}-{slug}.html")
