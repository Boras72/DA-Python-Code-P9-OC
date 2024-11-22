"""
Ce module définit les URLs principales du projet Django.

Dépendances:
- django.contrib.admin
- django.urls
- django.shortcuts
- django.conf
- django.conf.urls.static

Fonctions principales:
- root_redirect: Redirige vers feed ou login selon l'authentification

Routes principales:
Authentication:
    - /auth/: URLs de l'application d'authentification
    - /auth/login/: Connexion
    - /auth/signup/: Inscription
    - /auth/logout/: Déconnexion

Administration:
    - /admin/: Interface d'administration Django

Application principale:
    - /: Redirection racine
    - /*: URLs de l'application principale
"""

# Le fichier "urls.py" définit les chemins URL pour les différentes vues de l'application
# Les noms des chemins URL doivent correspondre à ceux utilisés dans le fichier 'views.py'.
# Attention: 'login' est utilisé ici au lieu de 'connexion'. Utiliser toujours les mêmes noms dans les vues et les templates.
# Il est conseillé de regrouper les URLs par application, utiliser plutot 'include()' pour séparer les URLs de 'authe' et 'func' dans leurs propres fichiers urls.py.

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static


def root_redirect(request):
    """
    Redirige l'utilisateur selon son état d'authentification.

    Args:
        request (HttpRequest): La requête HTTP.

    Returns:
        HttpResponseRedirect: Redirection vers 'feed' si authentifié,
                            sinon vers 'login'.

    Exemple d'utilisation:
        path('', root_redirect, name='root')
    """
    if request.user.is_authenticated:
        return redirect("feed")
    return redirect("login")


urlpatterns = [
    path("", root_redirect, name="root"),
    path("admin/", admin.site.urls),
    path("auth/", include("authe.urls")),
    path("", include("func.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
