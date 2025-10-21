from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model # Importer get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required # Importer login_required
from .forms import InscriptionForm, ConnexionForm, ProfilUpdateForm # Importer ProfilUpdateForm

User = get_user_model() # Récupérer le modèle utilisateur

@login_required # Il faut être connecté pour voir son profil
def profil_view(request):
    """ Affiche le profil de l'utilisateur connecté. """
    user = request.user # L'utilisateur connecté
    context = {'user_profile': user} # On passe l'utilisateur au template
    return render(request, 'utilisateurs/profil_detail.html', context)

@login_required
def profil_modifier_view(request):
    """ Permet à l'utilisateur de modifier sa photo de profil. """
    user = request.user
    if request.method == 'POST':
        # On passe 'instance=user' pour modifier l'objet existant
        # On passe request.FILES pour gérer l'upload
        form = ProfilUpdateForm(request.POST, request.FILES, instance=user) 
        if form.is_valid():
            form.save()
            messages.success(request, "Votre photo de profil a été mise à jour !")
            return redirect('utilisateurs:profil') # Redirige vers la page de profil
        else:
             messages.error(request, "Erreur lors de la mise à jour.")
    else: # Si c'est GET, on affiche le formulaire pré-rempli
        form = ProfilUpdateForm(instance=user)
        
    context = {'form': form}
    return render(request, 'utilisateurs/profil_modifier.html', context)

def public_profil_view(request, nom_utilisateur):
    """ Affiche le profil public d'un utilisateur par son nom. """
    # On cherche l'utilisateur ou renvoie une erreur 404
    user_profile = get_object_or_404(User, nom_utilisateur=nom_utilisateur) 
    context = {'user_profile': user_profile}
    # On réutilise le même template que pour le profil personnel
    return render(request, 'utilisateurs/profil_detail.html', context)

def inscription_view(request):
    """ Gère l'inscription des utilisateurs. """
    # Si l'utilisateur est déjà connecté, on le redirige
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save() # Sauvegarde l'utilisateur (mot de passe haché)
            login(request, user) # Connecte l'utilisateur
            messages.success(request, f"Inscription réussie ! Bienvenue, {user.nom_utilisateur}.")
            return redirect('core:home')
        else:
            # Si le formulaire n'est pas valide (ex: mdp != 4 chars), on affiche les erreurs
            messages.error(request, "Erreur dans le formulaire. Veuillez corriger.")
    else:
        form = InscriptionForm()
    
    return render(request, 'utilisateurs/inscription.html', {'form': form})


def connexion_view(request):
    """ Gère la connexion des utilisateurs. """
    if request.user.is_authenticated:
        return redirect('core:home')
        
    if request.method == 'POST':
        # *** CORRECTION ICI ***
        form = ConnexionForm(request.POST) # On passe juste request.POST
        # *** FIN CORRECTION ***

        if form.is_valid():
            username = form.cleaned_data.get('nom_utilisateur') # Utilise nom_utilisateur
            password = form.cleaned_data.get('password')
            # authenticate utilise 'username' même si notre champ s'appelle nom_utilisateur
            user = authenticate(request, username=username, password=password) 
            
            if user is not None:
                login(request, user)
                messages.info(request, f"Heureux de vous revoir, {user.nom_utilisateur} !")
                next_page = request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('core:home')
            else:
                messages.warning(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            # Afficher les erreurs du formulaire s'il n'est pas valide (rare pour la connexion)
             messages.warning(request, "Veuillez corriger les erreurs ci-dessous.")
    else: # Si c'est une requête GET (affichage initial de la page)
        form = ConnexionForm()

    return render(request, 'utilisateurs/connexion.html', {'form': form})

def deconnexion_view(request):
    """ Déconnecte l'utilisateur. """
    logout(request)
    messages.info(request, "Vous avez été déconnecté. À bientôt !")
    return redirect('core:home')