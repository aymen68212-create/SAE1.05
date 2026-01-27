from pathlib import Path
import json
import sys

NB_MAXI_FICHIERS = 100
TAILLE_MINI_FICHIER_EN_MEBI_OCTET = 1
NOM_FICHIER_JSON = "gros_fichiers.json"

def inventorier_fichiers(repertoire_de_base):
    liste_fichiers = []
    rep_path = Path(repertoire_de_base)

    for fichier in rep_path.rglob("*"):
        if fichier.is_file():
            try:
                chemin_complet = str(fichier.resolve())
                taille_octets = fichier.stat().st_size
                liste_fichiers.append([chemin_complet, taille_octets])
            except:
                pass

    return liste_fichiers

def trier_par_taille(liste_fichiers):
    return sorted(liste_fichiers, key=lambda x: x[1], reverse=True)

def filtrer_fichiers(liste_fichiers, taille_mini_en_mio, nb_maxi):
    taille_mini_octets = taille_mini_en_mio * 1048576
    liste_filtree = []

    for fichier in liste_fichiers:
        if fichier[1] >= taille_mini_octets:
            liste_filtree.append(fichier)

    return liste_filtree[:nb_maxi]

def creer_fichier_json(liste_fichiers, nom_fichier):
    for fichier in liste_fichiers:
        fichier[0] = fichier[0].replace('\\', '\\\\')

    with open(nom_fichier, 'w', encoding='utf-8') as f:
        json.dump(liste_fichiers, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    repertoire_de_base = sys.argv[1]

    if not Path(repertoire_de_base).exists():
        sys.exit(1)

    liste_fichiers = inventorier_fichiers(repertoire_de_base)
    liste_fichiers = trier_par_taille(liste_fichiers)
    liste_fichiers = filtrer_fichiers(
        liste_fichiers,
        TAILLE_MINI_FICHIER_EN_MEBI_OCTET,
        NB_MAXI_FICHIERS
    )
    creer_fichier_json(liste_fichiers, NOM_FICHIER_JSON)
