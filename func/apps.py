"""
Ce module configure l'application fonctionnelle du projet Django.

Dépendances:
- django.apps

Classes principales:
- FuncConfig: Configuration de l'application fonctionnelle

Routes principales:
- Aucune route définie dans ce module
"""
from django.apps import AppConfig


class FuncConfig(AppConfig):
    """
    Configuration de l'application fonctionnelle.

    Attributes:
        default_auto_field (str): Type de champ auto-incrémenté par défaut
        name (str): Nom de l'application

    Example:
        # Dans settings.py
        INSTALLED_APPS = [
            ...
            'func.apps.FuncConfig',
            ...
        ]
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "func"
