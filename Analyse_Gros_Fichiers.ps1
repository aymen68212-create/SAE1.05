# 1. On lance la sélection du dossier et on stocke le résultat
$dossier = python select_dir.py

# 2. Si un dossier a été choisi, on lance l'analyse
if ($dossier) {
    Write-Host "Analyse du dossier : $dossier"
    python scan_files.py "$dossier"

    # 3. Une fois le JSON généré, on lance l'interface graphique
    python main_gui.py
}