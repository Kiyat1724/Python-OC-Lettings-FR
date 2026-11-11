"""Tests des pages d'erreur, des locations et des profils du site."""

from unittest.mock import patch

import pytest
from django.contrib.auth.models import User
from django.test import Client, override_settings
from django.urls import reverse

from lettings.models import Address, Letting
from profiles.models import Profile


@override_settings(DEBUG=False, ALLOWED_HOSTS=['testserver'])
def test_unknown_url_returns_custom_404():
    """Une URL inconnue affiche la page 404 personnalisée."""
    client = Client()

    response = client.get('/page-inconnue/')

    assert response.status_code == 404
    assert b'404 - Page not found' in response.content


@override_settings(DEBUG=False, ALLOWED_HOSTS=['testserver'])
def test_server_error_returns_custom_500():
    """Une erreur interne affiche la page 500 personnalisée."""
    client = Client(raise_request_exception=False)

    with patch(
        'oc_lettings_site.views.render',
        side_effect=RuntimeError('Simulated server error'),
    ):
        response = client.get(reverse('index'))

    assert response.status_code == 500
    assert b'500 - Server error' in response.content


@pytest.mark.django_db
def test_lettings_index_displays_the_list(client):
    """La liste des locations affiche le titre d'une location enregistrée."""
    address = Address.objects.create(
        number=12,
        street='Ocean Drive',
        city='Newport Beach',
        state='CA',
        zip_code=92660,
        country_iso_code='USA',
    )
    letting = Letting.objects.create(title='Ocean View Test House', address=address)

    response = client.get(reverse('lettings_index'))

    assert response.status_code == 200
    assert letting.title in response.content.decode()


@pytest.mark.django_db
def test_letting_detail_displays_title_and_address(client):
    """La fiche affiche le titre et la rue de la location demandée."""
    address = Address.objects.create(
        number=24,
        street='Pacific Coast Highway',
        city='Newport Beach',
        state='CA',
        zip_code=92660,
        country_iso_code='USA',
    )
    letting = Letting.objects.create(title='Pacific View Test House', address=address)

    url = reverse('letting', kwargs={'letting_id': letting.pk})
    response = client.get(url)

    assert response.status_code == 200
    html = response.content.decode()
    assert letting.title in html
    assert address.street in html


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
    profile = Profile.objects.create(user=user, favorite_city='Laguna Beach')

    url = reverse('profile', kwargs={'username': user.username})
    response = client.get(url)

    assert response.status_code == 200
    html = response.content.decode()
    assert user.username in html
    assert profile.favorite_city in html
