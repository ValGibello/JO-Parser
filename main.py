from lxml import html
import requests
import re
import datetime
import telegram_send

### Récupération du JO ###

adresse_jo=["https://www.legifrance.gouv.fr/affichJO.do?idJO="]
jour = datetime.datetime.now()

print("Nous sommes le " + (jour.strftime("%d/%m/%Y")))

print("Connection à Légifrance" + "\n" + "Téléchargement du JO..." + "\n")

page = requests.get('https://www.legifrance.gouv.fr/affichJO.do?idJO=')
contenu = html.fromstring(page.content)
liens_sommaire = contenu.xpath('//a[@class="lienSommaire"]/text()')

nb_entrées = str(len(liens_sommaire))

print("Il y a " + nb_entrées + " entrées dans le JO du jour." + "\n")
print("Détection..." + "\n")

### PARSING ###

nb_traitements = int()
contenu_utile = []

keywords = ["création d'un traitement", "données"]
keywords_re = re.compile("|".join(keywords))

for item in liens_sommaire:
    if keywords_re.search(str(item)):
        nb_traitements += 1
        contenu_utile.append(item)
        print("Un traitement intéressant publié au JO." + "\n")
    
### GENERATION D'UN RAPPORT ET DIFFUSION ###

if len(contenu_utile)>0:
    print("Il y a " + str(nb_traitements) + " entrée(s) intéressante(s)." + "\n" + "************************************************************" + "\n" + "\n")
    print("************************************************************" + "\n" + "Génération d'un rapport..." + "\n" + "************************************************************" + "\n")
    print(*contenu_utile, sep="\n \n")
    telegram_send.send(["Bonjour ! Voici la sélection Journal Officiel du jour."])
    telegram_send.send(messages=contenu_utile)
    telegram_send.send(messages=adresse_jo, parse_mode="text")
else:
    print("Aucun traitement intéressant publié au JO. Essayez de modifier les règles de tri.")


