from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from datetime import date, datetime
from .models import TimeSlot, Establishment, Booking, CustomUser
from .forms import CustomUserCreationForm, BookingForm, TimeSlotForm, EstablishmentForm


def index(request):
    """
    Page d'accueil avec la liste des créneaux disponibles et les filtres.
    """
    # Récupérer tous les créneaux futurs
    time_slots = TimeSlot.objects.filter(date__gte=date.today()).select_related('establishment')
    
    # Filtres
    search_query = request.GET.get('search', '')
    city_filter = request.GET.get('city', '')
    establishment_type_filter = request.GET.get('type', '')
    date_filter = request.GET.get('date', '')
    wifi_filter = request.GET.get('wifi', '')
    
    if search_query:
        time_slots = time_slots.filter(
            Q(title__icontains=search_query) |
            Q(establishment__name__icontains=search_query) |
            Q(establishment__city__icontains=search_query)
        )
    
    if city_filter:
        time_slots = time_slots.filter(establishment__city__icontains=city_filter)
    
    if establishment_type_filter:
        time_slots = time_slots.filter(establishment__establishment_type=establishment_type_filter)
    
    if date_filter:
        time_slots = time_slots.filter(date=date_filter)
    
    if wifi_filter:
        time_slots = time_slots.filter(establishment__wifi_available=True)
    
    # Obtenir les villes disponibles pour le filtre
    cities = Establishment.objects.values_list('city', flat=True).distinct()
    
    context = {
        'time_slots': time_slots,
        'cities': cities,
        'search_query': search_query,
        'city_filter': city_filter,
        'establishment_type_filter': establishment_type_filter,
        'date_filter': date_filter,
        'wifi_filter': wifi_filter,
    }
    
    return render(request, 'core/index.html', context)


def timeslot_detail(request, pk):
    """
    Page de détail d'un créneau.
    """
    time_slot = get_object_or_404(TimeSlot, pk=pk)
    
    context = {
        'time_slot': time_slot,
        'available_places': time_slot.available_capacity(),
    }
    
    return render(request, 'core/timeslot_detail.html', context)


@login_required
def book_timeslot(request, pk):
    """
    Page de réservation d'un créneau.
    """
    time_slot = get_object_or_404(TimeSlot, pk=pk)
    
    if request.method == 'POST':
        form = BookingForm(request.POST, time_slot=time_slot)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.time_slot = time_slot
            
            # Vérifier la disponibilité avant de sauvegarder
            if not time_slot.is_available(booking.number_of_places):
                messages.error(request, f'Seulement {time_slot.available_capacity()} place(s) disponible(s).')
            else:
                try:
                    booking.save()
                    messages.success(request, 'Réservation confirmée ! Rendez-vous sur place.')
                    return redirect('my_bookings')
                except Exception as e:
                    messages.error(request, f'Erreur lors de la réservation : {str(e)}')
    else:
        form = BookingForm(time_slot=time_slot)
    
    context = {
        'time_slot': time_slot,
        'form': form,
        'available_places': time_slot.available_capacity(),
    }
    
    return render(request, 'core/book_timeslot.html', context)


@login_required
def my_bookings(request):
    """
    Liste des réservations de l'utilisateur connecté.
    """
    bookings = Booking.objects.filter(user=request.user).select_related('time_slot', 'time_slot__establishment')
    
    context = {
        'bookings': bookings,
    }
    
    return render(request, 'core/my_bookings.html', context)


@login_required
def cancel_booking(request, pk):
    """
    Annuler une réservation.
    """
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    
    if request.method == 'POST':
        booking.status = 'CANCELLED'
        booking.save()
        messages.success(request, 'Réservation annulée.')
        return redirect('my_bookings')
    
    context = {
        'booking': booking,
    }
    
    return render(request, 'core/cancel_booking.html', context)


def register(request):
    """
    Page d'inscription.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Compte créé avec succès !')
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'core/register.html', context)


@login_required
def profile(request):
    """
    Page de profil de l'utilisateur.
    """
    context = {
        'user': request.user,
    }
    
    return render(request, 'core/profile.html', context)


@login_required
def establishment_dashboard(request):
    """
    Dashboard pour les gérants d'établissements.
    """
    if request.user.user_type != 'ETABLISSEMENT':
        messages.error(request, 'Accès réservé aux établissements.')
        return redirect('index')
    
    establishments = Establishment.objects.filter(owner=request.user)
    
    # Récupérer tous les créneaux de l'établissement
    time_slots = TimeSlot.objects.filter(establishment__owner=request.user).select_related('establishment')
    
    # Récupérer les réservations du jour
    today = date.today()
    today_bookings = Booking.objects.filter(
        time_slot__establishment__owner=request.user,
        time_slot__date=today,
        status='CONFIRMED'
    ).select_related('user', 'time_slot')
    
    context = {
        'establishments': establishments,
        'time_slots': time_slots,
        'today_bookings': today_bookings,
    }
    
    return render(request, 'core/establishment_dashboard.html', context)


@login_required
def create_timeslot(request):
    """
    Créer un nouveau créneau.
    """
    if request.user.user_type != 'ETABLISSEMENT':
        messages.error(request, 'Accès réservé aux établissements.')
        return redirect('index')
    
    # Vérifier que l'utilisateur a au moins un établissement
    establishments = Establishment.objects.filter(owner=request.user)
    if not establishments.exists():
        messages.warning(request, 'Vous devez d\'abord créer un établissement.')
        return redirect('create_establishment')
    
    if request.method == 'POST':
        form = TimeSlotForm(request.POST)
        establishment_id = request.POST.get('establishment')
        
        if form.is_valid() and establishment_id:
            time_slot = form.save(commit=False)
            time_slot.establishment = get_object_or_404(Establishment, pk=establishment_id, owner=request.user)
            time_slot.save()
            messages.success(request, 'Créneau créé avec succès !')
            return redirect('establishment_dashboard')
    else:
        form = TimeSlotForm()
    
    context = {
        'form': form,
        'establishments': establishments,
    }
    
    return render(request, 'core/create_timeslot.html', context)


@login_required
def create_establishment(request):
    """
    Créer un nouvel établissement.
    """
    if request.user.user_type != 'ETABLISSEMENT':
        messages.error(request, 'Accès réservé aux établissements.')
        return redirect('index')
    
    if request.method == 'POST':
        form = EstablishmentForm(request.POST, request.FILES)
        if form.is_valid():
            establishment = form.save(commit=False)
            establishment.owner = request.user
            establishment.save()
            messages.success(request, 'Établissement créé avec succès !')
            return redirect('establishment_dashboard')
    else:
        form = EstablishmentForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'core/create_establishment.html', context)
