
Write-Output
Write-Output
Write-Output


Write-Output

$repertoire_base = python selection_dossier.py


if (-not $repertoire_base) {
    Write-Output
    exit
}


if (-not (Test-Path $repertoire_base)) {
    Write-Output
    exit
}

Write-Output "Dossier sélectionné : $repertoire_base"


Write-Output
python analyse_fichiers.py "$repertoire_base"


if (-not (Test-Path "gros_fichiers.json")) {
    Write-Output "Erreur : fichier JSON non créé."
    exit
}

Write-Output "Analyse terminée. Fichier JSON créé."


Write-Output "Lancement de l'interface graphique..."
python affichage_camembert.py

Write-Output "Fin du script principal."
