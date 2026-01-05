import csv

etudiants = [
    {"ID": 1, "Nom": "Schmitt", "Prenom": "Albert", "Note": 9},
    {"ID": 2, "Nom": "Al-Hakim", "Prenom": "Yasmine", "Note": 17},
    {"ID": 3, "Nom": "Tran", "Prenom": "Sebastien", "Note": 12},
    {"ID": 4, "Nom": "Meyer", "Prenom": "Claire", "Note": 16},
    {"ID": 5, "Nom": "Kobayashi", "Prenom": "Kaito", "Note": 11}
]
with open("donnees.csv", "w", newline="", encoding="utf-8") as fichier:
    writer = csv.writer(fichier)
    writer.writerow(["ID", "Nom", "Prenom", "Note"])

