"""Vues des listes et des fiches de profils."""

import logging

from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Profile


logger = logging.getLogger('oc_lettings.profiles')


def profiles_index(request):
    """Afficher la liste de tous les profils."""
    profiles_list = Profile.objects.all()
    context = {'profiles_list': profiles_list}
    return render(request, 'profiles_index.html', context)


def profile(request, username):
    """Afficher un profil ou renvoyer une 404 s'il n'existe pas."""
    try:
        profile = get_object_or_404(Profile, user__username=username)
    except Http404:
        logger.warning('Profil demande introuvable.')
        raise

    context = {'profile': profile}
    return render(request, 'profile.html', context)
