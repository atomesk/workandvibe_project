# Script de démarrage rapide pour Work&Vibe
# Exécutez ce fichier dans PowerShell: .\start.ps1

Write-Host "🚀 Démarrage de Work&Vibe..." -ForegroundColor Cyan

# Vérifier si l'environnement virtuel existe
if (-Not (Test-Path "venv")) {
    Write-Host "📦 Création de l'environnement virtuel..." -ForegroundColor Yellow
    python -m venv venv
}

# Activer l'environnement virtuel
Write-Host "🔌 Activation de l'environnement virtuel..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Installer les dépendances
Write-Host "📥 Installation des dépendances..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet

# Créer les migrations si nécessaire
if (-Not (Test-Path "db.sqlite3")) {
    Write-Host "🗄️  Création de la base de données..." -ForegroundColor Yellow
    python manage.py makemigrations
    python manage.py migrate
    
    Write-Host ""
    Write-Host "👤 Création d'un superutilisateur..." -ForegroundColor Yellow
    Write-Host "   (Vous pouvez créer un superutilisateur plus tard avec: python manage.py createsuperuser)" -ForegroundColor Gray
}

# Lancer le serveur
Write-Host ""
Write-Host "✅ Tout est prêt!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Démarrage du serveur sur http://localhost:8000" -ForegroundColor Cyan
Write-Host "🔐 Admin disponible sur http://localhost:8000/admin" -ForegroundColor Cyan
Write-Host ""
Write-Host "Appuyez sur CTRL+C pour arrêter le serveur" -ForegroundColor Gray
Write-Host ""

python manage.py runserver
