import re
N=" "
def fr(s):  # espaces fines insécables
    s=re.sub(r" ([?!:;»])", N+r"\1", s); s=re.sub(r"« ", "«"+N, s); return s
tips=[
 ("2026-11-17","budget","Budget","Ce prélèvement, tu sais encore <em>ce que c'est</em> ?","Les abonnements oubliés coûtent sans bruit.","Le 1er du mois, surligne chaque prélèvement de ton relevé. Celui que tu ne reconnais pas : tu vérifies, tu résilies."),
 ("2026-11-18","ecole","Enfants et école","L'assurance scolaire, tu l'as <em>sous la main</em> ?","On te la demande toujours au pire moment.","Dès que tu la reçois, prends-la en photo et range-la dans un album « École »."),
 ("2026-11-19","sante","Santé","Le prochain rappel de vaccin, <em>c'est quand</em> ?","Personne ne s'en souvient. Et c'est normal.","Le jour du vaccin, note tout de suite la date du rappel dans ton agenda. Dix secondes, c'est réglé."),
 ("2026-11-20","contrats","Contrats","Ta box se réengage <span class=\"nw\">peut-être</span> <em>sans toi</em>.","La date qui compte, c'est l'échéance.","Note la date d'échéance de chaque contrat : box, assurance, énergie. C'est souvent elle qui décide quand tu peux changer."),
 ("2026-11-21","organisation","Organisation","Des papiers qui traînent <em>partout</em> ?","Un seul endroit, une fois par semaine.","Une boîte « à traiter » : chaque papier y entre. Le samedi matin, tu la vides en un quart d'heure."),
 ("2026-11-22","charge-mentale","Charge mentale","Ta tête tourne encore <em>à 23 h</em> ?","Elle a juste peur d'oublier.","Avant de dormir, écris sur une feuille tout ce qui t'occupe. Ta tête peut lâcher : c'est noté."),
 ("2026-11-23","papiers","Papiers","Ta fiche de paie de 2012, <em>tu l'as jetée</em> ?","Elle te le dit elle-même : <span class=\"nw\">à garder</span> sans limite de durée.","Un dossier <span class=\"nw\">« Fiches de paie »</span>, et chaque mois la nouvelle y entre. Tu n'en jettes aucune, jamais."),
]
tpl=open('semaines/2026-11-16/tip-gabarit.html').read()
for d,slug,theme,hook,sub,geste in tips:
    h=tpl.replace("{THEME}",theme).replace("{HOOK}",fr(hook)).replace("{SUB}",fr(sub)).replace("{GESTE}",fr(geste))
    open(f"semaines/2026-11-16/tip-{d}-{slug}.html","w").write(h)
    print(f"semaines/2026-11-16/tip-{d}-{slug}.html")
