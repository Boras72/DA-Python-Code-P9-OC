"""
URL configuration for BooksReview project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
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
    if request.user.is_authenticated:
        return redirect("feed")
    return redirect("login")


urlpatterns = [
    path("", root_redirect, name="root"),
    path("admin/", admin.site.urls),
    path("auth/", include("authe.urls")),
    path("", include("func.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
