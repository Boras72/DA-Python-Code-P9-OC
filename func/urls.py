"""
Ce module définit les URLs de l'application fonctionnelle.

Dépendances:
- django.urls
- .views

Fonctions principales:
- feed: Affichage du flux d'activité
- posts: Gestion des posts (tickets et critiques)
- subscriptions: Gestion des abonnements
- ticket_create/edit/delete: CRUD des tickets
- create_review/edit_review/delete_review: CRUD des critiques
- create_ticket_review: Création simultanée ticket + critique

Routes principales:

Flux et Posts:
    - /feed/: Flux d'activité
    - /posts/: Liste des posts de l'utilisateur

Abonnements:
    - /subscriptions/: Gestion des abonnements
    - /follow/<user_id>/: Suivre un utilisateur
    - /unfollow/<user_id>/: Ne plus suivre un utilisateur

Tickets:
    - /ticket/create/: Créer un ticket
    - /ticket/edit/<ticket_id>/: Modifier un ticket
    - /ticket/delete/<ticket_id>/: Supprimer un ticket

Critiques:
    - /review/create/<ticket_id>/: Créer une critique
    - /review/edit/<review_id>/: Modifier une critique
    - /review/delete/<review_id>/: Supprimer une critique
    - /ticket-review/create/: Créer un ticket et sa critique
"""

from django.urls import path
from .views import (
    ticket_create,
    ticket_edit,
    ticket_delete,
    feed,
    create_review,
    create_ticket_review,
    edit_review,
    delete_review,
    posts,
    subscriptions,
    follow_user,
    unfollow_user,
)

urlpatterns = [
    path("feed/", feed, name="feed"),
    path("posts/", posts, name="posts"),
    path("subscriptions/", subscriptions, name="subscriptions"),
    path("follow/<int:user_id>/", follow_user, name="follow_user"),
    path("unfollow/<int:user_id>/", unfollow_user, name="unfollow_user"),
    path("ticket/create/", ticket_create, name="ticket_create"),
    path("ticket/edit/<int:ticket_id>/", ticket_edit, name="ticket_edit"),
    path("ticket/delete/<int:ticket_id>/", ticket_delete, name="ticket_delete"),
    path("review/create/<int:ticket_id>/", create_review, name="create_review"),
    path("review/edit/<int:review_id>/", edit_review, name="edit_review"),
    path("review/delete/<int:review_id>/", delete_review, name="delete_review"),
    path("ticket-review/create/", create_ticket_review, name="create_ticket_review"),
]
