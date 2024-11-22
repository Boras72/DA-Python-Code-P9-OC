"""
Ce module configure l'interface d'administration pour l'application Django.
Dépendances :
- django.contrib
- django.contrib.auth
- .models

Classes principales :
- CustomUserAdmin : Personnalisation de l'interface d'administration pour le modèle User.

Routes principales :
- /admin/ : Route pour accéder à l'interface d'administration.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    """
    Personnalisation de l'interface d'administration pour le modèle User.

    Attributs :
        list_display (tuple): Champs affichés dans la liste des utilisateurs.
        list_filter (tuple): Filtres disponibles dans la liste des utilisateurs.
        search_fields (tuple): Champs disponibles pour la recherche.
        ordering (tuple): Ordre de tri des utilisateurs.
        fieldsets (tuple): Organisation des champs dans le formulaire de modification.
        add_fieldsets (tuple): Organisation des champs dans le formulaire d'ajout.

    Exemple d'utilisation :
        admin.site.register(User, CustomUserAdmin)
    """
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "date_joined",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("-date_joined",)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Informations personnelles", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Dates importantes", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
