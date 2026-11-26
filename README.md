# Orange County Lettings

Application Django de consultation de locations et de profils utilisateurs.

Projet réalisé dans le cadre du parcours Développeur Python d’OpenClassrooms.

## Environnement validé

- Python 3.14.7, indiqué dans `.python-version`
- Django 6.1.3
- SQLite
- Docker Desktop avec conteneurs Linux
- GitHub Actions pour l’intégration continue

Les versions exactes des dépendances sont enregistrées dans
`requirements.txt`.

## Architecture

- `oc_lettings_site` : configuration du projet, accueil et pages d’erreur
- `lettings` : adresses et locations
- `profiles` : profils liés aux utilisateurs Django
- `templates` : templates HTML
- `static` : fichiers CSS, JavaScript, images et polices

## Installation locale

### Prérequis

- Git
- uv
- Un terminal PowerShell sous Windows, ou un shell sous Linux/macOS

### Récupérer le projet

```bash
git clone https://github.com/Kiyat1724/Python-OC-Lettings-FR.git
cd Python-OC-Lettings-FR
```

Les développements décrits ici sont actuellement sur la branche
`feat/docker` :

```bash
git switch feat/docker
```

### Créer l’environnement

```bash
uv venv --python 3.14.7 .venv-modern
```

Sous Windows PowerShell :

```powershell
.\.venv-modern\Scripts\Activate.ps1
```

Sous Linux/macOS :

```bash
source .venv-modern/bin/activate
```

Installer les dépendances :

```bash
uv pip install -r requirements.txt
```

Vérifier l’installation :

```bash
python --version
python -m django --version
uv pip check
```

### Configurer les variables d’environnement

Django exige une clé secrète fournie par `DJANGO_SECRET_KEY`.

Dans PowerShell, après activation de l’environnement virtuel :

```powershell
$env:DJANGO_SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(64))"
$env:DJANGO_DEBUG = "True"
$env:DJANGO_ALLOWED_HOSTS = "127.0.0.1,localhost"
```

Ces variables restent disponibles uniquement dans le terminal actuel.
Les redéfinir après ouverture d’un nouveau terminal. Générer une nouvelle
clé locale peut invalider les sessions existantes ; une reconnexion peut
être nécessaire.

Sous Linux/macOS :

```bash
export DJANGO_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(64))')"
export DJANGO_DEBUG=True
export DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
```

Sans `DJANGO_DEBUG`, le débogage est désactivé par défaut.
Un fichier `.env` n’est pas chargé automatiquement par cette configuration.

Pour le déploiement, fournir une clé distincte et persistante via la
configuration de l’hébergeur. Ne pas l’enregistrer dans Git.

Vérifier la configuration après avoir défini les variables :

```bash
python manage.py check
```

### Préparer la base de données

Avant de migrer une base contenant des données importantes, en conserver
une sauvegarde.

Examiner puis appliquer les migrations :

```bash
python manage.py migrate --plan
python manage.py migrate
```

Une base neuve ne contient pas automatiquement les données de démonstration.

Les migrations de copie transfèrent les données des anciennes tables
lorsqu’elles existent et contiennent des enregistrements.

### Démarrer le site

```bash
python manage.py runserver
```

Accès :

- Accueil : http://127.0.0.1:8000/
- Locations : http://127.0.0.1:8000/lettings/
- Profils : http://127.0.0.1:8000/profiles/
- Administration : http://127.0.0.1:8000/admin/

Sur une base neuve, créer un administrateur :

```bash
python manage.py createsuperuser
```

Sur une base existante, utiliser un compte administrateur connu.

## Migrations et conservation des données

La séparation des applications suit cet ordre :

1. Création des modèles et des tables de `lettings` et `profiles`.
2. Copie des données avec `RunPython` et `bulk_create`.
3. Suppression des anciens modèles et tables après les migrations de copie.

Les identifiants sont conservés. Les adresses sont copiées avant les
locations afin de préserver leurs relations. Les profils conservent leurs
liens avec les utilisateurs.

La nouvelle version des migrations de copie a été rejouée sur une copie
d’une sauvegarde antérieure à la refonte.

La comparaison avant/après a confirmé :

- 6 adresses identiques ;
- 6 locations identiques ;
- 4 profils identiques ;
- aucune relation invalide ;
- suppression des anciennes tables.

Les migrations de copie ne fournissent pas de fonction de retour arrière.
Ne pas tenter un retour à un état antérieur sans stratégie de restauration.

Le réglage `DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'` conserve
le type d’identifiant défini dans les migrations existantes.

## Tests et qualité

Exécuter les tests :

```bash
python -m pytest
```

Mesurer la couverture :

```bash
python -m pytest --cov --cov-report=term-missing
```

Vérifier le code :

```bash
python -m flake8
```

Vérifier la cohérence des modèles et des migrations sans créer de fichier :

```bash
python manage.py makemigrations --check --dry-run
```

### Derniers résultats validés

- 11 tests réussis
- 92 % de couverture des lignes dans le périmètre configuré
- Aucun signalement Flake8

Le fichier `.coveragerc` exclut les tests et les migrations du calcul.
Les points d’entrée ASGI et WSGI restent inclus.

Les tests couvrent notamment :

- les listes et les fiches de locations et de profils ;
- les représentations textuelles des modèles ;
- les ressources inexistantes ;
- les pages d’erreur 404 et 500.

La couverture mesure les lignes exécutées ; elle ne garantit pas que
tous les scénarios possibles sont vérifiés.

Les rapports de couverture ne sont pas versionnés.

## Docker : développement local

### Prérequis

Docker Desktop doit être démarré avec son moteur Linux.

Vérifier que les parties Client et Server répondent :

```bash
docker version
```

### Construire l’image

Depuis la racine du projet :

```bash
docker build -t oc-lettings:dev .
```

Le Dockerfile :

- utilise Python 3.14.7 ;
- installe les dépendances de `requirements.txt` ;
- copie le code du projet ;
- démarre Gunicorn sur `0.0.0.0:8000`.

Le fichier `.dockerignore` exclut notamment les environnements virtuels,
les fichiers de configuration locaux et les bases SQLite.

### Préparer une copie SQLite dédiée à Docker

Exemple pour Windows PowerShell, depuis la racine du projet.
Définir d’abord les variables de la section « Configurer les variables
d’environnement » dans ce même terminal.

La commande suivante crée `docker-local.sqlite3`. Elle refuse de remplacer
un fichier déjà présent :

```powershell
python -c "import sqlite3; from pathlib import Path; src = Path('oc-lettings-site.sqlite3').resolve(); dst = Path('docker-local.sqlite3').resolve(); assert src.is_file(), 'Base source introuvable'; assert not dst.exists(), 'Copie Docker deja presente : utiliser la copie existante ou choisir un autre nom'; source = sqlite3.connect(src.as_uri() + '?mode=ro', uri=True); target = sqlite3.connect(str(dst)); source.backup(target); target.close(); source.close(); print(dst)"
```

La source est ouverte en lecture seule. Le conteneur utilisera la copie.

### Créer et démarrer le conteneur

Si un conteneur nommé `oc-lettings-local` existe déjà, consulter la section
« Reprendre un conteneur existant ».

Pour une première création :

```powershell
$dockerDatabase = (Resolve-Path .\docker-local.sqlite3).Path
```

```powershell
docker run -d --name oc-lettings-local -p 127.0.0.1:8001:8000 -e DJANGO_SECRET_KEY -e DJANGO_DEBUG=True -e DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost --mount "type=bind,source=$dockerDatabase,target=/app/oc-lettings-site.sqlite3" oc-lettings:dev
```

Appliquer les migrations sur la copie montée :

```bash
docker exec oc-lettings-local python manage.py migrate --noinput
docker exec oc-lettings-local python manage.py migrate --check
```

Consulter les messages :

```bash
docker logs --tail 50 oc-lettings-local
```

Ouvrir http://127.0.0.1:8001/.

Le port 8001 de l’ordinateur est relié au port 8000 du conteneur.
Le service est publié uniquement sur l’interface locale.

### Reprendre un conteneur existant

```bash
docker ps -a
docker start oc-lettings-local
```

Arrêter le conteneur :

```bash
docker stop oc-lettings-local
```

`docker start` conserve le montage, les variables et l’image définis lors
de la création. Il ne récupère pas les nouvelles variables du terminal
et ne remplace pas la base montée par un autre fichier. Un conteneur
antérieur à la configuration par variables doit être recréé pour
utiliser la nouvelle image et ces paramètres.

Les données de la copie SQLite restent sur l’ordinateur après l’arrêt
ou la suppression du conteneur.

### Vérifier l’image sans monter de base locale

```bash
docker run --rm -e DJANGO_SECRET_KEY -e DJANGO_DEBUG=False -e DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,testserver oc-lettings:dev python manage.py check
docker run --rm -e DJANGO_SECRET_KEY -e DJANGO_DEBUG=False -e DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,testserver oc-lettings:dev python -m pytest --cov --cov-report=term-missing
```

Les tests utilisent leur propre base temporaire.

Après une modification du code ou de la configuration des tests,
reconstruire l’image pour y intégrer les nouveaux fichiers.

Reconstruire une image ne met pas à jour un conteneur déjà créé.

### Limites actuelles

Cette section décrit les essais locaux avec Docker.
Le conteneur utilise Gunicorn et WhiteNoise. La commande locale active
le débogage ; la procédure ci-dessous permet de vérifier le fonctionnement
avec `DEBUG=False`.

## Exécution locale avec Gunicorn et WhiteNoise

Le Dockerfile démarre désormais Gunicorn à la place de `runserver`.

WhiteNoise sert les fichiers statiques regroupés pendant la construction
avec `collectstatic`, y compris lorsque `DEBUG=False`.

Le nom d’un tag Docker ne change pas le comportement du Dockerfile :
une image reconstruite avec le tag `dev` utilisera également Gunicorn.

### Construire l’image

```powershell
docker build -t oc-lettings:prod .
```

La collecte utilise une clé factice limitée à la commande de construction.
Une clé d’exécution doit toujours être fournie au démarrage du conteneur.

### Créer un conteneur de vérification

Définir les variables d’environnement dans le terminal comme indiqué
dans la section d’installation locale.

Utiliser la copie SQLite dédiée, après avoir arrêté tout autre
conteneur qui l’utiliserait :

```powershell
$dockerDatabase = (Resolve-Path .\docker-local.sqlite3).Path
```

Pour une première création du conteneur :

```powershell
docker run -d --name oc-lettings-prod-check -p 127.0.0.1:8003:8000 -e DJANGO_SECRET_KEY -e DJANGO_DEBUG=False -e DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost --mount "type=bind,source=$dockerDatabase,target=/app/oc-lettings-site.sqlite3" oc-lettings:prod
```

Si ce conteneur existe déjà, utiliser `docker start` pour le reprendre
avec sa configuration initiale, plutôt que relancer `docker run`.

Vérifier les migrations :

```powershell
docker exec oc-lettings-prod-check python manage.py migrate --noinput
docker exec oc-lettings-prod-check python manage.py migrate --check
```

### Vérifier le fonctionnement

```powershell
docker logs --tail 30 oc-lettings-prod-check
curl.exe -I http://127.0.0.1:8003/
curl.exe -I http://127.0.0.1:8003/static/css/styles.css
```

Ouvrir http://127.0.0.1:8003/ et vérifier les pages, le style et
l’administration.

### État de préparation au déploiement

Gunicorn et WhiteNoise sont configurés et testés localement.
Le déploiement public, HTTPS, les secrets persistants et le stockage
durable doivent encore être configurés sur l’hébergement retenu.

## Surveillance avec Sentry

L’application utilise le SDK Sentry avec les intégrations Django et logging.

La surveillance est activée uniquement si la variable `SENTRY_DSN`
est renseignée. Sans DSN, aucun envoi Sentry n’est initialisé.

### Activer Sentry en local

Dans PowerShell, après avoir configuré les variables Django :

```powershell
$env:SENTRY_DSN = Read-Host "Collez votre DSN Sentry"
$env:SENTRY_ENVIRONMENT = "development"
```

Saisir le DSN complet à l’invite, puis appuyer sur Entrée.
Ne pas enregistrer sa valeur dans le code.

Le logger `oc_lettings` et ses enfants transmettent les messages de
niveau INFO ou supérieur. Les messages ERROR peuvent également créer
des événements dans Issues.

Les vues enregistrent un avertissement lorsqu’une location ou un profil
demandé est introuvable, puis conservent la réponse HTTP 404.

La collecte automatique des informations utilisateur, corps de requêtes,
cookies, en-têtes, paramètres de requête et variables locales est limitée
par la configuration `data_collection`.

### Vérifications réalisées

- Réception d’une exception RuntimeError de démonstration dans Issues.
- Réception d’un message INFO dans Logs.
- Réception des avertissements des vues pour les ressources introuvables.
- Réussite des 11 tests après intégration.

### Tests ordinaires sans transmission à Sentry

Dans PowerShell, retirer temporairement le DSN avant les tests :

```powershell
Remove-Item Env:SENTRY_DSN -ErrorAction SilentlyContinue
python -m pytest --cov --cov-report=term-missing --cov-fail-under=80
```

Pour réactiver Sentry, saisir à nouveau le DSN avec Read-Host.

La CI ne fournit pas de DSN et ne transmet donc pas les erreurs simulées
par les tests.

### Exécution dans Docker

Les variables du terminal ne sont pas transmises automatiquement au
conteneur. Pour activer Sentry, ajouter à la commande docker run :

```text
-e SENTRY_DSN -e SENTRY_ENVIRONMENT
```

Ces variables doivent être définies dans le terminal avant la création
du conteneur. Redémarrer un ancien conteneur ne change pas ses variables.

L’activation sur l’hébergement sera vérifiée lors du déploiement.

## Image publiée sur Docker Hub

Dépôt public : https://hub.docker.com/r/rouksaid/oc-lettings

Image vérifiée :

```text
rouksaid/oc-lettings:5ab62ae
```

Le tag `5ab62ae` identifie le commit utilisé pour construire cette image.

### Télécharger l’image

```powershell
docker pull rouksaid/oc-lettings:5ab62ae
```

### Exécuter l’image téléchargée

Définir d’abord `DJANGO_SECRET_KEY` dans le terminal comme indiqué
dans la section de configuration.

Préparer la copie `docker-local.sqlite3` avec la procédure précédente
et arrêter tout autre conteneur utilisant cette copie.

```powershell
$dockerDatabase = (Resolve-Path .\docker-local.sqlite3).Path
```

Pour une première création :

```powershell
docker run -d --name oc-lettings-hub-check -p 127.0.0.1:8004:8000 -e DJANGO_SECRET_KEY -e DJANGO_DEBUG=False -e DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost -e SENTRY_DSN= --mount "type=bind,source=$dockerDatabase,target=/app/oc-lettings-site.sqlite3" rouksaid/oc-lettings:5ab62ae
```

Sentry est désactivé pour ce contrôle.

Si la copie nécessite des migrations :

```powershell
docker exec oc-lettings-hub-check python manage.py migrate --noinput
```

Ouvrir http://127.0.0.1:8004/.

Pour reprendre ce même conteneur après un arrêt :

```powershell
docker start oc-lettings-hub-check
```

### Vérifications effectuées

- Téléchargement de l’image depuis Docker Hub.
- Vérification de la configuration Django.
- Réponse HTTP 200 pour l’accueil.
- Réponse HTTP 200 et type text/css pour la feuille de style.

L’image ne contient pas la base SQLite. Les données sont fournies
séparément par montage.

## Intégration continue

Le workflow `.github/workflows/ci.yml` s’exécute sur les push et les
pull requests.

Il effectue les étapes suivantes :

1. Récupération du code.
2. Installation de Python à partir de `.python-version`.
3. Installation des dépendances.
4. Vérification de leur compatibilité.
5. Vérification de la configuration Django.
6. Vérification des changements de modèles non migrés.
7. Analyse Flake8.
8. Tests avec une couverture minimale de 80 %.
9. Construction de l’image Docker.

Une étape en échec fait échouer le job.

Cette pipeline vérifie le projet ; elle ne publie pas encore d’image et
ne déploie pas l’application.

Consulter les exécutions :

https://github.com/Kiyat1724/Python-OC-Lettings-FR/actions

## Consulter les données

Tables métier actuelles :

- `lettings_address`
- `lettings_letting`
- `profiles_profile`

Si la commande SQLite est installée :

```bash
sqlite3 oc-lettings-site.sqlite3
```

Puis, dans SQLite :

```sql
.tables
PRAGMA table_info(profiles_profile);
SELECT user_id, favorite_city FROM profiles_profile;
.quit
```
