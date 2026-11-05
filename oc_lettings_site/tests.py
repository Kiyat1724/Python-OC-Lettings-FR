"""Tests des réponses et des pages d'erreur du site."""

from unittest.mock import patch

from django.test import Client, override_settings
from django.urls import reverse


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
