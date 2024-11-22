"""
Module de configuration principale du projet Django BooksReview.

Dépendances:
- django.contrib
- django.middleware
- django.template
- django.auth
- django.messages
- pathlib

Configuration principale:
- Middleware
- Templates
- Base de données
- Fichiers statiques et médias
- Authentification
- Routes URL principales

Routes principales:
- / : Page d'accueil du site
- /admin/ : Interface d'administration
- /authe/ : Application d'authentification
- /func/ : Application principale 

Configuration des middlewares :
    - SessionMiddleware : Gestion des sessions
    - CommonMiddleware : Fonctionnalités communes
    - CsrfViewMiddleware : Protection CSRF
    - AuthenticationMiddleware : Authentification
    - MessageMiddleware : Messages flash
    - XFrameOptionsMiddleware : Protection clickjacking

Configuration des templates :
    - Backend : DjangoTemplates
    - Répertoires : templates/, authe/templates/, func/templates/
    - Options : debug, request, auth, messages

Configuration de la base de données :
    - Moteur : SQLite3
    - Nom : db.sqlite3
"""


from pathlib import Path
import os

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-@&oc)2$gj6tltxr(c45=i)on=-1%n5_@7jkd3!&*@q2ag=q8@b"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "authe",
    "func",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "BooksReview.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
            BASE_DIR / "authe" / "templates",
            BASE_DIR / "func" / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "BooksReview.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Configuration des fichiers statiques et médias
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Configuration du modèle utilisateur personnalisé
AUTH_USER_MODEL = "authe.User"

# Configuration des redirections après authentification
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "feed"
LOGOUT_REDIRECT_URL = "login"
# la racine du site ('/) redirige vers 'feed' si l'utilisateur est connecté ou 'login' si l'utilisateur n'est pas connecté
# redirections après login/signup réussis vers 'feed'
