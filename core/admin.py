from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Establishment, TimeSlot, Booking


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'user_type', 'company_name', 'phone']
    list_filter = ['user_type', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {'fields': ('user_type', 'phone', 'company_name', 'avatar')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {'fields': ('user_type', 'phone', 'company_name', 'avatar')}),
    )


@admin.register(Establishment)
class EstablishmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'establishment_type', 'city', 'owner']
    list_filter = ['establishment_type', 'city', 'wifi_available', 'power_outlets']
    search_fields = ['name', 'city', 'address']


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['title', 'establishment', 'date', 'start_time', 'end_time', 'total_capacity', 'available_places']
    list_filter = ['date', 'is_group_only', 'establishment']
    search_fields = ['title', 'establishment__name']
    
    def available_places(self, obj):
        return obj.available_capacity()
    available_places.short_description = 'Places disponibles'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'time_slot', 'number_of_places', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'time_slot__title']
