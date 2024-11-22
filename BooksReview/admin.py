"""
Ce module configure l'interface d'administration pour l'application Django.
Dépendances :
- django.contrib
- django.contrib.auth
- .models

Classes principales :
- CustomUserAdmin : Personnalisation de l'interface d'administration pour le modèle User.
- TicketAdmin : Personnalisation de l'interface d'administration pour le modèle Ticket.
- ReviewAdmin : Personnalisation de l'interface d'administration pour le modèle Review.
- UserFollowsAdmin : Personnalisation de l'interface d'administration pour le modèle UserFollows.

Routes principales :
- /admin/ : Route pour accéder à l'interface d'administration.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from authe.models import User  # Importation du modèle User personnalisé
from func.models import Ticket, Review, UserFollows


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


# Enregistrez le modèle User personnalisé avec l'admin personnalisé
admin.site.register(User, CustomUserAdmin)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """
    Personnalisation de l'interface d'administration pour le modèle Ticket.

    Attributs :
        list_display (tuple): Champs affichés dans la liste des tickets.
        list_filter (tuple): Filtres disponibles dans la liste des tickets.
        search_fields (tuple): Champs disponibles pour la recherche.

    Exemple d'utilisation :
        admin.site.register(Ticket, TicketAdmin)
    """
    list_display = ("title", "user", "time_created")
    list_filter = ("user", "time_created")
    search_fields = ("title", "description", "user__username")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Personnalisation de l'interface d'administration pour le modèle Review.

    Attributs :
        list_display (tuple): Champs affichés dans la liste des critiques.
        list_filter (tuple): Filtres disponibles dans la liste des critiques.
        search_fields (tuple): Champs disponibles pour la recherche.

    Exemple d'utilisation :
        admin.site.register(Review, ReviewAdmin)
    """
    list_display = ("headline", "rating", "user", "ticket", "time_created")
    list_filter = ("rating", "user", "time_created")
    search_fields = ("headline", "body", "user__username", "ticket__title")


@admin.register(UserFollows)
class UserFollowsAdmin(admin.ModelAdmin):
    """
    Personnalisation de l'interface d'administration pour le modèle UserFollows.

    Attributs :
        list_display (tuple): Champs affichés dans la liste des abonnements.
        list_filter (tuple): Filtres disponibles dans la liste des abonnements.

    Exemple d'utilisation :
        admin.site.register(UserFollows, UserFollowsAdmin)
    """
    list_display = ("user", "followed_user")
    list_filter = ("user", "followed_user")
    search_fields = ("user__username", "followed_user__username")
