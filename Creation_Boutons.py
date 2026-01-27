from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt

class Boutons:
    def __init__(self, repertoire_base, callback):
        self.repertoire_base = repertoire_base
        self.callback = callback

    def dessine_boutons(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignTop)

        bouton = QPushButton("Créer le script pwsh de suppression des fichiers...")
        bouton.clicked.connect(self.callback)
        layout.addWidget(bouton, alignment=Qt.AlignHCenter)

        text = QLineEdit(self.repertoire_base)
        layout.addWidget(text, alignment=Qt.AlignHCenter)

        return widget
