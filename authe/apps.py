"""
Ce module configure l'application d'authentification pour Django.
Dépendances :
- django.apps

Classes principales :
- AuthConfig : Configuration de l'application d'authentification.

Routes principales :
- Aucune route définie dans ce module.
"""
from django.apps import AppConfig


class AuthConfig(AppConfig):
    """
    Configuration de l'application d'authentification.

    Attributs :
        default_auto_field (str): Type de champ auto-incrémenté par défaut.
        name (str): Nom de l'application.

    Exemple d'utilisation :
        # Dans settings.py
        INSTALLED_APPS = [
            ...
            'authe.apps.AuthConfig',
            ...
        ]
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "authe"
