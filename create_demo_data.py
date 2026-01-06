"""
Script pour créer des données de démonstration pour Work&Vibe.
Exécutez ce script avec: python manage.py shell < create_demo_data.py
"""

from django.contrib.auth import get_user_model
from core.models import Establishment, TimeSlot, Booking
from datetime import date, time, timedelta

User = get_user_model()

print("🚀 Création des données de démonstration...")

# Créer des utilisateurs de test
print("\n👥 Création des utilisateurs...")

# Supprimer les données existantes (optionnel)
# User.objects.all().delete()
# Establishment.objects.all().delete()
# TimeSlot.objects.all().delete()
# Booking.objects.all().delete()

# Utilisateur Particulier
particulier, created = User.objects.get_or_create(
    username='marie_dupont',
    defaults={
        'email': 'marie@example.com',
        'user_type': 'PARTICULIER',
        'phone': '0601020304',
        'first_name': 'Marie',
        'last_name': 'Dupont'
    }
)
if created:
    particulier.set_password('demo123')
    particulier.save()
    print("✅ Utilisateur Particulier créé: marie_dupont / demo123")

# Utilisateur Entreprise
entreprise, created = User.objects.get_or_create(
    username='startup_innovante',
    defaults={
        'email': 'contact@startup.com',
        'user_type': 'ENTREPRISE',
        'phone': '0612345678',
        'company_name': 'Startup Innovante',
        'first_name': 'Jean',
        'last_name': 'Martin'
    }
)
if created:
    entreprise.set_password('demo123')
    entreprise.save()
    print("✅ Utilisateur Entreprise créé: startup_innovante / demo123")

# Utilisateur Établissement
etablissement_user, created = User.objects.get_or_create(
    username='cafe_central',
    defaults={
        'email': 'contact@cafecentral.fr',
        'user_type': 'ETABLISSEMENT',
        'phone': '0123456789',
        'company_name': 'Café Central',
        'first_name': 'Pierre',
        'last_name': 'Bernard'
    }
)
if created:
    etablissement_user.set_password('demo123')
    etablissement_user.save()
    print("✅ Utilisateur Établissement créé: cafe_central / demo123")

# Créer des établissements
print("\n🏢 Création des établissements...")

cafe_central = Establishment.objects.create(
    owner=etablissement_user,
    name='Café Central',
    establishment_type='CAFE',
    address='15 Rue de la République',
    city='Paris',
    description='Un café cosy au cœur de Paris, parfait pour travailler dans une ambiance chaleureuse.',
    wifi_available=True,
    power_outlets=True,
    quiet_zone=True,
    free_coffee=True
)
print(f"✅ Établissement créé: {cafe_central.name}")

bar_coworking = Establishment.objects.create(
    owner=etablissement_user,
    name='Le Comptoir du Coworking',
    establishment_type='BAR',
    address='42 Avenue des Entrepreneurs',
    city='Lyon',
    description='Bar moderne avec espaces dédiés au coworking. WiFi haut débit et ambiance conviviale.',
    wifi_available=True,
    power_outlets=True,
    quiet_zone=False,
    free_coffee=False
)
print(f"✅ Établissement créé: {bar_coworking.name}")

restaurant_work = Establishment.objects.create(
    owner=etablissement_user,
    name='Bistrot & Business',
    establishment_type='RESTAURANT',
    address='8 Place du Marché',
    city='Marseille',
    description='Restaurant avec espace coworking le matin. Cuisine traditionnelle et WiFi gratuit.',
    wifi_available=True,
    power_outlets=True,
    quiet_zone=True,
    free_coffee=True
)
print(f"✅ Établissement créé: {restaurant_work.name}")

# Créer des créneaux
print("\n📅 Création des créneaux...")

today = date.today()
tomorrow = today + timedelta(days=1)
after_tomorrow = today + timedelta(days=2)

# Créneaux pour aujourd'hui
slot1 = TimeSlot.objects.create(
    establishment=cafe_central,
    title='Matinée Productive',
    description='Créneau matinal pour démarrer la journée en douceur avec un café offert.',
    date=today,
    start_time=time(9, 0),
    end_time=time(12, 0),
    total_capacity=15,
    price_info='Gratuit',
    is_group_only=False
)
print(f"✅ Créneau créé: {slot1.title}")

slot2 = TimeSlot.objects.create(
    establishment=bar_coworking,
    title='After-Work Networking',
    description='Séance de coworking en fin de journée, idéale pour le networking.',
    date=today,
    start_time=time(17, 0),
    end_time=time(20, 0),
    total_capacity=20,
    price_info='Consommation obligatoire',
    is_group_only=False
)
print(f"✅ Créneau créé: {slot2.title}")

# Créneaux pour demain
slot3 = TimeSlot.objects.create(
    establishment=restaurant_work,
    title='Petit-déjeuner Coworking',
    description='Travaillez tout en profitant d\'un excellent petit-déjeuner.',
    date=tomorrow,
    start_time=time(8, 0),
    end_time=time(11, 0),
    total_capacity=10,
    price_info='15€ (petit-déjeuner inclus)',
    is_group_only=False
)
print(f"✅ Créneau créé: {slot3.title}")

slot4 = TimeSlot.objects.create(
    establishment=cafe_central,
    title='Session Focus Afternoon',
    description='Après-midi silencieux pour un travail concentré.',
    date=tomorrow,
    start_time=time(14, 0),
    end_time=time(18, 0),
    total_capacity=12,
    price_info='Gratuit',
    is_group_only=False
)
print(f"✅ Créneau créé: {slot4.title}")

slot5 = TimeSlot.objects.create(
    establishment=bar_coworking,
    title='Journée Complète Startup',
    description='Journée dédiée aux startups. Espace privatisable pour votre équipe.',
    date=after_tomorrow,
    start_time=time(9, 0),
    end_time=time(18, 0),
    total_capacity=25,
    price_info='20€ par personne',
    is_group_only=True
)
print(f"✅ Créneau créé: {slot5.title}")

# Créer quelques réservations
print("\n🎫 Création de réservations...")

booking1 = Booking.objects.create(
    user=particulier,
    time_slot=slot1,
    number_of_places=1,
    status='CONFIRMED',
    notes='J\'ai hâte de travailler dans ce cadre !'
)
print(f"✅ Réservation créée: {booking1.user.username} -> {booking1.time_slot.title}")

booking2 = Booking.objects.create(
    user=entreprise,
    time_slot=slot3,
    number_of_places=3,
    status='CONFIRMED',
    notes='Réservation pour l\'équipe marketing'
)
print(f"✅ Réservation créée: {booking2.user.username} -> {booking2.time_slot.title}")

booking3 = Booking.objects.create(
    user=particulier,
    time_slot=slot4,
    number_of_places=1,
    status='CONFIRMED'
)
print(f"✅ Réservation créée: {booking3.user.username} -> {booking3.time_slot.title}")

print("\n✨ Données de démonstration créées avec succès !")
print("\n📝 Comptes de test créés:")
print("   Particulier: marie_dupont / demo123")
print("   Entreprise: startup_innovante / demo123")
print("   Établissement: cafe_central / demo123")
print("\n🌐 Accédez à http://localhost:8000 pour tester l'application!")
