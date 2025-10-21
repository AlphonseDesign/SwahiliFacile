# core/context_processors.py
from publications.models import Publication

def slider_publications(request):
    """
    Récupère les 3 publications les plus récentes (ou épinglées) 
    qui possèdent une image pour les afficher dans le slider.
    """

    # On s'assure de prendre que les posts qui ont une image
    posts_pour_slider = Publication.objects.filter(
        image__isnull=False   # Doit avoir une image
    ).exclude(
        image=''              # Ne doit pas être une image vide
    ).order_by(
        '-epingle',           # Les épinglés en premier
        '-date_creation'      # Puis les plus récents
    )[:3]                     # On prend les 3 premiers

    return {
        'slider_publications': posts_pour_slider
    }