import sys
import json
import platform
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QColor

from Creation_Onglets import Onglets
from Creation_Camembert import Camembert
from Creation_Legendes import Legendes
from Creation_Boutons import Boutons

NB_LEGENDES_PAR_PAGE = 25


def charger_json(nom_fichier="resultats.json"):
    with open(nom_fichier, 'r', encoding='utf-8') as f:
        liste_fichiers = json.load(f)

    for fichier in liste_fichiers:
        fichier[0] = fichier[0].replace('\\\\', '\\')

    return liste_fichiers


def generer_couleurs_aleatoires(nb_couleurs=100):
    import random
    liste_couleurs = []
    for i in range(nb_couleurs):
        rouge = random.randint(0, 255)
        vert = random.randint(0, 255)
        bleu = random.randint(0, 255)
        couleur = QColor(rouge, vert, bleu)
        liste_couleurs.append(couleur)
    return liste_couleurs


def creation_script_suppression():
    global liste_legende, liste_fichiers, repertoire_base

    fichiers_a_supprimer = []

    for page in liste_legende:
        etats_cases = page.recupere_etats_case_a_cocher()
        index_debut = page.num_legende_start

        for i, est_coche in enumerate(etats_cases):
            if est_coche:
                index_fichier = index_debut + i
                chemin_fichier = liste_fichiers[index_fichier][0]
                fichiers_a_supprimer.append(chemin_fichier)

    if not fichiers_a_supprimer:
        print("Aucun fichier sélectionné")
        return

    systeme = platform.system()
    nom_script = "Supprimer_Fichiers.ps1"

    contenu = 'Write-Output "Script PowerShell pour supprimer des fichiers sans confirmation"\n'
    contenu += 'Write-Output "Attention : cette suppression est définitive..."\n'
    contenu += '$reponse = Read-Host "Veuillez confirmer la suppression de tous ces fichiers : (OUI)"\n'
    contenu += 'if ($reponse -eq "OUI") {\n'
    contenu += '    $confirmation = Read-Host "Etes-vous bien certain(e) ? (OUI)"\n'
    contenu += '    if ($confirmation -eq "OUI") {\n'

    for chemin in fichiers_a_supprimer:
        chemin_path = Path(chemin)
        if systeme == "Windows":
            chemin_str = str(chemin_path).replace('/', '\\')
        else:
            chemin_str = str(chemin_path).replace('\\', '/')
        contenu += f'        Remove-Item -Path "{chemin_str}" -Force\n'

    contenu += '    } else {\n'
    contenu += '        Write-Output "Opération annulée..."\n'
    contenu += '    }\n'
    contenu += '} else {\n'
    contenu += '    Write-Output "Opération annulée..."\n'
    contenu += '}\n'

    with open(nom_script, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"Script créé : {nom_script}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Erreur : aucun répertoire fourni")
        sys.exit(1)

    repertoire_base = sys.argv[1]

    liste_fichiers = charger_json("resultats.json")
    liste_couleurs = generer_couleurs_aleatoires(100)

    appli = QApplication(sys.argv)
    fenetre = Onglets()

    fromage = Camembert(liste_fichiers, liste_couleurs)
    layout_fromage = fromage.dessine_camembert()
    fenetre.add_onglet("Camembert", layout_fromage)

    liste_legende = []
    nb_pages = (len(liste_fichiers) + NB_LEGENDES_PAR_PAGE - 1) // NB_LEGENDES_PAR_PAGE

    for num_page in range(nb_pages):
        index_debut = num_page * NB_LEGENDES_PAR_PAGE
        legende = Legendes(liste_fichiers, liste_couleurs, index_debut)
        liste_legende.append(legende)
        layout_legende = legende.dessine_legendes()
        fenetre.add_onglet(f"Légende {num_page + 1}", layout_legende)

    ihm = Boutons(repertoire_base, creation_script_suppression)
    layout_ihm = ihm.dessine_boutons()
    fenetre.add_onglet("IHM", layout_ihm)

    fenetre.show()
    sys.exit(appli.exec_())