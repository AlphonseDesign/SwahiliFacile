from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.templatetags.static import static # Importez static

# ... (Votre UtilisateurPersoManager reste inchangé) ...
class UtilisateurPersoManager(BaseUserManager):
    def create_user(self, nom_utilisateur, numero_telephone, password=None, **extra_fields):
        if not nom_utilisateur:
            raise ValueError("Le nom d'utilisateur est obligatoire")
        if not numero_telephone:
            raise ValueError("Le numéro de téléphone est obligatoire")
        user = self.model(
            nom_utilisateur=nom_utilisateur.lower(),
            numero_telephone=numero_telephone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, nom_utilisateur, numero_telephone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le Superuser doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le Superuser doit avoir is_superuser=True.')
        return self.create_user(nom_utilisateur, numero_telephone, password, **extra_fields)


class UtilisateurPerso(AbstractBaseUser, PermissionsMixin):
    nom_utilisateur = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Nom d'utilisateur"
    )
    numero_telephone = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Numéro de téléphone"
    )
    photo_profil = models.ImageField(
        upload_to='profils/',
        null=True,
        blank=True,
        verbose_name="Photo de profil"
    )

    # *** NOUVEAUX CHAMPS AJOUTÉS ICI ***
    biographie = models.TextField(
        max_length=250, # Limite de 250 caractères
        blank=True, 
        null=True,
        verbose_name="Biographie"
    )
    lien_facebook = models.URLField(
        max_length=255, 
        blank=True, 
        null=True,
        verbose_name="Lien Facebook"
    )
    lien_whatsapp = models.CharField( # On utilise CharField pour les numéros WhatsApp
        max_length=20, 
        blank=True, 
        null=True,
        verbose_name="Numéro WhatsApp (ex: +243...)"
    )
    lien_instagram = models.URLField(
        max_length=255, 
        blank=True, 
        null=True,
        verbose_name="Lien Instagram"
    )
    # *** FIN DES NOUVEAUX CHAMPS ***

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_inscription = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'nom_utilisateur'
    REQUIRED_FIELDS = ['numero_telephone']

    objects = UtilisateurPersoManager()

    def __str__(self):
        return self.nom_utilisateur

    def get_photo_url(self):
        if self.photo_profil and hasattr(self.photo_profil, 'url'):
            return self.photo_profil.url
        else:
            # Assurez-vous d'avoir une image 'default_avatar.png' 
            # dans votre dossier 'static/images/'
            return static('images/default_avatar.png')