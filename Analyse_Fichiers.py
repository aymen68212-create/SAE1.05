import sys
import json
from pathlib import Path


def inventaire_fichiers(repertoire_de_base):
    liste_fichiers = []
    rep_base = Path(repertoire_de_base)

    for element in rep_base.rglob("*"):
        if element.is_file():
            try:
                chemin_complet = str(element.resolve())
                taille = element.stat().st_size
                liste_fichiers.append([chemin_complet, taille])
            except (PermissionError, OSError):
                continue

    return liste_fichiers


def trier_par_taille(liste_fichiers):
    return sorted(liste_fichiers, key=lambda x: x[1], reverse=True)


def filtrer_fichiers(liste_fichiers, taille_mini_mib=1, nb_max=100):
    taille_mini_octets = taille_mini_mib * 1048576
    liste_filtree = [f for f in liste_fichiers if f[1] >= taille_mini_octets]
    return liste_filtree[:nb_max]


def sauvegarder_json(liste_fichiers, nom_fichier="resultats.json"):
    for fichier in liste_fichiers:
        fichier[0] = fichier[0].replace('\\', '\\\\')

    with open(nom_fichier, 'w', encoding='utf-8') as f:
        json.dump(liste_fichiers, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Erreur : aucun répertoire fourni")
        sys.exit(1)

    repertoire = sys.argv[1]
    TAILLE_MINI_MIB = 1
    NB_MAX_FICHIERS = 100

    liste_complete = inventaire_fichiers(repertoire)
    liste_triee = trier_par_taille(liste_complete)
    liste_finale = filtrer_fichiers(liste_triee, TAILLE_MINI_MIB, NB_MAX_FICHIERS)
    sauvegarder_json(liste_finale)