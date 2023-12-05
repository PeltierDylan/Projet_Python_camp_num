"""
Application d'Audit de Sites Web avec Tkinter

Cette application est conçue pour permettre aux utilisateurs d'effectuer un audit SEO basique sur des sites web. 
Elle utilise Tkinter pour une interface utilisateur graphique, permettant une interaction facile et intuitive. 
Les utilisateurs peuvent entrer une URL et des mots-clés SEO pour obtenir un rapport détaillé sur différents aspects 
de l'URL spécifiée, tels que les liens internes/externes, l'utilisation de mots-clés, et le pourcentage d'images 
avec des attributs alt. L'application offre également la possibilité de sauvegarder le rapport généré et de mettre à jour 
une liste de mots parasites pour affiner l'analyse SEO.

Caractéristiques Principales:
- Entrée d'URL et de mots-clés pour l'audit.
- Extraction et analyse de contenu HTML d'une page web.
- Affichage des détails de l'audit incluant les liens internes/externes, le pourcentage d'images avec attribut alt, et les mots-clés.
- Fonctionnalité pour sauvegarder le rapport d'audit.
- Interface pour mettre à jour une liste de mots parasites.

Modules Externes Requis:
- tkinter : Pour l'interface utilisateur graphique.
- projet : Contient les classes personnalisées UrlAudit, HtmlAnalyser, et TextAnalyser pour diverses analyses.

Utilisation:
Exécuter ce script lancera l'application avec Tkinter. L'utilisateur peut interagir avec l'interface graphique pour entrer des données et recevoir des rapports.
"""
#######################################################################################
# Import Standard
import os
#######################################################################################
# Import Spécifique
from projet import UrlAudit, HtmlAnalyser, TextAnalyser
import tkinter as tk
from tkinter import filedialog, messagebox
#######################################################################################


class App:
    """
    Une application Tkinter pour l'audit de sites web. 
    Permet à l'utilisateur d'entrer une URL et des mots-clés SEO, 
    et affiche un rapport détaillé de l'audit après analyse.
    """
    def __init__(self, master):
        """
        Initialise l'application avec une interface utilisateur 
        comprenant des entrées pour l'URL et les mots-clés, 
        ainsi que des boutons pour lancer l'analyse et sauvegarder les rapports.
        
        :param master: Le widget parent dans lequel cette application est intégrée.
        """
        self.master = master
        master.title("Audit Websites")
        self.menu_bar = tk.Menu(master)
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Mots parasites", command=self.update_badwords)
        self.menu_bar.add_cascade(label="Fichier", menu=file_menu)
        self.master.config(menu=self.menu_bar)
        self.label_url = tk.Label(master, text="Entrer l'URL à auditer :")
        self.entry_url = tk.Entry(master)
        self.label_keywords = tk.Label(master, text="Entrer les mots-clés souhaiter pour le SEO :")
        self.entry_keywords = tk.Entry(master)
        self.analyse_btn = tk.Button(master, text="Analyser", command=self.analyse)
        self.label_url.pack()
        self.entry_url.pack()
        self.label_keywords.pack()
        self.entry_keywords.pack()
        self.analyse_btn.pack()
        self.second_frame = tk.Frame(master)
        self.details_label = tk.Label(self.second_frame, text="Détails de l'audit :")
        self.details_text = tk.Text(self.second_frame)
        self.details_label.pack()
        self.details_text.pack(fill=tk.BOTH, expand=True)
        self.save_btn = tk.Button(self.second_frame, text="Sauvegarder", command=self.save)
        self.save_btn.pack(side=tk.RIGHT, padx=10)


    def analyse(self):
        """
        Lance l'analyse de l'URL saisie par l'utilisateur. 
        Récupère le HTML de l'URL, extrait les liens internes et externes, 
        et affiche des détails comme le pourcentage d'images avec un attribut alt, 
        et la présence de mots-clés définis par l'utilisateur.
        """
        try:
            self.details_text.delete("1.0", tk.END)
        except:
            pass
        url = self.entry_url.get()
        user_keywords = set(self.entry_keywords.get().lower().split(','))
        try:
            html_main = UrlAudit.recuperer_html(url)
        except Exception as e:
            messagebox.showerror(f"Erreur", "Impossible de se connecter à la page demandée {url} \n Erreur :{e}")
            return
        domain = UrlAudit.extraire_nom_domaine(url)
        links_main = HtmlAnalyser.extraire_attributs(html_main, 'a', 'href')
        internal_links, external_links = UrlAudit.classifier_par_domaine(domain, links_main)
        badwords = TextAnalyser.recuperer_parasites("parasites.csv")
        for link in internal_links:
            try:
                html = UrlAudit.recuperer_html(link)
            except Exception as e:
                print(f"Impossible de se connecter à la page {e}")
                continue
            html_cleaned = HtmlAnalyser.nettoyer_html(html)
            occurrences = TextAnalyser.compter_occurrences(html_cleaned)
            found_keywords = TextAnalyser.retirer_parasites(occurrences, badwords)
            self.affichage_details(url=link, user_keywords=user_keywords, keywords=found_keywords, html=html)
        self.second_frame.pack(fill=tk.BOTH, expand=True)


    def affichage_details(self, url, user_keywords, keywords, html):
        """
        Affiche les détails de l'audit pour une URL spécifique.

        Args:
            url (str): L'URL de la page analysée.
            user_keywords (list): Ensemble de mots-clés fournis par l'utilisateur.
            keywords (list): Mots-clés trouvés dans la page.
            html (str): Le contenu HTML de la page.
        """
        percent_alt_img = HtmlAnalyser.percent_attributs(html, 'img', 'alt')
        links = HtmlAnalyser.extraire_attributs(html, 'a', 'href')
        sub_internal_links, sub_external_links = UrlAudit.classifier_par_domaine(url, links)
        nb_internal_links = len(sub_internal_links)
        nb_external_links = len(sub_external_links)
        three_first_keywords = list(keywords.keys())[:3]
        user_keywords_in_page = any([word in three_first_keywords for word in user_keywords])
        details = (
            f"Détails pour l'URL : {url}\n"
            f"Nombre de liens internes : {nb_internal_links}\n"
            f"Nombre de liens externes : {nb_external_links}\n"
            f"Pourcentage d'images avec attribut alt : {percent_alt_img} %\n"
            f"Les 3 premiers mots-clés : {', '.join(three_first_keywords)}\n"
            f"Présence de mots-clés : {'Oui' if user_keywords_in_page else 'Non'}\n"
            )
        self.details_text.insert(tk.END, details + "\n\n")


    def save(self):
        """
        Sauvegarde le rapport d'audit dans un fichier texte. 
        Permet à l'utilisateur de choisir l'emplacement et le nom du fichier.
        """
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text file", ".txt"), ("All Files", ".*")],
            initialdir=os.getcwd(),
            title="Sauvegarder le rapport d'audit"
        )

        if not filename:
            return
        with open(filename, 'w') as file:
            report_content = self.details_text.get("1.0", tk.END)
            file.write(report_content)
        messagebox.showinfo("Sauvegarde", "Le rapport a été sauvegardé avec succès !")


    def update_badwords(self):
        """
        Permet à l'utilisateur de mettre à jour la liste des mots parasites. 
        Ouvre une nouvelle fenêtre pour éditer et sauvegarder la liste mise à jour.
        """
        edit_window = tk.Toplevel(self.master)
        edit_window.title("Mise à jour des Mots parasites")
        try:
            with open("parasites.csv", 'r') as f:
                current_badwords = f.read().splitlines()
        except FileNotFoundError:
            messagebox.showerror("Erreur", "Le fichier parasites.csv est introuvable")
            return
        edit_text = tk.Text(edit_window, height=10, width=50)
        edit_text.pack(padx=10, pady=10)
        for word in current_badwords:
            edit_text.insert(tk.END, word + "\n")
        save_button = tk.Button(edit_window, text="Sauvegarder", command=lambda: self.save_badwords(edit_text, edit_window))
        save_button.pack(pady=10)


    def save_badwords(self, edit_text, edit_window):
        """
        Sauvegarde la liste mise à jour des mots parasites dans un fichier.

        :param edit_text: Le widget Text contenant la liste mise à jour.
        :param edit_window: La fenêtre d'édition où la liste est modifiée.
        """
        updated_badwords = edit_text.get("1.0", tk.END).strip().split("\n")
        with open("parasites.csv", 'w') as f:
            for word in updated_badwords:
                f.write(word + "\n")
        edit_window.destroy()
        messagebox.showinfo("Sauvegarde", "Les mots parasites ont été sauvegardés avec succès !")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
