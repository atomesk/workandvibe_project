from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Booking, TimeSlot, Establishment


class CustomUserCreationForm(UserCreationForm):
    """
    Formulaire d'inscription personnalisé.
    """
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False, label='Téléphone')
    company_name = forms.CharField(max_length=200, required=False, label='Nom de l\'entreprise')
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'user_type', 'company_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajouter des classes CSS Tailwind pour le style
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full px-4 py-3 rounded-2xl border border-slate-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition'


class BookingForm(forms.ModelForm):
    """
    Formulaire de réservation d'un créneau.
    """
    class Meta:
        model = Booking
        fields = ['number_of_places', 'notes']
        widgets = {
            'number_of_places': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-2xl border border-slate-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition',
                'min': '1',
                'placeholder': 'Nombre de places'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-2xl border border-slate-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition',
                'rows': '4',
                'placeholder': 'Notes ou demandes particulières (optionnel)'
            }),
        }
    
    def __init__(self, *args, time_slot=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.time_slot = time_slot
        
        if time_slot:
            # Mettre à jour le max du champ number_of_places
            available = time_slot.available_capacity()
            self.fields['number_of_places'].widget.attrs['max'] = available
            self.fields['number_of_places'].help_text = f'{available} place(s) disponible(s)'
    
    def clean_number_of_places(self):
        number_of_places = self.cleaned_data.get('number_of_places')
        if self.time_slot and number_of_places:
            if not self.time_slot.is_available(number_of_places):
                raise forms.ValidationError(
                    f'Seulement {self.time_slot.available_capacity()} place(s) disponible(s).'
                )
        return number_of_places


class TimeSlotForm(forms.ModelForm):
    """
    Formulaire de création de créneau pour les établissements.
    """
    class Meta:
        model = TimeSlot
        fields = ['title', 'description', 'date', 'start_time', 'end_time', 'total_capacity', 'price_info', 'is_group_only']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-2xl border border-slate-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition',
                'placeholder': 'Ex: Matinée Coworking'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-2xl border border-slate-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition',
                'rows': '4',
                'placeholder': 'Décrivez le créneau...'
            }),
            'date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 rounded-2xl border border-slate-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition',
                'type': 'date'
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'w-full px-4 py-3 rounded-2xl border border-slate-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition',
                'type': 'time'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'w-full px-4 py-3 rounded-2xl border border-slate-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition',
                'type': 'time'
            }),
            'total_capacity': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-2xl border border-slate-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition',
                'min': '1',
                'placeholder': 'Nombre de places'
            }),
            'price_info': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-2xl border border-slate-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition',
                'placeholder': 'Ex: Gratuit, 10€, Consommation obligatoire'
            }),
            'is_group_only': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-indigo-600 border-slate-300 rounded focus:ring-indigo-500'
            }),
        }


class EstablishmentForm(forms.ModelForm):
    """
    Formulaire de création/modification d'établissement.
    """
    class Meta:
        model = Establishment
        fields = ['name', 'establishment_type', 'address', 'city', 'description', 'logo', 
                  'wifi_available', 'power_outlets', 'quiet_zone', 'free_coffee']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-2xl border border-slate-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition',
                'placeholder': 'Nom de l\'établissement'
            }),
            'establishment_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-2xl border border-slate-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition'
            }),
            'address': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-2xl border border-slate-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition',
                'placeholder': 'Adresse complète'
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-2xl border border-slate-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition',
                'placeholder': 'Ville'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-2xl border border-slate-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition',
                'rows': '4',
                'placeholder': 'Décrivez votre établissement...'
            }),
            'wifi_available': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-indigo-600 border-slate-300 rounded focus:ring-indigo-500'
            }),
            'power_outlets': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-indigo-600 border-slate-300 rounded focus:ring-indigo-500'
            }),
            'quiet_zone': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-indigo-600 border-slate-300 rounded focus:ring-indigo-500'
            }),
            'free_coffee': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-indigo-600 border-slate-300 rounded focus:ring-indigo-500'
            }),
        }
