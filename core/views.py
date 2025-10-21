# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from publications.models import Publication
from messagerie.models import FilDeDiscussion, Message # <-- AJOUTER
from django.contrib.auth.decorators import login_required, user_passes_test # <-- AJOUTER
from django.contrib import messages # <-- AJOUTER

# --- Vues existantes ---
def home_view(request):
    # On récupère toutes les publications, l'ordre est déjà défini dans le Meta du modèle
    publications = Publication.objects.all()

    context = {
        'publications': publications
    }
    return render(request, 'core/home.html', context)

def sponsor_view(request):
    # C'est une page simple, pas besoin de contexte pour l'instant
    return render(request, 'core/sponsor.html')


#
# CORRECTION : Définir la fonction 'est_admin' AVANT de l'utiliser.
#
def est_admin(user):
    """ Teste si l'utilisateur est un admin (staff). """
    return user.is_authenticated and user.is_staff
#
# FIN DE LA CORRECTION
#


@user_passes_test(est_admin) # Sécurise la vue, redirige si pas admin
def dashboard_view(request):
    """ Page d'accueil du tableau de bord. """
    # On peut ajouter des stats ici plus tard
    fils_non_lus = FilDeDiscussion.objects.filter(lu_par_admin=False).count()
    context = {
        'fils_non_lus': fils_non_lus
    }
    return render(request, 'core/dashboard.html', context)

@user_passes_test(est_admin)
def dashboard_messages_list_view(request):
    """ Affiche tous les fils de discussion. """
    tous_les_fils = FilDeDiscussion.objects.all().order_by('-dernier_message')
    context = {
        'fils_de_discussion': tous_les_fils
    }
    return render(request, 'core/dashboard_messages_list.html', context)

@user_passes_test(est_admin)
def dashboard_message_detail_view(request, fil_id):
    """ Affiche un fil spécifique et permet à l'admin de répondre (texte OU image). """
    fil = get_object_or_404(FilDeDiscussion, id=fil_id)
    
    if not fil.lu_par_admin:
        fil.lu_par_admin = True
        fil.save()

    if request.method == 'POST':
        contenu = request.POST.get('contenu', '') # Récupère le texte, '' par défaut
        image_file = request.FILES.get('image_upload') # Récupère le fichier image

        # Vérifier si au moins l'un des deux (texte ou image) est fourni
        if contenu or image_file:
            # Créer le message en incluant l'image si elle existe
            Message.objects.create(
                fil=fil,
                expediteur=request.user,
                contenu=contenu,
                image=image_file # Sera None si aucun fichier n'est uploadé
            )
            
            fil.lu_par_visiteur = False 
            fil.save() 
            
            messages.success(request, "Réponse envoyée !")
            # Important : rediriger pour éviter le double POST et recharger la page
            return redirect('core:dashboard_message_detail', fil_id=fil.id)
        else:
            # Si ni texte ni image n'ont été envoyés
            messages.warning(request, "Veuillez écrire un message ou joindre une image.")


    messages_du_fil = fil.messages.all().order_by('envoye_le')
    
    context = {
        'fil': fil,
        'messages_du_fil': messages_du_fil
    }
    return render(request, 'core/dashboard_message_detail.html', context)