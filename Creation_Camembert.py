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

        taille_totale = sum(f[1] for f in self.liste_fichiers)
        font = QFont("Arial Narrow", 12, QFont.Bold)

        for i, (path, taille) in enumerate(self.liste_fichiers):
            etiquette = f"{taille // 1048576}MiB"
            pourcentage = taille / taille_totale * 100
            slice_ = series.append(etiquette, pourcentage)
            slice_.setBrush(self.liste_couleurs[i])
            slice_.setLabelFont(font)
            slice_.setLabelPosition(slice_.LabelOutside)

        for slice_ in series.slices():
            slice_.setLabelVisible(slice_.angleSpan() > 6)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Répartition des tailles des fichiers")
        chart.legend().hide()

        return QChartView(chart)
