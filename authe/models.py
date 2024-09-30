from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser): #classe user héritant de "abstractUser" 
    follows = models.ManyToManyField(
        'self',
        symmetrical=False,
        verbose_name='suit'
    )
    followed_by = models.ManyToManyField(
        'self',
        symmetrical=False,
        verbose_name='suivi par',
        related_name='followers'
    )
    groups = models.ManyToManyField(  
        'auth.Group',
        related_name='custom_user_groups',  # Add a custom related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Add a custom related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    