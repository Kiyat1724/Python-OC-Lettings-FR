"""Tests des listes et des fiches des locations."""

import pytest
from django.urls import reverse

from .models import Address, Letting


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
    letting = Letting.objects.create(
        title='Ocean View Test House',
        address=address,
    )

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
    letting = Letting.objects.create(
        title='Pacific View Test House',
        address=address,
    )

    url = reverse('letting', kwargs={'letting_id': letting.pk})
    response = client.get(url)

    assert response.status_code == 200
    html = response.content.decode()
    assert letting.title in html
    assert address.street in html
