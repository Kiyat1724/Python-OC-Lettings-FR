"""Copier les profils depuis l'application d'origine."""

from django.db import migrations


def copy_existing_data(apps, schema_editor):
    """Copier en lot en conservant les utilisateurs et identifiants."""
    OldProfile = apps.get_model('oc_lettings_site', 'Profile')
    NewProfile = apps.get_model('profiles', 'Profile')
    database = schema_editor.connection.alias

    profiles = [
        NewProfile(
            id=profile.id,
            user_id=profile.user_id,
            favorite_city=profile.favorite_city,
        )
        for profile in OldProfile.objects.using(database).all().iterator()
    ]

    NewProfile.objects.using(database).bulk_create(
        profiles,
        batch_size=100,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
        ('oc_lettings_site', '0002_auto_20261029_1655'),
    ]

    operations = [
        migrations.RunPython(copy_existing_data),
    ]
