
from pathlib import Path
import json
import sys


TAILLE_MIN_MIB = 10
NB_MAX_FICHIERS = 100
FICHIER_JSON = "gros_fichiers.json"


MIB_EN_OCTETS = 1048576

def analyser_dossier(repertoire_base):

    liste_fichiers = []

    for element in Path(repertoire_base).rglob("*"):
        if element.is_file():
            chemin = str(element)
            taille = element.stat().st_size
            liste_fichiers.append([chemin, taille])

    return liste_fichiers



def trier_et_filtrer(liste_fichiers):
    """
    - Trie du plus gros au plus petit
    - Supprime les fichiers < taille minimale
    - Limite à NB_MAX_FICHIERS
    """

    liste_fichiers = sorted(
        liste_fichiers,
        key=lambda fichier: fichier[1],
        reverse=True
    )


    liste_filtrée = []
    for fichier in liste_fichiers:
        if fichier[1] >= TAILLE_MIN_MIB * MIB_EN_OCTETS:
            liste_filtrée.append(fichier)


    return liste_filtrée[:NB_MAX_FICHIERS]



def sauvegarder_json(liste_fichiers, nom_fichier):

    for fichier in liste_fichiers:
        fichier[0] = fichier[0].replace("\\", "\\\\")

    with open(nom_fichier, "w", encoding="utf-8") as f:
        json.dump(liste_fichiers, f, indent=2)



if __name__ == "__main__":


    if len(sys.argv) < 2:
        print("ERREUR : aucun dossier fourni")
        print("Utilisation : python analyse_fichiers.py <dossier>")
        sys.exit(1)

    repertoire_base = sys.argv[1]

    print("Analyse du dossier :", repertoire_base)


    fichiers = analyser_dossier(repertoire_base)
    print("Nombre total de fichiers trouvés :", len(fichiers))


    gros_fichiers = trier_et_filtrer(fichiers)
    print("Nombre de gros fichiers :", len(gros_fichiers))


    sauvegarder_json(gros_fichiers, FICHIER_JSON)

    print("Résultat enregistré dans :", FICHIER_JSON)


