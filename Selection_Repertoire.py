from PyQt5.QtWidgets import QApplication, QFileDialog
from pathlib import Path
import sys

def selectionner_repertoire():
    app = QApplication(sys.argv)
    repertoire = QFileDialog.getExistingDirectory(
        None,
        "Sélectionnez le répertoire de base à analyser",
        str(Path.home())
    )
    return repertoire

if __name__ == "__main__":
    repertoire_selectionne = selectionner_repertoire()
    if repertoire_selectionne:
        print(repertoire_selectionne)
    else:
        print("")
