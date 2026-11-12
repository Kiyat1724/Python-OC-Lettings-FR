"""Vue de la page d'accueil du site."""

from django.shortcuts import render


def index(request):
    """Afficher la page d'accueil du site."""
    return render(request, 'index.html')
