"""Préparer Django et démarrer Gunicorn dans le conteneur."""

import os
import subprocess
import sys


def main():
    """Appliquer les migrations, collecter les fichiers et lancer le serveur."""
    subprocess.run(
        [sys.executable, 'manage.py', 'migrate', '--noinput'],
        check=True,
    )

    subprocess.run(
        [sys.executable, 'manage.py', 'collectstatic', '--noinput'],
        check=True,
    )

    port = os.environ.get('PORT', '8000')

    os.execvp(
        'gunicorn',
        [
            'gunicorn',
            'oc_lettings_site.wsgi:application',
            '--bind',
            f'0.0.0.0:{port}',
            '--access-logfile',
            '-',
            '--error-logfile',
            '-',
        ],
    )


if __name__ == '__main__':
    main()
