# messagerie/admin.py
from django.contrib import admin
from .models import FilDeDiscussion, Message

class MessageInline(admin.TabularInline):
    """ Affiche les messages DANS la vue du FilDeDiscussion """
    model = Message
    fields = ('expediteur', 'contenu', 'envoye_le')
    readonly_fields = ('expediteur', 'contenu', 'envoye_le')
    extra = 0 # N'affiche pas de champs vides en plus

@admin.register(FilDeDiscussion)
class FilDeDiscussionAdmin(admin.ModelAdmin):
    list_display = ('visiteur', 'sujet', 'dernier_message', 'lu_par_admin', 'lu_par_visiteur')
    list_filter = ('lu_par_admin', 'lu_par_visiteur', 'dernier_message')
    search_fields = ('visiteur__nom_utilisateur', 'sujet')
    inlines = [MessageInline] # Affiche les messages liés

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('expediteur', 'fil', 'envoye_le')
    search_fields = ('expediteur__nom_utilisateur', 'contenu')