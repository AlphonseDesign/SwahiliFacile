# messagerie/models.py
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

# ... (FilDeDiscussion model remains the same) ...
class FilDeDiscussion(models.Model):
    visiteur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='fils_de_discussion',
        limit_choices_to={'is_staff': False}
    )
    sujet = models.CharField(max_length=255, default="Contact (pas de sujet)")
    cree_le = models.DateTimeField(auto_now_add=True)
    dernier_message = models.DateTimeField(auto_now=True)
    lu_par_admin = models.BooleanField(default=False)
    lu_par_visiteur = models.BooleanField(default=True)

    class Meta:
        ordering = ['-dernier_message']

    def __str__(self):
        return f"Discussion entre {self.visiteur.nom_utilisateur} et Admin"


class Message(models.Model):
    """ Un message unique dans un fil de discussion. """
    fil = models.ForeignKey(
        FilDeDiscussion,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    expediteur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='messages_envoyes'
    )
    contenu = models.TextField(blank=True, null=True) # <-- Autoriser le texte à être vide si image
    
    # AJOUT DU CHAMP IMAGE
    image = models.ImageField(
        upload_to='messagerie/images/', # Chemin dans MEDIA_ROOT
        blank=True,                     # L'image est optionnelle
        null=True                       # Optionnelle en BDD
    )
    
    envoye_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['envoye_le']

    def __str__(self):
        if self.contenu:
            return f"Message texte de {self.expediteur.nom_utilisateur}"
        elif self.image:
            return f"Image de {self.expediteur.nom_utilisateur}"
        return f"Message vide de {self.expediteur.nom_utilisateur}" # Cas improbable