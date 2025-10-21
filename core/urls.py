from django.urls import path
from . import views

app_name = 'core' # Important pour les templates

urlpatterns = [
    # Page d'accueil
    path('', views.home_view, name='home'),
    # Page Sponsor
    path('sponsoriser/', views.sponsor_view, name='sponsor'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/messages/', views.dashboard_messages_list_view, name='dashboard_messages_list'),
    path('dashboard/messages/<int:fil_id>/', views.dashboard_message_detail_view, name='dashboard_message_detail'),
]