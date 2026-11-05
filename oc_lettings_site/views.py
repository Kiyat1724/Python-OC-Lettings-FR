"""Vues des pages d'accueil, des locations et des profils."""

from django.shortcuts import get_object_or_404, render

from .models import Letting, Profile


def index(request):
    """Afficher la page d'accueil du site."""
    return render(request, 'index.html')


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


def profiles_index(request):
    """Afficher la liste de tous les profils."""
    profiles_list = Profile.objects.all()
    context = {'profiles_list': profiles_list}
    return render(request, 'profiles_index.html', context)


def profile(request, username):
    """Afficher un profil ou renvoyer une 404 s'il n'existe pas."""
    profile = get_object_or_404(Profile, user__username=username)
    context = {'profile': profile}
    return render(request, 'profile.html', context)
