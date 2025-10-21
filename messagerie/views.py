# messagerie/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import FilDeDiscussion, Message

@login_required # Toutes les vues ici nécessitent une connexion
def inbox_view(request):
    """ Affiche la boîte de réception du visiteur connecté. """
    
    # On ne récupère que les fils où le visiteur est l'auteur
    fils_de_discussion = FilDeDiscussion.objects.filter(visiteur=request.user)
    
    context = {
        'fils_de_discussion': fils_de_discussion
    }
    return render(request, 'messagerie/inbox.html', context)

@login_required
def thread_detail_view(request, fil_id):
    """ Affiche un fil de discussion spécifique. """
    
    # Sécurité : On s'assure que le fil existe ET qu'il appartient à l'utilisateur
    fil = get_object_or_404(FilDeDiscussion, id=fil_id, visiteur=request.user)
    
    # Marquer le fil comme 'lu' par le visiteur
    if not fil.lu_par_visiteur:
        fil.lu_par_visiteur = True
        fil.save()

    # Logique pour la RÉPONSE du visiteur
    if request.method == 'POST':
        contenu = request.POST.get('contenu')
        if contenu:
            Message.objects.create(
                fil=fil,
                expediteur=request.user,
                contenu=contenu
            )
            # Mettre à jour le fil
            fil.lu_par_admin = False # Marquer comme 'non lu' pour l'admin
            fil.save() 
            messages.success(request, "Message envoyé !")
            return redirect('messagerie:thread_detail', fil_id=fil.id)

    messages_du_fil = fil.messages.all().order_by('envoye_le')
    
    context = {
        'fil': fil,
        'messages_du_fil': messages_du_fil
    }
    # On réutilise le template de chat de l'admin, il est générique !
    return render(request, 'messagerie/thread_detail.html', context)

@login_required
def new_thread_view(request):
    """ Permet au visiteur de démarrer une nouvelle conversation. """
    
    if request.method == 'POST':
        sujet = request.POST.get('sujet')
        contenu = request.POST.get('contenu')
        
        if not sujet or not contenu:
            messages.error(request, "Le sujet et le message sont obligatoires.")
            return render(request, 'messagerie/new_thread.html')

        # 1. Créer le fil de discussion
        # On le marque 'non lu' pour l'admin
        fil = FilDeDiscussion.objects.create(
            visiteur=request.user,
            sujet=sujet,
            lu_par_admin=False 
        )
        
        # 2. Créer le premier message
        Message.objects.create(
            fil=fil,
            expediteur=request.user,
            contenu=contenu
        )
        
        messages.success(request, "Votre message a été envoyé à l'administrateur.")
        return redirect('messagerie:inbox') # Redirige vers la boîte de réception

    return render(request, 'messagerie/new_thread.html')