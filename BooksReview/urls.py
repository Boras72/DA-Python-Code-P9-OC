

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
#from django.contrib import auth
from django.urls import path, include
from authe.views import LoginPage, SignupPage, logout_user
from func.views import (ticket_create, ticket_edit, ticket_delete, feed, create_review, create_ticket_review, edit_review, delete_review)
from .views import accueil_view






urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginPage.as_view(), name='login'),
    path('signup/', SignupPage.as_view(), name='signup'),  
    path('logout/', logout_user, name='logout'),
    path('feed/', feed, name='feed'),
    path('ticket/create/', ticket_create, name='ticket_create'),
    path('ticket/edit/<int:ticket_id>/', ticket_edit, name='ticket_edit'),
    path('ticket/delete/<int:ticket_id>/', ticket_delete, name='ticket_delete'),
    path('review/create/<int:ticket_id>/', create_review, name='create_review'),
    path('ticket-review/create/', create_ticket_review, name='create_ticket_review'),
    path('review/edit/<int:review_id>/', edit_review, name='edit_review'),
    path('review/delete/<int:review_id>/', delete_review, name='delete_review'),
    path('', accueil_view, name='accueil'),

]



