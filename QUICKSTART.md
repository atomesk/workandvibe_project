# 🚀 Guide de Démarrage Rapide - Work&Vibe

## Installation en 3 étapes

### 1️⃣ Naviguer vers le projet
```powershell
cd workandvibe_project
```

### 2️⃣ Lancer le script de démarrage
```powershell
.\start.ps1
```

**Ou manuellement :**

```powershell
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Installer les dépendances
pip install -r requirements.txt

# Créer la base de données
python manage.py makemigrations
python manage.py migrate

# Créer un superutilisateur (optionnel)
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver
```

### 3️⃣ Accéder à l'application
- **Interface utilisateur :** http://localhost:8000
- **Interface admin :** http://localhost:8000/admin

---

## 📱 Première Utilisation

### Créer un compte Établissement
1. Cliquez sur "Inscription"
2. Sélectionnez "Établissement" comme type de compte
3. Remplissez les informations
4. Créez votre établissement depuis le Dashboard
5. Créez vos premiers créneaux

### Créer un compte Particulier/Entreprise
1. Cliquez sur "Inscription"
2. Sélectionnez votre type de compte
3. Explorez les créneaux disponibles
4. Réservez gratuitement !

---

## 🎨 Caractéristiques

✅ **Mobile-First Design** - Optimisé pour smartphone  
✅ **Glassmorphism** - Effets de flou modernes  
✅ **Bottom Nav Bar** - Navigation mobile intuitive  
✅ **Tailwind CSS** - Design système ultra-moderne  
✅ **Réservation gratuite** - Paiement sur place uniquement  

---

## 🛠️ Commandes Utiles

```powershell
# Créer un superutilisateur
python manage.py createsuperuser

# Créer de nouvelles migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Lancer le serveur
python manage.py runserver

# Créer un nouvel utilisateur depuis le shell
python manage.py shell
```

---

## 📚 Structure des Modèles

### CustomUser
- Types : Particulier, Entreprise, Établissement
- Champs : username, email, phone, company_name, avatar

### Establishment
- Propriétaire, nom, type, adresse, ville
- Équipements : WiFi, prises, zone silencieuse, café offert

### TimeSlot
- Créneau de coworking avec date/heure
- Capacité et places disponibles
- Information tarifaire

### Booking
- Réservation d'un créneau
- Statuts : Confirmé, Annulé, Terminé

---

## 🎯 Prochaines Étapes

1. Personnaliser le logo dans le header
2. Ajouter des images pour les établissements
3. Configurer les emails de confirmation
4. Déployer en production (Heroku, DigitalOcean, etc.)

---

## ⚡ Dépannage

**Erreur : "No module named 'django'"**
```powershell
# Assurez-vous que l'environnement virtuel est activé
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Erreur : "Table doesn't exist"**
```powershell
python manage.py makemigrations
python manage.py migrate
```

**Le serveur ne démarre pas**
```powershell
# Vérifiez que le port 8000 n'est pas utilisé
# Ou utilisez un autre port
python manage.py runserver 8080
```

---

## 📞 Support

Pour toute question, consultez :
- README.md pour la documentation complète
- Les commentaires dans le code
- La documentation Django : https://docs.djangoproject.com/

---

**Bon développement ! 🎉**
