from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt


class Boutons:
    def __init__(self, repertoire_base, callback):
        self.repertoire_base = repertoire_base
        self.callback = callback

    def dessine_boutons(self):
        boutons = QWidget()
        layout_boutons = QVBoxLayout(boutons)
        layout_boutons.setSpacing(10)
        layout_boutons.setAlignment(Qt.AlignTop)

        bouton_genere_delete_script = QPushButton("Créer le script pwsh de suppression des fichiers...")
        bouton_genere_delete_script.setFixedSize(500, 40)
        bouton_genere_delete_script.clicked.connect(self.callback)
        layout_boutons.addWidget(bouton_genere_delete_script, alignment=Qt.AlignHCenter)

        text_repertoire_base = QLineEdit()
        text_repertoire_base.setText(self.repertoire_base)
        text_repertoire_base.setFixedSize(490, 30)
        layout_boutons.addWidget(text_repertoire_base, alignment=Qt.AlignHCenter)

        return boutons