# publications/models.py
from django.db import models
from django.conf import settings # Pour lier à notre UtilisateurPerso
from django.urls import reverse  # N'oubliez pas cet import

class Publication(models.Model):
    # Choix du type de post
    class TypePublication(models.TextChoices):
        TEXTE = 'TEXTE', 'Texte'
        PHOTO = 'PHOTO', 'Photo'
        VIDEO = 'VIDEO', 'Vidéo'
        LIEN = 'LIEN', 'Lien'

    type_publication = models.CharField(max_length=10, choices=TypePublication.choices, default=TypePublication.TEXTE)
    
    # Auteur (l'admin qui poste)
    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        limit_choices_to={'is_staff': True}
    )
    
    # Contenu
    titre = models.CharField(max_length=255, help_text="Titre de la publication")
    contenu_texte = models.TextField(blank=True, null=True, help_text="Contenu principal (si type TEXTE)")
    image = models.ImageField(upload_to='publications/images/', blank=True, null=True, help_text="Image (si type PHOTO)")
    video_url = models.URLField(blank=True, null=True, help_text="Lien YouTube, Vimeo, etc. (si type VIDEO)")
    lien_externe = models.URLField(blank=True, null=True, help_text="Lien du site (si type LIEN)")

    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True)
    epingle = models.BooleanField(default=False, help_text="Cocher pour garder en haut de la liste")
    vues = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-epingle', '-date_creation'] # Les épinglés d'abord, puis les plus récents

    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        """ Retourne l'URL unique pour cette publication. """
        return reverse('publications:detail', kwargs={'pk': self.pk})

    # Pour le partage (Open Graph)
    def get_description_apercu(self):
        """ Retourne une description courte pour les aperçus. """
        if self.contenu_texte:
            # Coupe proprement à 150 caractères
            if len(self.contenu_texte) > 150:
                return self.contenu_texte[:150] + '...'
            return self.contenu_texte
        # Description par défaut si pas de texte
        return "Découvrez cette publication et plus encore sur Swahili Facile."

    def get_image_apercu(self):
        if self.image:
            return self.image.url
        return None

    def get_embed_url(self):
        """ Convertit un lien YouTube/Vimeo en URL 'embed' pour iframe. """
        if not self.video_url:
            return None
        
        video_id = None
        # Cas YouTube: https://www.youtube.com/watch?v=VIDEO_ID
        if 'youtube.com/watch?v=' in self.video_url:
            video_id = self.video_url.split('v=')[-1].split('&')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        
        # Cas YouTube court: https://youtu.be/VIDEO_ID
        if 'youtu.be/' in self.video_url:
            video_id = self.video_url.split('/')[-1].split('?')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        
        # Cas Vimeo: https://vimeo.com/VIDEO_ID
        if 'vimeo.com/' in self.video_url:
            video_id = self.video_url.split('/')[-1].split('?')[0]
            return f'https://player.vimeo.com/video/{video_id}'

        # Si ce n'est pas un lien reconnu, on renvoie None
        return None

class Commentaire(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='commentaires')
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='reponses')

    class Meta:
        ordering = ['date_creation'] # Les plus anciens d'abord

    def __str__(self):
        return f"Commentaire de {self.auteur} sur {self.publication.titre}"

    def get_reponses(self):
        """ Récupère toutes les réponses (enfants) de ce commentaire. """
        return self.reponses.all().order_by('date_creation')

class Like(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='likes')
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        # La contrainte la plus importante : empêche le "multi-like"
        unique_together = ('publication', 'utilisateur')

    def __str__(self):
        return f"{self.utilisateur} aime {self.publication.titre}"