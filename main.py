from lxml import html
import requests

page = requests.get('https://www.legifrance.gouv.fr/affichJO.do?idJO=')
contenu = html.fromstring(page.content)

lien_sommaire = contenu.xpath('//a[@class="lienSommaire"]/text()')
print(lien_sommaire)