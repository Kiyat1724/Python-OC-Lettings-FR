"""Modèles des adresses et des locations."""

from django.core.validators import MaxValueValidator, MinLengthValidator
from django.db import models


class Address(models.Model):
    """Représenter l'adresse d'une location."""

    number = models.PositiveIntegerField(validators=[MaxValueValidator(9999)])
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    zip_code = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
    country_iso_code = models.CharField(max_length=3, validators=[MinLengthValidator(3)])

    class Meta:
        """Définir le libellé au pluriel."""

        verbose_name_plural = 'Addresses'

    def __str__(self):
        """Retourner le numéro et le nom de la rue."""
        return f'{self.number} {self.street}'


class Letting(models.Model):
    """Représenter une location liée à une adresse."""

    title = models.CharField(max_length=256)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        """Retourner le titre de la location."""
        return self.title
