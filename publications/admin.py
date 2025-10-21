from django.contrib import admin
from .models import Publication, Commentaire, Like
from django.db.models import Count  # <-- L'importation correcte

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_publication', 'auteur', 'date_creation', 'epingle', 'vues', 'like_count', 'comment_count')
    list_filter = ('type_publication', 'epingle', 'date_creation') 
    search_fields = ('titre', 'contenu_texte')
    ordering = ('-epingle', '-date_creation')
    readonly_fields = ('auteur', 'vues')

    # Cette fonction doit être alignée (indentée) comme les autres
    def save_model(self, request, obj, form, change):
        if not getattr(obj, 'auteur', None):
            obj.auteur = request.user 
        super().save_model(request, obj, form, change)

    # Assurez-vous que cette ligne a la MÊME indentation
    # que 'def save_model' juste au-dessus.
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # On utilise Count (sans 'models.')
        queryset = queryset.annotate(
            _like_count=Count('likes', distinct=True),
            _comment_count=Count('commentaires', distinct=True)
        )
        return queryset

    # Assurez-vous que cette ligne a la MÊME indentation
    def like_count(self, obj):
        return obj._like_count
    like_count.admin_order_field = '_like_count'
    like_count.short_description = 'Likes'

    # Assurez-vous que cette ligne a la MÊME indentation
    def comment_count(self, obj):
        return obj._comment_count
    comment_count.admin_order_field = '_comment_count'
    comment_count.short_description = 'Commentaires'

# Les classes suivantes (CommentaireAdmin et LikeAdmin) ne changent pas
@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    # ... (votre code)
    list_display = ('auteur', 'publication', 'date_creation', 'parent')
    list_filter = ('date_creation',)
    search_fields = ('contenu', 'auteur__nom_utilisateur') # J'ai changé 'numero_telephone' en 'nom_utilisateur'

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    # ... (votre code)
    list_display = ('utilisateur', 'publication', 'date_creation')
    list_filter = ('date_creation',)
    search_fields = ('utilisateur__nom_utilisateur', 'publication__titre') # J'ai changé 'numero_telephone' en 'nom_utilisateur'