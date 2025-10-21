from django.contrib import admin
from .models import UtilisateurPerso
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

@admin.register(UtilisateurPerso)
class UtilisateurPersoAdmin(UserAdmin):
    model = UtilisateurPerso
    
    list_display = ('nom_utilisateur', 'numero_telephone', 'is_staff', 'is_active', 'photo_profil_display')
    search_fields = ('nom_utilisateur', 'numero_telephone',)
    ordering = ('-date_inscription',)
    
    readonly_fields = ('last_login', 'date_inscription') 

    fieldsets = (
        (None, {'fields': ('nom_utilisateur', 'password')}),
        ('Informations Personnelles', {'fields': ('numero_telephone', 'photo_profil')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nom_utilisateur', 'numero_telephone', 'photo_profil', 'password', 'password2'),
        }),
    )

    def photo_profil_display(self, obj):
        if obj.photo_profil and hasattr(obj.photo_profil, 'url'):
            return format_html('<img src="{}" width="40" height="40" style="border-radius: 50%; object-fit: cover;" />', obj.photo_profil.url)
        return "Pas de photo"
    photo_profil_display.short_description = 'Photo'