from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QColor
from Creation_Onglets import Onglets
from Creation_Camembert import Camembert
from Creation_Legendes import Legendes
from Creation_Boutons import Boutons
import json
import sys
import random
import platform

# Constantes
NB_LEGENDES_PAR_PAGE = 25
NOM_FICHIER_JSON = "gros_fichiers.json"
NOM_SCRIPT_SUPPRESSION = "Suppression_Fichiers.ps1"


def lire_fichier_json(nom_fichier):
    """
    Lit le fichier JSON contenant la liste des gros fichiers.
    Retourne la liste de listes : [[chemin, taille], ...]
    """
    with open(nom_fichier, 'r', encoding='utf-8') as f:
        liste_fichiers = json.load(f)

    # Remplacement des double antislashs par des antislashs simples
    for fichier in liste_fichiers:
        fichier[0] = fichier[0].replace('\\\\', '\\')

    return liste_fichiers


def generer_couleurs_aleatoires(nb_couleurs):
    """
    Génère une liste de couleurs aléatoires au format QColor.
    Retourne la liste de couleurs.
    """
    liste_couleurs = []

    for i in range(nb_couleurs):
        # Génération de valeurs RGB aléatoires
        rouge = random.randint(0, 255)
        vert = random.randint(0, 255)
        bleu = random.randint(0, 255)

        # Création de l'objet QColor
        couleur = QColor(rouge, vert, bleu)
        liste_couleurs.append(couleur)

    return liste_couleurs


def creation_script_suppression():
    """
    Fonction callback appelée lors du clic sur le bouton.
    Génère le script PowerShell de suppression des fichiers cochés.
    """
    # Liste pour stocker tous les fichiers à supprimer
    fichiers_a_supprimer = []

    # Parcours de toutes les pages de légendes
    for page_legende in liste_legendes:
        # Récupération des états des cases à cocher
        etats = page_legende.recupere_etats_cases_a_cocher()

        # Récupération de l'index de départ de cette page
        index_depart = page_legende.num_legende_start

        # Parcours des cases à cocher
        for i, est_coche in enumerate(etats):
            if est_coche:
                # Ajout du fichier à la liste
                index_fichier = index_depart + i
                fichiers_a_supprimer.append(liste_fichiers[index_fichier][0])

    # Vérification qu'au moins un fichier est sélectionné
    if len(fichiers_a_supprimer) == 0:
        print("Aucun fichier sélectionné.")
        return

    # Détection du système d'exploitation
    systeme = platform.system()

    # Génération du script PowerShell
    with open(NOM_SCRIPT_SUPPRESSION, 'w', encoding='utf-8') as f:
        # En-tête du script
        f.write('Write-Output "Script PowerShell pour supprimer des fichiers sans confirmation"\n')
        f.write('Write-Output "Attention : cette suppression est définitivement ..."\n')
        f.write('$reponse = Read-Host "Veuillez confirmer la suppression de tous ces fichiers : (OUI)"\n')
        f.write('if ($reponse -eq "OUI") {\n')
        f.write('    $confirmation = Read-Host "Etes-vous bien certain(e) ? (OUI)"\n')
        f.write('    if ($confirmation -eq "OUI") {\n')

        # Ajout des commandes de suppression
        for fichier in fichiers_a_supprimer:
            # Remplacement des antislashs par des slashs pour compatibilité multiplateforme
            if systeme == "Windows":
                chemin_fichier = fichier
            else:
                # Sur MacOS/Linux, conversion des chemins Windows si nécessaire
                chemin_fichier = fichier.replace('\\', '/')

            f.write(f'        Remove-Item -Path "{chemin_fichier}" -Force\n')

        # Fin du script
        f.write('    } else {\n')
        f.write('        Write-Output "Opération annulée..."\n')
        f.write('    }\n')
        f.write('} else {\n')
        f.write('    Write-Output "Opération annulée..."\n')
        f.write('}\n')

    print(f"Script '{NOM_SCRIPT_SUPPRESSION}' créé avec succès !")
    print(f"  -> {len(fichiers_a_supprimer)} fichier(s) seront supprimés si vous exécutez ce script.")


if __name__ == "__main__":
    # Vérification de la présence d'un argument (répertoire de base)
    if len(sys.argv) < 2:
        print("Erreur : Aucun répertoire spécifié.")
        print("Usage : python Affichage_Resultats.py <repertoire_de_base>")
        sys.exit(1)

    # Récupération du répertoire de base
    repertoire_base = sys.argv[1]

    # Lecture du fichier JSON
    print(f"Lecture du fichier '{NOM_FICHIER_JSON}'...")
    liste_fichiers = lire_fichier_json(NOM_FICHIER_JSON)
    print(f"  -> {len(liste_fichiers)} fichiers chargés")

    # Génération des couleurs aléatoires
    liste_couleurs = generer_couleurs_aleatoires(len(liste_fichiers))

    # Création de l'application Qt
    appli = QApplication(sys.argv)

    # Création de la fenêtre avec onglets
    fenetre = Onglets()

    # Création et ajout du camembert
    fromage = Camembert(liste_fichiers, liste_couleurs)
    layout_fromage = fromage.dessine_camembert()
    fenetre.add_onglet("Camembert", layout_fromage)

    # Création et ajout des pages de légendes
    liste_legendes = []
    nb_pages_legendes = (len(liste_fichiers) + NB_LEGENDES_PAR_PAGE - 1) // NB_LEGENDES_PAR_PAGE

    for num_page_leg in range(nb_pages_legendes):
        # Création d'une page de légendes
        page_legende = Legendes(
            liste_fichiers,
            liste_couleurs,
            NB_LEGENDES_PAR_PAGE * num_page_leg,
            NB_LEGENDES_PAR_PAGE
        )
        liste_legendes.append(page_legende)

        # Construction du layout et ajout à l'onglet
        layout_legende = page_legende.dessine_legendes()
        fenetre.add_onglet(f"Légende {num_page_leg + 1}", layout_legende)

    # Création et ajout de l'onglet IHM avec le bouton
    ihm = Boutons(repertoire_base, creation_script_suppression)
    layout_ihm = ihm.dessine_boutons()
    fenetre.add_onglet("IHM", layout_ihm)

    # Affichage de la fenêtre
    fenetre.show()
    print("Interface graphique affichée.")

    # Lancement de l'application
    sys.exit(appli.exec_())