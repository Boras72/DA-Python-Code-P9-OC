from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser): # Modèle User de Django qui hérite de AbstractUser (modèle User personnalisé = CustomUser)
    # Ajout de champs supplémentaires si nécessaire
    email = models.EmailField(blank=True)  # champs 'email' optionnel avec (blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
