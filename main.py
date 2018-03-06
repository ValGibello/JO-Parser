### MODULE 1 - DOWNLOADING HTML ###

from lxml import html
import requests
import re
import datetime
import telegram_send

adresse_jo=["https://www.legifrance.gouv.fr/affichJO.do?idJO="]
jour = datetime.datetime.now()

print("Nous sommes le " + (jour.strftime("%d/%m/%Y")))

#from pprint import pprint

print("Connection à Légifrance" + "\n" + "Téléchargement du JO..." + "\n")

page = requests.get('https://www.legifrance.gouv.fr/affichJO.do?idJO=')
contenu = html.fromstring(page.content)

liens_sommaire = contenu.xpath('//a[@class="lienSommaire"]/text()')
### print(liens_sommaire)

nb_lignes = str(len(liens_sommaire))

print("Il y a " + nb_lignes + " entrées dans le JO du jour." + "\n")
print("Détection..." + "\n")

### MODULE 2 - PARSING ###

keywords = ['traitement', 'données']
keywords_re = re.compile("|".join(keywords))

nb_traitements = int()
contenu_utile = []

for item in liens_sommaire:
    if keywords_re.search(str(item)):
        nb_traitements += 1
        contenu_utile.append(item)
        print("Un traitement publié au JO." + "\n")
    

print("Il y a " + str(nb_traitements) + " entrée(s) intéressantes." + "\n" + "************************************************************" + "\n" + "\n")

### MODULE 3 - CREATING REPORT ###
print("************************************************************" + "\n" + "Génération d'un rapport..." + "\n" + "************************************************************" + "\n")


print(*contenu_utile, sep="\n \n")
telegram_send.send(["Bonjour ! Voici la sélection Journal Officiel du jour."])
telegram_send.send(messages=contenu_utile)
telegram_send.send(messages=adresse_jo, parse_mode="text")

