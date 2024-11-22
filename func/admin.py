"""
Ce module configure l'interface d'administration pour les modèles de l'application fonctionnelle.

Dépendances:
- django.contrib.admin
- .models

Classes principales:
- TicketAdmin: Configuration de l'administration des tickets
- ReviewAdmin: Configuration de l'administration des critiques
- UserFollowsAdmin: Configuration de l'administration des abonnements

Routes principales:
- /admin/func/ticket/: Administration des tickets
- /admin/func/review/: Administration des critiques  
- /admin/func/userfollows/: Administration des abonnements
"""

from django.contrib import admin
from .models import Ticket, Review, UserFollows


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour le modèle Ticket.

    Attributs:
        list_display (tuple): Colonnes affichées dans la liste des tickets
        list_filter (tuple): Filtres disponibles dans la liste
        search_fields (tuple): Champs utilisés pour la recherche

    Exemple d'utilisation:
        @admin.register(Ticket)
        class TicketAdmin(admin.ModelAdmin):
    """
    list_display = ("title", "user", "time_created")
    list_filter = ("user", "time_created")
    search_fields = ("title", "description", "user__username")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour le modèle Review.

    Attributs:
        list_display (tuple): Colonnes affichées dans la liste des critiques
        list_filter (tuple): Filtres disponibles dans la liste
        search_fields (tuple): Champs utilisés pour la recherche

    Exemple d'utilisation:
        @admin.register(Review)
        class ReviewAdmin(admin.ModelAdmin):
    """
    list_display = ("headline", "rating", "user", "ticket", "time_created")
    list_filter = ("rating", "user", "time_created")
    search_fields = ("headline", "body", "user__username", "ticket__title")


@admin.register(UserFollows)
class UserFollowsAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour le modèle UserFollows.

    Attributs:
        list_display (tuple): Colonnes affichées dans la liste des abonnements
        list_filter (tuple): Filtres disponibles dans la liste
        search_fields (tuple): Champs utilisés pour la recherche

    Exemple d'utilisation:
        @admin.register(UserFollows)
        class UserFollowsAdmin(admin.ModelAdmin):
    """
    list_display = ("user", "followed_user")
    list_filter = ("user", "followed_user")
    search_fields = ("user__username", "followed_user__username")
