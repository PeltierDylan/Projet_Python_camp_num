**Vous créerez un repo Git sur lequel vous placerez votre projet, vous n'aurez plus qu'à me soumettre le lien du git.**

---

**L'optimisation pour les moteurs de recherche**, aussi connue sous le sigle **SEO**, inclut l'ensemble des techniques qui visent à améliorer le positionnement d'une page, d'un site ou d'une application web dans la page de résultats d'un moteur de recherche.

---

Certains critères comptent pour le bon référencement d’un site internet. Nous allons en retenir quelques-uns à savoir :

- **Les mots clefs** présents pour chaque page du site
- **La présence de balises alt** pour les images
- **Le nombre de liens entrants et sortants**

Vous allez réaliser un auditeur de référencement SEO pour sites internet à l’aide de fonctions simples.

---

**Etape 1 :** Créer une fonction qui prend en paramètre un texte et qui retourne une liste/dictionnaires de l’ensemble des mots présents dans le texte avec leur occurrence, cette liste sera classée par nombres d’occurrences.

**Etape 2 :** Créer une fonction qui prend en paramètre la structure de données précédentes, ainsi qu’une liste de mots parasites et qui retourne la structure de données privées des mots de la liste parasite.

_Le but étant d’enlever les mots parasites comme le, la, les…_

**Etape 3 :** Créer une fonction qui récupère les mots parasite dans un fichier `parasite.csv` et retourne une liste de ces mots.

**Etape 4 :** Testez votre code. Vous devrez pouvoir soumettre une chaine de caractères assez longue. Appelez la fonction de l’étape 1, puis utilisez la fonction de l’étape 3 puis appelez la fonction de l’étape 2 pour obtenir les mots clefs les plus importants de cette page.

**Etape 5 :** Créez une fonction qui prend en paramètre une chaine de caractère au format html et renvoie le même texte mais sans les balises html, vous pouvez utiliser BeautifulSoup.

**Etape 6 :** Ecrire une fonction qui prend en paramètre une chaine de caractère, le nom d’une balise, le nom d’un attribut et retourne la liste des valeurs associées aux balises.

**Etape 7 :** Testez cette fonction pour récupérer dans un code html toutes les valeurs des attributs `alt` des balises `img`. Testez cette fonction pour récupérer tous les `href` des balises `a`.

**Etape 8 :** Créer une fonction qui prend en paramètre une URL et qui extrait le nom de domaine.

**Etape 9 :** Créer une fonction prenant en paramètre une chaine de caractère représentant un nom de domaine, et une liste de valeurs qui sont des URL et qui retourne deux listes avec les URL qui font partie du domaine et ceux qui n’en font pas partie.

**Etape 10 :** Créer une fonction qui ouvre une page html depuis une URL et récupère le texte HTML qui la compose.

**Etape 11 :** Ecrire le programme qui fait l’audit de votre première page.

Elle demandera l’URL de la page à analyser puis elle affichera les mots clefs avec les 3 premières valeurs d’occurrences, le nombre de liens entrants et le nombre de liens sortant et la présence de balises alt.

---
