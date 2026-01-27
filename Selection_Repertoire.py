from PyQt5.QtWidgets import QApplication, QFileDialog
from pathlib import Path
import sys


def selectionner_repertoire():
    """
    Ouvre une boîte de dialogue pour sélectionner un répertoire.
    Retourne le chemin absolu du répertoire sélectionné.
    """
    # Création de l'application Qt
    app = QApplication(sys.argv)

    # Ouverture du sélecteur de répertoire
    repertoire = QFileDialog.getExistingDirectory(
        None,
        "Sélectionnez le répertoire de base à analyser",
        str(Path.home())
    )

    # Retour du répertoire sélectionné (chaîne vide si annulation)
    return repertoire


if __name__ == "__main__":
    # Programme principal
    repertoire_selectionne = selectionner_repertoire()

    if repertoire_selectionne:
        # Affichage du répertoire sélectionné
        print(repertoire_selectionne)
    else:
        # Aucun répertoire sélectionné
        print("")