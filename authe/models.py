"""
Ce module définit les modèles de données pour l'application Django.
Dépendances :
- django.contrib.auth.models
- django.db

Classes principales :
- User : Modèle utilisateur personnalisé qui étend AbstractUser.

Routes principales :
- Aucune route définie dans ce module.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé qui étend AbstractUser.

    Attributs :
        email (EmailField): Champ email optionnel.

    Méthodes :
        __str__ : Retourne le nom d'utilisateur.

    Exemple d'utilisation :
        user = User.objects.create_user(username="john", email="john@example.com", password="password123")
    """
    email = models.EmailField(blank=True)  # champs 'email' optionnel avec (blank=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        """
        Retourne le nom d'utilisateur.

        Returns:
            str: Le nom d'utilisateur.
        """
        return self.username
