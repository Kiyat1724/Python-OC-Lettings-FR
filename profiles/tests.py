"""Tests des pages et du modèle de profils."""

import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Profile


@pytest.mark.django_db
def test_profiles_index_displays_username(client):
    """La liste des profils affiche le nom de l'utilisateur."""
    user = User.objects.create_user(username='oc-profile-list')
    Profile.objects.create(
        user=user,
        favorite_city='Newport Beach',
    )

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


def test_profile_string_representation():
    """Un profil est représenté par le nom de son utilisateur."""
    user = User(username='roukiat-test')
    profile = Profile(
        user=user,
        favorite_city='Lyon',
    )

    assert str(profile) == 'roukiat-test'


@pytest.mark.django_db
def test_unknown_profile_returns_404(client):
    """Un profil inexistant renvoie une réponse 404."""
    url = reverse('profile', kwargs={'username': 'profil-inexistant'})

    response = client.get(url)

    assert response.status_code == 404
