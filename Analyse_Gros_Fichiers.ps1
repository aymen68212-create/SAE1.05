Set-Location $PSScriptRoot
$PYTHON = ".\.venv\Scripts\python.exe"

Write-Output "=============================================="
Write-Output "  Outil de recherche des gros fichiers"
Write-Output "=============================================="
Write-Output ""

Write-Output "Étape 1 : Sélection du répertoire à analyser..."
$rep_base = & $PYTHON Selection_Repertoire.py

if (-not $rep_base) {
    Write-Output "Erreur : Aucun répertoire sélectionné."
    exit
}

if (-not (Test-Path $rep_base)) {
    Write-Output "Erreur : Le répertoire '$rep_base' n'existe pas."
    exit
}

Write-Output "Étape 2 : Analyse de l'arborescence..."
& $PYTHON Analyse_Arborescence.py "$rep_base"

Write-Output "Étape 3 : Affichage des résultats..."
& $PYTHON Affichage_Resultats.py "$rep_base"



