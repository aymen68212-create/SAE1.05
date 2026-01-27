Write-Output "=============================================="
Write-Output "  Outil de recherche des gros fichiers"
Write-Output "=============================================="
Write-Output ""

# Étape 1 : Sélection du répertoire de base
Write-Output "Étape 1 : Sélection du répertoire à analyser..."
$rep_base = python Selection_Repertoire.py

# Vérification que l'utilisateur a bien sélectionné un répertoire
if (-not $rep_base) {
    Write-Output "Erreur : Aucun répertoire sélectionné."
    Write-Output "Opération annulée."
    exit
}

# Vérification que le répertoire existe
if (Test-Path $rep_base) {
    Write-Output "  -> Répertoire sélectionné : $rep_base"
    Write-Output ""
} else {
    Write-Output "Erreur : Le répertoire '$rep_base' n'existe pas."
    Write-Output "Opération annulée."
    exit
}

# Étape 2 : Analyse de l'arborescence
Write-Output "Étape 2 : Analyse de l'arborescence..."
python Analyse_Arborescence.py "$rep_base"
Write-Output ""

# Étape 3 : Affichage graphique des résultats
Write-Output "Étape 3 : Affichage des résultats..."
python Affichage_Resultats.py "$rep_base"

Write-Output ""
Write-Output "=============================================="
Write-Output "  Analyse terminée"
Write-Output "=============================================="


