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

NB_LEGENDES_PAR_PAGE = 25
NOM_FICHIER_JSON = "gros_fichiers.json"
NOM_SCRIPT_SUPPRESSION = "Suppression_Fichiers.ps1"

def lire_fichier_json(nom_fichier):
    with open(nom_fichier, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for f in data:
        f[0] = f[0].replace('\\\\', '\\')
    return data

def generer_couleurs(nb):
    return [QColor(random.randint(0,255), random.randint(0,255), random.randint(0,255)) for _ in range(nb)]

def creation_script_suppression():
    fichiers = []

    for page in liste_legendes:
        etats = page.recupere_etats_cases_a_cocher()
        start = page.num_start
        for i, coche in enumerate(etats):
            if coche:
                fichiers.append(liste_fichiers[start + i][0])

    if not fichiers:
        return

    with open(NOM_SCRIPT_SUPPRESSION, 'w', encoding='utf-8') as f:
        f.write('$r=Read-Host "Confirmer suppression (OUI)"\n')
        f.write('if($r -eq "OUI"){\n')
        for fichier in fichiers:
            chemin = fichier if platform.system()=="Windows" else fichier.replace('\\','/')
            f.write(f'Remove-Item "{chemin}" -Force\n')
        f.write('}\n')

if __name__ == "__main__":
    repertoire_base = sys.argv[1]
    liste_fichiers = lire_fichier_json(NOM_FICHIER_JSON)
    couleurs = generer_couleurs(len(liste_fichiers))

    app = QApplication(sys.argv)
    fenetre = Onglets()

    camembert = Camembert(liste_fichiers, couleurs)
    fenetre.add_onglet("Camembert", camembert.dessine_camembert())

    liste_legendes = []
    pages = (len(liste_fichiers) + NB_LEGENDES_PAR_PAGE - 1) // NB_LEGENDES_PAR_PAGE

    for i in range(pages):
        leg = Legendes(liste_fichiers, couleurs, i*NB_LEGENDES_PAR_PAGE, NB_LEGENDES_PAR_PAGE)
        liste_legendes.append(leg)
        fenetre.add_onglet(f"Légende {i+1}", leg.dessine_legendes())

    ihm = Boutons(repertoire_base, creation_script_suppression)
    fenetre.add_onglet("IHM", ihm.dessine_boutons())

    fenetre.show()
    sys.exit(app.exec_())
