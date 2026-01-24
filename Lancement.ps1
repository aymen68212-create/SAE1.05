Write-Output "========================================"
Write-Output "  Analyse des gros fichiers - SAE 1.05"
Write-Output "========================================"
Write-Output ""

Write-Output "[1/3] Selection du repertoire..."
$rep_base = python Selection_Repertoire.py

if (-not $rep_base) {
    Write-Output "[ERREUR] Aucun repertoire selectionne"
    exit
}

if (Test-Path $rep_base) {
    Write-Output "[OK] Repertoire : $rep_base"
} else {
    Write-Output "[ERREUR] Le repertoire n'existe pas"
    exit
}

Write-Output ""
Write-Output "[2/3] Analyse en cours..."
python Analyse_Fichiers.py "$rep_base"

if (Test-Path "resultats.json") {
    Write-Output "[OK] Analyse terminee"
} else {
    Write-Output "[ERREUR] Fichier JSON non cree"
    exit
}

Write-Output ""
Write-Output "[3/3] Affichage des resultats..."
python Affichage_Resultats.py "$rep_base"

Write-Output ""
Write-Output "Termine !"