# utilisateurs/forms.py
from django import forms
# On n'importe PLUS UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class InscriptionForm(forms.ModelForm): # <<< CHANGEMENT ICI
    
    # On garde les définitions pour les widgets et labels personnalisés
    nom_utilisateur = forms.CharField(
        max_length=150, 
        required=True, 
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    numero_telephone = forms.CharField(
        max_length=20, 
        required=True, 
        label="Numéro de téléphone"
    )
    password = forms.CharField(
        label="Mot de passe", 
        widget=forms.PasswordInput 
    )
    password2 = forms.CharField(
        label="Confirmer le mot de passe", 
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        # On liste TOUS les champs nécessaires pour créer l'utilisateur
        # y compris 'password', mais PAS 'password2' car il n'est pas dans le modèle User
        fields = ('nom_utilisateur', 'numero_telephone', 'password') 

    # Vérification de confirmation (inchangée)
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            self.add_error('password2', "Les deux mots de passe ne correspondent pas.")
            
        return cleaned_data

    # AJOUT : Méthode save pour hacher le mot de passe
    def save(self, commit=True):
        # On récupère l'instance utilisateur mais on ne la sauvegarde pas encore (commit=False)
        user = super().save(commit=False)
        
        # On hache le mot de passe récupéré du formulaire
        password = self.cleaned_data.get("password")
        user.set_password(password) # set_password gère le hachage sécurisé
        
        # On sauvegarde l'utilisateur si commit=True
        if commit:
            user.save()
            
        return user

# --- ConnexionForm (inchangé) ---
class ConnexionForm(forms.Form):
    nom_utilisateur = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput
    )

class ProfilUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        # Ajout des nouveaux champs
        fields = [
            'photo_profil', 
            'biographie', 
            'lien_facebook',
            'lien_whatsapp',
            'lien_instagram'
        ]
        widgets = {
            'photo_profil': forms.FileInput(attrs={'accept': 'image/*'}),
            'biographie': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Parlez un peu de vous...'}),
            'lien_facebook': forms.URLInput(attrs={'placeholder': 'https://facebook.com/votrepage'}),
            'lien_whatsapp': forms.TextInput(attrs={'placeholder': '+243...'}),
            'lien_instagram': forms.URLInput(attrs={'placeholder': 'https://instagram.com/votrecompte'}),
        }