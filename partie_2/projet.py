"""
Ce script fournit des outils pour l'analyse de contenu web, notamment le comptage d'occurrences de mots,
le nettoyage de texte HTML, l'extraction d'attributs de balises, et l'audit de pages web.

Le script se compose de plusieurs étapes :
1. Comptage d'occurrences de mots dans un texte.
2. Retrait de mots parasites d'un dictionnaire d'occurrences.
3. Récupération de mots parasites à partir d'un fichier CSV.
4. Test de l'étape 4 (comptage d'occurrences et nettoyage des mots parasites).
5. Nettoyage de code HTML pour en extraire le texte.
6. Extraction d'attributs spécifiques de balises HTML.
7. Test de l'étape 7 (nettoyage HTML et extraction d'attributs).
8. Extraction du nom de domaine d'une URL.
9. Classification des URLs en internes et externes.
10. Récupération du code HTML d'une page web.
11. Audit de contenu d'une page web.
"""
# -*- coding:utf-8 -*-
###################################################################
# IMPORTS STANDARDS
from collections import Counter
import csv
import re
import requests
from urllib.parse import urlparse
###################################################################
###################################################################
# IMPORT SPECIFIQUE
from bs4 import BeautifulSoup
###################################################################

class TextAnalyser:
    @staticmethod
    def compter_occurrences(texte):
        """
        Compte les occurrences de chaque mot dans un texte.

        Args:
            texte (str): Le texte à analyser.

        Returns:
            dict: Un dictionnaire où les clés sont des mots et les valeurs sont le nombre d'occurrences de chaque mot.
        """
        mots = re.findall(r'\b\w+\b', texte.lower())
        occurrences = Counter(mots)
        return dict(sorted(occurrences.items(), key=lambda item: item[1], reverse=True))


    @staticmethod
    def retirer_parasites(occurrences, parasites):
        """
        Retire les mots parasites d'un dictionnaire d'occurrences.

        Args:
            occurrences (dict): Un dictionnaire d'occurrences de mots.
            parasites (set): Un ensemble de mots à exclure.

        Returns:
            dict: Un dictionnaire d'occurrences nettoyé des mots parasites.
        """
        return {mot: occurrences[mot] for mot in occurrences if mot.lower() not in parasites}


    @staticmethod
    def recuperer_parasites(fichier):
        """
        Récupère une liste de mots parasites à partir d'un fichier CSV.

        Args:
            fichier (str): Le chemin du fichier CSV contenant les mots parasites.

        Returns:
            set: Un ensemble de mots parasites.
        """
        with open(fichier, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            mots_parasites = {row[0].lower() for row in reader}
        return mots_parasites

class HtmlAnalyser:
    @staticmethod
    def nettoyer_html(html):
        """
        Nettoie le HTML pour ne conserver que le texte visible.

        Args:
            html (str): Le code HTML à nettoyer.

        Returns:
            str: Le texte nettoyé extrait du HTML.
        """
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text()

    @staticmethod
    def extraire_attributs(html, balise, attribut):
        """
        Extrait les valeurs d'un attribut spécifique de toutes les balises d'un type donné dans un HTML.

        Args:
            html (str): Le code HTML à analyser.
            balise (str): Le type de balise HTML à rechercher.
            attribut (str): L'attribut dont la valeur doit être extraite.

        Returns:
            list: Une liste des valeurs de l'attribut pour chaque balise trouvée.
        """
        soup = BeautifulSoup(html, "html.parser")
        return [tag[attribut] for tag in soup.find_all(balise) if tag.has_attr(attribut)]

    @staticmethod
    def percent_attributs(html, balise, attribut):
        """
        Calcule le pourcentage d'occurrence d'un attribut spécifique de toutes les balises d'un type donné dans un HTML.

        Args:
            html (str): Le code HTML à analyser.
            balise (str): Le type de balise HTML à rechercher.
            attribut (str): L'attribut dont la valeur doit être extraite.

        Returns:
            float: Le pourcentage d'occurrence de l'attribut.
        """
        soup = BeautifulSoup(html, "html.parser")
        all_balises = len(soup.find_all(balise))
        if all_balises == 0:
            return 0
        balises_with_attributs = len([tag[attribut] for tag in soup.find_all(balise) if tag.has_attr(attribut)])
        return int(balises_with_attributs) / int(all_balises) * 100

class UrlAudit:
    @staticmethod
    def extraire_nom_domaine(url):
        """
        Extrait le nom de domaine d'une URL.

        Args:
            url (str): L'URL dont le nom de domaine doit être extrait.

        Returns:
            str: Le nom de domaine de l'URL.
        """
        return urlparse(url).netloc


    @staticmethod
    def classifier_par_domaine(domaine, urls):
        """
        Classifie les URLs en internes et externes par rapport à un domaine donné.

        Args:
            domaine (str): Le nom de domaine de référence.
            urls (list): Une liste d'URLs à classifier.

        Returns:
            tuple: Deux listes, la première contenant les URLs internes et la deuxième les URLs externes.
        """
        internes, externes = [], []
        for url in urls:
            if domaine in url:
                internes.append(url)
            else:
                externes.append(url)
        return internes, externes


    @staticmethod
    def recuperer_html(url):
        """
        Récupère le code HTML d'une page web à partir de son URL.

        Args:
            url (str): L'URL de la page web.

        Returns:
            str: Le code HTML de la page.
        """
        response = requests.get(url, timeout=5)
        return response.text


    def audit_page(self, url):
        """
        Réalise un audit de contenu d'une page web à partir de son URL.

        Args:
            url (str): L'URL de la page web à analyser.

        Affiche:
            Les résultats de l'analyse, y compris les mots clés, les liens entrants et sortants, et les balises alt des images.
        """
        html = self.recuperer_html(url)
        texte = HtmlAnalyser.nettoyer_html(html)
        occurrences = TextAnalyser.compter_occurrences(texte)
        mots_parasites = TextAnalyser.recuperer_parasites("parasites.csv")
        mots_cles = TextAnalyser.retirer_parasites(occurrences, mots_parasites)
        
        print("Mots clés avec les 3 premières valeurs d'occurrences :")
        for mot, occ in list(mots_cles.items())[:3]:
            print(f"{mot}: {occ}")
        
        liens = extraire_attributs(html, 'a', 'href')
        liens_entrants, liens_sortants = self.classifier_par_domaine(extraire_nom_domaine(url), liens)
        
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