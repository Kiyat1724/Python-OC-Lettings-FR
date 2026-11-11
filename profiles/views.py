"""Vues des listes et des fiches de profils."""

from django.shortcuts import get_object_or_404, render

from .models import Profile


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
