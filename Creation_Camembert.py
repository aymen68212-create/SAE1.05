from PyQt5.QtChart import QChart, QChartView, QPieSeries
from PyQt5.QtGui import QFont


class Camembert:
    def __init__(self, liste_fichiers, liste_couleurs):
        self.liste_fichiers = liste_fichiers
        self.liste_couleurs = liste_couleurs

    def dessine_camembert(self):
        if not self.liste_fichiers:
            raise ValueError("La liste doit contenir au moins 1 fichier.")

        series = QPieSeries()
        series.setLabelsVisible(True)

        taille_totale = sum([f[1] for f in self.liste_fichiers])

        font = QFont("Arial Narrow", 12, QFont.Bold)
        for path_fichier, taille_fichier in self.liste_fichiers:
            etiquette = f"{taille_fichier // 1048576}MiB"
            pourcentage = taille_fichier / taille_totale * 100
            slice_ = series.append(etiquette, pourcentage)
            slice_.setBrush(self.liste_couleurs[len(series) - 1])
            slice_.setLabelFont(font)
            slice_.setLabelPosition(slice_.LabelPosition.LabelOutside)

        for slice_ in series.slices():
            slice_.setLabelVisible(slice_.angleSpan() > 6)

        fromage = QChart()
        fromage.addSeries(series)
        fromage.setTitle("Répartition des tailles des fichiers")
        fromage.legend().hide()

        layout_fromage = QChartView(fromage)
        return layout_fromage