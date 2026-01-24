import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QFileDialog

def selection_repertoire():
    app = QApplication(sys.argv)
    repertoire = QFileDialog.getExistingDirectory(
        None,
        "Sélectionnez le répertoire à analyser",
        str(Path.home()),
        QFileDialog.ShowDirsOnly
    )
    return repertoire

if __name__ == "__main__":
    rep = selection_repertoire()
    if rep:
        print(rep)
    else:
        sys.exit(1)