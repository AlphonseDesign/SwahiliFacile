from django.shortcuts import render, get_object_or_404, redirect
from .models import Publication, Commentaire, Like
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings


def publication_detail_view(request, pk):
    publication = get_object_or_404(Publication, pk=pk)

    if request.method == 'POST' and request.user.is_authenticated:
        contenu_commentaire = request.POST.get('contenu')
        parent_id = request.POST.get('parent_id')
        parent_obj = None
        if parent_id:
            try:
                parent_obj = Commentaire.objects.get(id=parent_id)
            except Commentaire.DoesNotExist:
                parent_obj = None
                messages.error(request, "Le commentaire auquel vous essayez de répondre n'existe pas.")
        if contenu_commentaire:
            Commentaire.objects.create(
                publication=publication,
                auteur=request.user,
                contenu=contenu_commentaire,
                parent=parent_obj
            )
            messages.success(request, "Votre réponse a été ajoutée !" if parent_obj else "Votre commentaire a été ajouté !")
            return redirect('publications:detail', pk=publication.pk)

    if request.method == 'GET':
        session_key = f'viewed_publication_{publication.pk}'
        if not request.session.get(session_key, False):
            publication.vues = F('vues') + 1
            publication.save()
            publication.refresh_from_db()
            request.session[session_key] = True

    commentaires = publication.commentaires.filter(parent=None).order_by('date_creation')

    a_deja_like = False
    if request.user.is_authenticated:
        a_deja_like = Like.objects.filter(publication=publication, utilisateur=request.user).exists()

    og_url = request.build_absolute_uri(publication.get_absolute_url())
    og_title = publication.titre
    og_description = publication.get_description_apercu()
    og_image = request.build_absolute_uri(publication.image.url) if publication.image else request.build_absolute_uri(settings.STATIC_URL + 'images/logo_default.png')

    context = {
        'publication': publication,
        'commentaires': commentaires,
        'a_deja_like': a_deja_like,
        'og_url': og_url,
        'og_title': og_title,
        'og_description': og_description,
        'og_image': og_image,
    }
    return render(request, 'publications/detail.html', context)


@login_required
def like_publication_view(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    try:
        like_existant = Like.objects.get(publication=publication, utilisateur=request.user)
        like_existant.delete()
        messages.info(request, "Vous n'aimez plus cette publication.")
    except Like.DoesNotExist:
        Like.objects.create(publication=publication, utilisateur=request.user)
        messages.success(request, "Vous aimez cette publication ! ❤️")
    return redirect('publications:detail', pk=publication.pk)
