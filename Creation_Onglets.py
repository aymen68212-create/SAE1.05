from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QMainWindow

class Onglets(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Résultat de recherche des gros fichiers...")
        self.setGeometry(200, 100, 1000, 700)
        self.onglets = QTabWidget()
        self.setCentralWidget(self.onglets)

    def add_onglet(self, titre, widget):
        onglet = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(widget)
        onglet.setLayout(layout)
        self.onglets.addTab(onglet, titre)
