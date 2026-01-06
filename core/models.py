from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class CustomUser(AbstractUser):
    """
    Modèle d'utilisateur personnalisé avec trois types d'utilisateurs.
    """
    USER_TYPE_CHOICES = [
        ('PARTICULIER', 'Particulier'),
        ('ENTREPRISE', 'Entreprise'),
        ('ETABLISSEMENT', 'Établissement'),
    ]
    
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='PARTICULIER',
        verbose_name='Type d\'utilisateur'
    )
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Téléphone')
    company_name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Nom de l\'entreprise')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Avatar')
    
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class Establishment(models.Model):
    """
    Modèle représentant un établissement (bar, restaurant, pub, etc.).
    """
    ESTABLISHMENT_TYPE_CHOICES = [
        ('BAR', 'Bar'),
        ('RESTAURANT', 'Restaurant'),
        ('PUB', 'Pub'),
        ('NIGHTCLUB', 'Nightclub'),
        ('CAFE', 'Café'),
        ('COWORKING', 'Espace Coworking'),
    ]
    
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='establishments',
        verbose_name='Propriétaire'
    )
    name = models.CharField(max_length=200, verbose_name='Nom')
    establishment_type = models.CharField(
        max_length=20,
        choices=ESTABLISHMENT_TYPE_CHOICES,
        verbose_name='Type d\'établissement'
    )
    address = models.CharField(max_length=300, verbose_name='Adresse')
    city = models.CharField(max_length=100, verbose_name='Ville')
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    logo = models.ImageField(upload_to='establishments/', blank=True, null=True, verbose_name='Logo')
    
    # Équipements
    wifi_available = models.BooleanField(default=False, verbose_name='WiFi disponible')
    power_outlets = models.BooleanField(default=False, verbose_name='Prises électriques')
    quiet_zone = models.BooleanField(default=False, verbose_name='Zone silencieuse')
    free_coffee = models.BooleanField(default=False, verbose_name='Café offert')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Dernière modification')
    
    class Meta:
        verbose_name = 'Établissement'
        verbose_name_plural = 'Établissements'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.city}"


class TimeSlot(models.Model):
    """
    Modèle représentant un créneau de coworking disponible dans un établissement.
    """
    establishment = models.ForeignKey(
        Establishment,
        on_delete=models.CASCADE,
        related_name='time_slots',
        verbose_name='Établissement'
    )
    title = models.CharField(max_length=200, verbose_name='Titre')
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    date = models.DateField(verbose_name='Date')
    start_time = models.TimeField(verbose_name='Heure de début')
    end_time = models.TimeField(verbose_name='Heure de fin')
    
    total_capacity = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Capacité totale'
    )
    
    # Prix informatif (pas de paiement en ligne)
    price_info = models.CharField(
        max_length=100,
        default='Gratuit',
        verbose_name='Information tarifaire',
        help_text='Ex: "Gratuit", "10€ la matinée", "Consommation obligatoire"'
    )
    
    # Type de réservation
    is_group_only = models.BooleanField(
        default=False,
        verbose_name='Réservation de groupe uniquement'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Dernière modification')
    
    class Meta:
        verbose_name = 'Créneau'
        verbose_name_plural = 'Créneaux'
        ordering = ['date', 'start_time']
    
    def __str__(self):
        return f"{self.title} - {self.date} ({self.start_time}-{self.end_time})"
    
    def available_capacity(self):
        """Calcule le nombre de places disponibles."""
        confirmed_bookings = self.bookings.filter(status='CONFIRMED')
        reserved_places = sum(booking.number_of_places for booking in confirmed_bookings)
        return self.total_capacity - reserved_places
    
    def is_available(self, number_of_places=1):
        """Vérifie si le nombre de places demandées est disponible."""
        return self.available_capacity() >= number_of_places
    
    def clean(self):
        """Validation personnalisée."""
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError('L\'heure de fin doit être après l\'heure de début.')


class Booking(models.Model):
    """
    Modèle représentant une réservation d'un créneau par un utilisateur.
    """
    STATUS_CHOICES = [
        ('CONFIRMED', 'Confirmé'),
        ('CANCELLED', 'Annulé'),
        ('COMPLETED', 'Terminé'),
    ]
    
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='Utilisateur'
    )
    time_slot = models.ForeignKey(
        TimeSlot,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='Créneau'
    )
    number_of_places = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Nombre de places'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='CONFIRMED',
        verbose_name='Statut'
    )
    
    notes = models.TextField(blank=True, null=True, verbose_name='Notes')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date de réservation')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Dernière modification')
    
    class Meta:
        verbose_name = 'Réservation'
        verbose_name_plural = 'Réservations'
        ordering = ['-created_at']
    
    def __str__(self):
        if self.time_slot:
            return f"{self.user.username} - {self.time_slot.title} ({self.number_of_places} place(s))"
        return f"{self.user.username} - Réservation ({self.number_of_places} place(s))"
    
    def clean(self):
        """Validation personnalisée."""
        # Vérifier si time_slot existe sur l'instance
        if hasattr(self, 'time_slot') and self.number_of_places:
            try:
                time_slot = self.time_slot
                # Vérifier la disponibilité uniquement pour les nouvelles réservations
                if not self.pk:  # Nouvelle réservation
                    if not time_slot.is_available(self.number_of_places):
                        raise ValidationError(
                            f'Seulement {time_slot.available_capacity()} place(s) disponible(s).'
                        )
            except Booking.time_slot.RelatedObjectDoesNotExist:
                # time_slot n'est pas encore assigné, passer la validation
                pass
