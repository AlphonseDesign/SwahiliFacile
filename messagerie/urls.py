# messagerie/urls.py
from django.urls import path
from . import views

app_name = 'messagerie'

urlpatterns = [
    # ex: /messages/ -> Boîte de réception du visiteur
    path('', views.inbox_view, name='inbox'),
    # ex: /messages/nouveau/ -> Écrire un nouveau message à l'admin
    path('nouveau/', views.new_thread_view, name='new_thread'),
    # ex: /messages/5/ -> Voir une discussion spécifique
    path('<int:fil_id>/', views.thread_detail_view, name='thread_detail'),
]