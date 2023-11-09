from collections import Counter
import re
from collections import Counter
import csv
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

# etape 1
def compter_occurrences(texte):
    mots = re.findall(r'\b\w+\b', texte.lower())
    occurrences = Counter(mots)
    return dict(sorted(occurrences.items(), key=lambda item: item[1], reverse=True))

# Etape 2
def retirer_parasites(occurrences, parasites):
    return {mot: occurrences[mot] for mot in occurrences if mot.lower() not in parasites}


# etape 3
def recuperer_parasites(fichier):
    with open(fichier, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        mots_parasites = {row[0].lower() for row in reader}
    return mots_parasites

# etape 4
def test_etape4():
    print("Test de l'étape 4 :");print("******************")
    texte = "La brise d'automne disperse les feuilles colorées. Un écureuil agile saute entre les branches. Loin, une cloche d'église résonne, rythmant le crépuscule naissant. Les pensées s'évadent, légères, au gré du vent frais, tandis que le monde s'habille de nuances orangées, annonçant la nuit étoilée."
    mots_occurrences = compter_occurrences(texte)
    parasites = recuperer_parasites('parasites.csv')
    resultat = retirer_parasites(mots_occurrences, parasites)
    print("Occurences des mots : ", end='');print(mots_occurrences)
    print("Occurences des mots sans parasites : ", end="");print(resultat)

# Etape 5
def nettoyer_html(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()

# etape 6
def extraire_attributs(html, balise, attribut):
    soup = BeautifulSoup(html, "html.parser")
    return [tag[attribut] for tag in soup.find_all(balise) if tag.has_attr(attribut)]

# Etape 7
def test_etape7():
    print("Test de l'étape 7 :");print("******************")
    html_exemple = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Exemple de Page HTML</title>
    </head>
    <body>
        <h1>Bienvenue sur ma page web</h1>
        <p>Ceci est un paragraphe de texte simple.</p>
        <a href="https://www.exemple.com" alt="Lien exemple">Visitez notre site web</a>
        <ul>
            <li>Liste item 1</li>
            <li>Liste item 2</li>
            <li>Liste item 3</li>
        </ul>
        <img src="image.jpg" alt="Image descriptive" />
        <p>Encore un peu de texte avec des <strong>mots en gras</strong> et des <em>mots en italique</em>.</p>
    </body>
    </html>
    """

    # Nettoyage du HTML
    html_cleaned = nettoyer_html(html_exemple)
    print("HTML nettoyé :")
    print(html_cleaned)

    # Extraction des attributs 'alt' des balises 'img'
    alt_values = extraire_attributs(html_exemple, 'img', 'alt')
    print("Valeurs de l'attribut 'alt' :")
    print(alt_values)

    # Extraction des attributs 'href' des balises 'a'
    href_values = extraire_attributs(html_exemple, 'a', 'href')
    print("\nValeurs de l'attribut 'href' :")
    print(href_values)

#Etape 8
def extraire_nom_domaine(url):
    return urlparse(url).netloc

# Etape 9
def classifier_par_domaine(domaine, urls):
    internes, externes = [], []
    for url in urls:
        if domaine in url:
            internes.append(url)
        else:
            externes.append(url)
    return internes, externes

# Etape 10
def recuperer_html(url):
    response = requests.get(url)
    return response.text

# Etape 11
def audit_page(url):
    html = recuperer_html(url)
    texte = nettoyer_html(html)
    occurrences = compter_occurrences(texte)
    mots_parasites = recuperer_parasites("parasites.csv")
    mots_cles = retirer_parasites(occurrences, mots_parasites)
    
    print("Mots clés avec les 3 premières valeurs d'occurrences :")
    for mot, occ in list(mots_cles.items())[:3]:
        print(f"{mot}: {occ}")
    
    liens = extraire_attributs(html, 'a', 'href')
    liens_entrants = [lien for lien in liens if lien.startswith(url)]
    liens_sortants = [lien for lien in liens if not lien.startswith(url)]
    
    print(f"Nombre de liens entrants: {len(liens_entrants)}")
    print(f"Nombre de liens sortants: {len(liens_sortants)}")
    
    alts = extraire_attributs(html, 'img', 'alt')
    print(f"Présence de balises alt: {alts if alts else 'Non'}")

# Exemple d'utilisation
if __name__ == "__main__":
    test_etape4()
    test_etape7()
    url_demandee = input("Entrez l'URL de la page à analyser : ")
    audit_page(url_demandee)