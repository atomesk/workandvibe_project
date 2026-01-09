# 📄 Fichier d'Instructions : Projet Work&Vibe (2025)

Ce document sert de référence pour GitHub Copilot afin de générer le code source de l'application.

---

## 1. Vision & Architecture Globale
* **Nom du projet :** Work&Vibe
* **Concept :** Plateforme de réservation de créneaux de travail/networking dans des établissements (bars, pubs, restaurants) pour des entrepreneurs et entreprises.
* **Modèle Économique :** Réservation gratuite sur l'application. Paiement sur place (directement à l'établissement).
* **Priorité UX :** Mobile-First (Design conçu pour smartphone d'abord, adaptatif desktop).
* **Style Visuel :** SaaS moderne 2025 (Glassmorphism, coins arrondis `3xl`, ombres douces, typographie épurée type "Inter").

---

## 2. Stack Technique
- **Backend :** Django 5.x
- **Base de données :** SQLite (Développement rapide)
- **Frontend :**
    - HTML5 / JavaScript moderne (ES6+)
    - Tailwind CSS (via CDN ou config locale)
    - Architecture : Templates Django (DRY)

---

## 3. Spécifications du Modèle de Données (models.py)

### A. Utilisateurs (AbstractUser)
- **Types :** Particulier, Entreprise, Établissement.
- **Champs additionnels :** Téléphone, Nom de l'entreprise (optionnel), Logo/Avatar.

### B. Établissements
- **Champs :** Nom, Type (Bar, Restaurant, Pub, Nightclub), Adresse, Ville, Description, Équipements (WiFi, Prises, Silencieux, Café offert).

### C. Créneaux (TimeSlots)
- **Champs :** Titre, Description, Date, Heure de début, Heure de fin.
- **Capacité :** Nombre total de places disponibles.
- **Type d'offre :** Prix affiché (ex: "Consommation obligatoire", "10€ la matinée") ou "Gratuit".
- **Logique de groupe :** Autoriser soit la réservation individuelle, soit la réservation de groupe (pour les entreprises).

### D. Réservations (Bookings)
- **Logique :** Un utilisateur réserve un nombre `n` de places.
- **Validation :** Vérifier que `n <= places_disponibles`.
- **Statut :** Confirmé, Annulé, Terminé.

---

## 4. Interfaces & Expérience Utilisateur (UI/UX)

### 📱 Mobile-First Design
- **Navigation :** Bottom Bar (Accueil, Recherche, Mes Réservations, Profil).
- **Cartes (Cards) :** Design arrondi avec image en fond ou en haut, badges pour les tarifs et les équipements.

### 🏠 Landing Page
- **Header :** Logo à gauche, bouton Profil à droite.
- **Recherche :** Barre de recherche sticky avec filtres rapides (Aujourd'hui, Demain, WiFi, Bars).
- **Liste :** Flux vertical de créneaux disponibles.

### 🏢 Dashboard Établissement
- Vue simplifiée pour créer un créneau en 3 clics.
- Liste des réservations du jour pour faire le "check-in" à l'entrée.

---

## 5. Logique Métier spécifique pour Copilot

1.  **Réservation Gratuite :** Le processus de réservation ne doit demander aucune information de carte bancaire. Afficher clairement : "Réservation gratuite - Paiement sur place".
2.  **Calcul des places :** Dans la vue de réservation, soustraire dynamiquement les places réservées de la capacité totale du `TimeSlot`.
3.  **Filtres de recherche :** Implémenter une recherche par ville et par type d'établissement via les paramètres `GET` de Django.
4.  **Authentification :** Créer des formulaires d'inscription distincts pour les clients et les gérants d'établissements.

---

## 6. Prompt Initial suggéré pour démarrer le code

> "Génère l'arborescence Django pour le projet 'Work&Vibe'. 
> Commence par créer un `CustomUser` dans `models.py` avec les rôles (Particulier, Entreprise, Établissement). 
> Ajoute les modèles `Establishment`, `TimeSlot` et `Booking` avec la logique de capacité. 
> Pour le front, utilise Tailwind CSS pour créer une page d'accueil mobile-first ultra-moderne (style 2025) avec une barre de recherche et des cartes de réservation élégantes."


