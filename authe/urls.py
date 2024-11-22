"""
Ce module définit les routes URL pour l'authentification des utilisateurs dans l'application Django.
Dépendances :
- django.urls
- .views

Fonctions principales :
- login_view : Vue pour la connexion des utilisateurs.
- SignupPage : Vue pour l'inscription des utilisateurs.
- logout_user : Vue pour la déconnexion des utilisateurs.

Routes principales :
- /login/ : Route pour la connexion des utilisateurs.
- /signup/ : Route pour l'inscription des utilisateurs.
- /logout/ : Route pour la déconnexion des utilisateurs.
"""

from django.urls import path
from .views import SignupPage, login_view, logout_user

urlpatterns = [
    path("login/", login_view, name="login"),
    path("signup/", SignupPage.as_view(), name="signup"),
    path("logout/", logout_user, name="logout"),
]
