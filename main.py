### MODULE 1 - DOWNLOADING HTML ###

from lxml import html
import requests

print("Téléchargement...")

page = requests.get('https://www.legifrance.gouv.fr/affichJO.do?idJO=')
contenu = html.fromstring(page.content)

lien_sommaire = contenu.xpath('//a[@class="lienSommaire"]/text()')
### print(lien_sommaire)

nb_lignes = str(len(lien_sommaire))

print("Il y a " + nb_lignes + " entrées dans le JO du jour.")
print("Détection...")

### MODULE 2 - PARSING ###

keywords = ['traitement', 'données']
nb_traitements = 0

for each in lien_sommaire:
    if keywords in lien_sommaire:
        nb_traitements += 1
        print("Un traitement publié au JO.")
    else:
        print("Pas de traitement.")

### MODULE 3 - CREATING REPORT ###