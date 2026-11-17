"""Tests des listes et des fiches des profils."""

import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Profile


@pytest.mark.django_db
def test_profiles_index_displays_username(client):
    """La liste des profils affiche le nom de l'utilisateur."""
    user = User.objects.create_user(username='oc-profile-list')
    Profile.objects.create(user=user, favorite_city='Newport Beach')

    response = client.get(reverse('profiles_index'))

    assert response.status_code == 200
    assert user.username in response.content.decode()


@pytest.mark.django_db
def test_profile_detail_displays_username_and_city(client):
    """La fiche affiche le nom d'utilisateur et sa ville préférée."""
    user = User.objects.create_user(username='oc-profile-detail')
    profile = Profile.objects.create(
        user=user,
        favorite_city='Laguna Beach',
    )

    url = reverse('profile', kwargs={'username': user.username})
    response = client.get(url)

    assert response.status_code == 200
    html = response.content.decode()
    assert user.username in html
    assert profile.favorite_city in html
