import sys
import json
import random
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QColor
from Creation_Onglets import Onglets
from Creation_Camembert import Camembert
from Creation_Legendes import Legendes
from Creation_Boutons import Boutons


def load_json(filename="data.json"):
    with open(filename, 'r') as f:
        return json.load(f)


def generate_colors(n):
    return [QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(n)]


def create_delete_script():
    pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    data = load_json()
    colors = generate_colors(len(data))

    win = Onglets()

    chart = Camembert(data, colors)
    win.add_onglet("Camembert", chart.dessine_camembert())

    for i in range(0, len(data), 25):
        leg = Legendes(data, colors, i)
        win.add_onglet(f"Légende {i // 25 + 1}", leg.dessine_legendes())

    buttons = Boutons("C:\\", create_delete_script)
    win.add_onglet("IHM", buttons.dessine_boutons())

    win.show()
    sys.exit(app.exec_())