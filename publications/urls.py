# publications/urls.py
from django.urls import path
from . import views

app_name = 'publications' # Important pour les templates

urlpatterns = [
    # Le chemin pour voir une publication par son ID (pk = Primary Key)
    # ex: /publications/1/
    path('<int:pk>/', views.publication_detail_view, name='detail'),
    path('<int:pk>/like/', views.like_publication_view, name='like'),
]