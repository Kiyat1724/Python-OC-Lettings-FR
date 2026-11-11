"""Vues des listes et des fiches de locations."""

from django.shortcuts import get_object_or_404, render

from .models import Letting


def lettings_index(request):
    """Afficher la liste de toutes les locations."""
    lettings_list = Letting.objects.all()
    context = {'lettings_list': lettings_list}
    return render(request, 'lettings_index.html', context)


def letting(request, letting_id):
    """Afficher une location ou renvoyer une 404 si elle n'existe pas."""
    letting = get_object_or_404(Letting, id=letting_id)
    context = {
        'title': letting.title,
        'address': letting.address,
    }
    return render(request, 'letting.html', context)
