from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QCheckBox
from PyQt5.QtCore import Qt

class Legendes:
    def __init__(self, liste_fichiers, liste_couleurs, num_start, nb_par_page):
        self.liste_fichiers = liste_fichiers
        self.liste_couleurs = liste_couleurs
        self.num_start = num_start
        self.nb_par_page = nb_par_page
        self.num_stop = min(len(liste_fichiers), num_start + nb_par_page)
        self.cases = []

    def dessine_legendes(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignTop)

        for i in range(self.num_start, self.num_stop):
            case = QCheckBox()
            self.cases.append(case)

            carre = QWidget()
            carre.setFixedSize(16, 16)
            carre.setStyleSheet(f"background-color: {self.liste_couleurs[i].name()};")

            chemin = self.liste_fichiers[i][0]
            taille = self.liste_fichiers[i][1] // 1048576
            label = QLabel(f"{chemin} --> ({taille} MiB)")

            ligne = QHBoxLayout()
            ligne.addWidget(case)
            ligne.addWidget(carre)
            ligne.addWidget(label)

            conteneur = QWidget()
            conteneur.setLayout(ligne)
            layout.addWidget(conteneur)

        return widget

    def recupere_etats_cases_a_cocher(self):
        return [case.isChecked() for case in self.cases]
