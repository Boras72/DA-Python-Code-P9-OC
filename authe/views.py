"""
Ce module contient les vues utilisées pour l'authentification des utilisateurs dans l'application Django.
Dépendances :
- django.contrib.auth
- django.shortcuts
- django.views.generic
- django.contrib.auth.decorators
- django.contrib
- .forms

Classes principales :
- SignupPage : Vue pour l'inscription des utilisateurs.

Fonctions principales :
- login_view : Vue pour la connexion des utilisateurs.
- logout_user : Vue pour la déconnexion des utilisateurs.

Routes principales :
- /login/ : Route pour la connexion des utilisateurs.
- /signup/ : Route pour l'inscription des utilisateurs.
- /logout/ : Route pour la déconnexion des utilisateurs.
"""
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm
from django.contrib import messages


class SignupPage(View):
    """
    Vue pour l'inscription des utilisateurs.

    Méthodes :
        - get : Affiche le formulaire d'inscription.
        - post : Traite le formulaire d'inscription.

    Args:
        request (HttpRequest): La requête HTTP.

    Returns:
        HttpResponse: La réponse HTTP avec le formulaire d'inscription ou une redirection en cas de succès.

    Exemple d'utilisation :
        # Dans urls.py
        path("signup/", SignupPage.as_view(), name="signup")
    """
    def get(self, request):
        """
        Affiche le formulaire d'inscription.

        Args:
            request (HttpRequest): La requête HTTP.

        Returns:
            HttpResponse: La réponse HTTP avec le formulaire d'inscription.
        """
        form = SignupForm()
        return render(request, "authe/signup.html", {"form": form})

    def post(self, request):
        """
        Traite le formulaire d'inscription.

        Args:
            request (HttpRequest): La requête HTTP.

        Returns:
            HttpResponse: La réponse HTTP avec le formulaire d'inscription ou une redirection en cas de succès.
        """
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription réussie ! Bienvenue {user.username} !")
            return redirect("feed")
        return render(request, "authe/signup.html", {"form": form})


def login_view(request):
    """
    Vue pour la connexion des utilisateurs.

    Args:
        request (HttpRequest): La requête HTTP.

    Returns:
        HttpResponse: La réponse HTTP avec le formulaire de connexion ou une redirection en cas de succès.

    Exemple d'utilisation :
        # Dans urls.py
        path("login/", login_view, name="login")
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request,f"Bienvenue, {user.username} !", extra_tags='aria-live="polite"') # WCAG: Rendre le message d'alerte accessible
                return redirect("feed")
            else:
                messages.error(request, "Identifiants invalides.", extra_tags='aria-live="polite" role="alert"' )# WCAG: Rendre le message d'erreur accessible   
    else:
        form = LoginForm()
    return render(request, "authe/login.html", {"form": form})


@login_required
def logout_user(request):
    """
    Vue pour la déconnexion des utilisateurs.

    Args:
        request (HttpRequest): La requête HTTP.

    Returns:
        HttpResponse: Une redirection vers la page de connexion.

    Exemple d'utilisation :
        # Dans urls.py
        path("logout/", logout_user, name="logout")
    """
    username = request.user.username  # Récupérer le nom d'utilisateur avant la déconnexion
    logout(request)
    messages.success(request, f"Au revoir, {username} !")
    return redirect("login")
