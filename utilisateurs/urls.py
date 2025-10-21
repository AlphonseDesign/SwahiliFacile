# utilisateurs/urls.py
from django.urls import path
from . import views

app_name = 'utilisateurs'

urlpatterns = [
    path('inscription/', views.inscription_view, name='inscription'),
    path('connexion/', views.connexion_view, name='connexion'),
    path('deconnexion/', views.deconnexion_view, name='deconnexion'),
    path('profil/', views.profil_view, name='profil'), # Voir son propre profil
    path('profil/modifier/', views.profil_modifier_view, name='profil_modifier'), # Modifier son profil
    # Optionnel: voir le profil d'un autre utilisateur par son nom
    path('profil/<str:nom_utilisateur>/', views.public_profil_view, name='public_profil'), 
]
