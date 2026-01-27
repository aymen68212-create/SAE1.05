from pathlib import Path
import json
import sys

# Constantes
NB_MAXI_FICHIERS = 100
TAILLE_MINI_FICHIER_EN_MEBI_OCTET = 1
NOM_FICHIER_JSON = "gros_fichiers.json"


def inventorier_fichiers(repertoire_de_base):
    """
    Parcourt récursivement tous les fichiers du répertoire de base.
    Retourne une liste de listes : [[chemin_complet, taille_en_octets], ...]
    """
    liste_fichiers = []

    # Conversion en objet Path
    rep_path = Path(repertoire_de_base)

    # Parcours récursif de tous les fichiers
    for fichier in rep_path.rglob("*"):
        # On ne garde que les fichiers (pas les dossiers)
        if fichier.is_file():
            try:
                # Récupération du chemin complet et de la taille
                chemin_complet = str(fichier.resolve())
                taille_octets = fichier.stat().st_size

                # Ajout à la liste
                liste_fichiers.append([chemin_complet, taille_octets])
            except:
                # En cas d'erreur (fichier inaccessible), on passe au suivant
                pass

    return liste_fichiers


def trier_par_taille(liste_fichiers):
    """
    Trie la liste de fichiers par taille décroissante.
    Retourne la liste triée.
    """
    # Tri avec lambda : on utilise le 2ème élément (index 1) comme clé
    # reverse=True pour ordre décroissant (du plus gros au plus petit)
    liste_triee = sorted(liste_fichiers, key=lambda x: x[1], reverse=True)

    return liste_triee


def filtrer_fichiers(liste_fichiers, taille_mini_en_mio, nb_maxi):
    """
    Ne conserve que les fichiers dont la taille est supérieure au seuil.
    Limite le nombre de fichiers au maximum spécifié.
    Retourne la liste filtrée.
    """
    # Conversion de la taille minimale en octets
    taille_mini_octets = taille_mini_en_mio * 1048576

    # Filtrage par taille
    liste_filtree = []
    for fichier in liste_fichiers:
        if fichier[1] >= taille_mini_octets:
            liste_filtree.append(fichier)

    # Limitation au nombre maximum avec slicing
    liste_filtree = liste_filtree[:nb_maxi]

    return liste_filtree


def creer_fichier_json(liste_fichiers, nom_fichier):
    """
    Sauvegarde la liste de fichiers dans un fichier JSON.
    """
    # Remplacement des antislashs pour Windows
    for liste_fichier in liste_fichiers:
        liste_fichier[0] = liste_fichier[0].replace('\\', '\\\\')

    # Écriture du fichier JSON
    with open(nom_fichier, 'w', encoding='utf-8') as f:
        json.dump(liste_fichiers, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    # Vérification de la présence d'un argument
    if len(sys.argv) < 2:
        print("Erreur : Aucun répertoire spécifié.")
        print("Usage : python Analyse_Arborescence.py <repertoire_de_base>")
        sys.exit(1)

    # Récupération du répertoire de base passé en argument
    repertoire_de_base = sys.argv[1]

    # Vérification que le répertoire existe
    if not Path(repertoire_de_base).exists():
        print(f"Erreur : Le répertoire '{repertoire_de_base}' n'existe pas.")
        sys.exit(1)

    print(f"Analyse du répertoire : {repertoire_de_base}")
    print("Inventaire des fichiers en cours...")

    # Étape 1 : Inventaire de tous les fichiers
    liste_fichiers = inventorier_fichiers(repertoire_de_base)
    print(f"  -> {len(liste_fichiers)} fichiers trouvés")

    # Étape 2 : Tri par taille décroissante
    liste_fichiers = trier_par_taille(liste_fichiers)
    print("  -> Fichiers triés par taille")

    # Étape 3 : Filtrage
    liste_fichiers = filtrer_fichiers(
        liste_fichiers,
        TAILLE_MINI_FICHIER_EN_MEBI_OCTET,
        NB_MAXI_FICHIERS
    )
    print(f"  -> {len(liste_fichiers)} fichiers conservés (>{TAILLE_MINI_FICHIER_EN_MEBI_OCTET} MiB)")

    # Étape 4 : Création du fichier JSON
    creer_fichier_json(liste_fichiers, NOM_FICHIER_JSON)
    print(f"  -> Fichier '{NOM_FICHIER_JSON}' créé avec succès")

    print("Analyse terminée !")