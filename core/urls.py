from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Page d'accueil et créneaux
    path('', views.index, name='index'),
    path('timeslot/<int:pk>/', views.timeslot_detail, name='timeslot_detail'),
    path('timeslot/<int:pk>/book/', views.book_timeslot, name='book_timeslot'),
    
    # Réservations
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:pk>/cancel/', views.cancel_booking, name='cancel_booking'),
    
    # Authentification
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Dashboard établissement
    path('establishment/dashboard/', views.establishment_dashboard, name='establishment_dashboard'),
    path('establishment/create/', views.create_establishment, name='create_establishment'),
    path('timeslot/create/', views.create_timeslot, name='create_timeslot'),
    
    # Landing
    path('landing/', views.landing, name='landing'),
]
