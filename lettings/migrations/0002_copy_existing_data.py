"""Copier les adresses et locations depuis l'application d'origine."""

from django.db import migrations


def copy_existing_data(apps, schema_editor):
    """Copier en lot en conservant les identifiants et les relations."""
    OldAddress = apps.get_model('oc_lettings_site', 'Address')
    OldLetting = apps.get_model('oc_lettings_site', 'Letting')
    NewAddress = apps.get_model('lettings', 'Address')
    NewLetting = apps.get_model('lettings', 'Letting')
    database = schema_editor.connection.alias

    addresses = [
        NewAddress(
            id=address.id,
            number=address.number,
            street=address.street,
            city=address.city,
            state=address.state,
            zip_code=address.zip_code,
            country_iso_code=address.country_iso_code,
        )
        for address in OldAddress.objects.using(database).all().iterator()
    ]

    NewAddress.objects.using(database).bulk_create(
        addresses,
        batch_size=100,
    )

    lettings = [
        NewLetting(
            id=letting.id,
            title=letting.title,
            address_id=letting.address_id,
        )
        for letting in OldLetting.objects.using(database).all().iterator()
    ]

    NewLetting.objects.using(database).bulk_create(
        lettings,
        batch_size=100,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('lettings', '0001_initial'),
        ('oc_lettings_site', '0002_auto_20261029_1655'),
    ]

    operations = [
        migrations.RunPython(copy_existing_data),
    ]
