import sys
from PyQt5.QtWidgets import QApplication, QFileDialog

def get_directory():
    app = QApplication(sys.argv)
    folder = QFileDialog.getExistingDirectory(None, "Sélectionnez le répertoire à analyser")
    if folder:
        print(folder)
    sys.exit(0)

if __name__ == "__main__":
    get_directory()