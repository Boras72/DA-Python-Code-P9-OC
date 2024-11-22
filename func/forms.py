"""
Ce module définit les formulaires pour la gestion des tickets et des critiques.

Dépendances:
- django.forms
- .models
- django.contrib.auth

Classes principales:
- TicketForm: Formulaire pour créer/modifier un ticket
- ReviewForm: Formulaire pour créer/modifier une critique

Routes principales:
- Aucune route définie dans ce module
"""

from django import forms
from .models import Ticket, Review
from django.contrib.auth import get_user_model

User = get_user_model()


class TicketForm(forms.ModelForm):
    """
    Formulaire pour la création et modification des tickets.

    Args:
        title (str): Titre du ticket
        description (str): Description détaillée
        image (ImageField): Image optionnelle

    Returns:
        Ticket: Instance du modèle Ticket

    Exemple d'utilisation:
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
    """
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Titre du livre/article"}),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Décrivez le livre ou l'article",
                    "rows": 5,
                }
            ),
            "image": forms.FileInput(attrs={"class": "form-control-file"}),
        }


class ReviewForm(forms.ModelForm):
    """
    Formulaire pour la création et modification des critiques.

    Args:
        headline (str): Titre de la critique
        rating (int): Note de 0 à 5
        body (str): Contenu de la critique

    Returns:
        Review: Instance du modèle Review

    Exemple d'utilisation:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
    """
    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]
        widgets = {
            "headline": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Titre de votre critique",
                }
            ),
            "rating": forms.RadioSelect(choices=[(i, str(i)) for i in range(6)]),
            "body": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Écrivez votre critique",
                    "rows": 5,
                }
            ),
        }


class UserSearchForm(forms.Form):
    """
    Formulaire de recherche d'utilisateurs pour la gestion des abonnements.

    Attributes:
        username (CharField): Champ de recherche par nom d'utilisateur

    Returns:
        Form: Formulaire de recherche avec un champ username

    Example:
        form = UserSearchForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            users = User.objects.filter(username__icontains=username)
    """
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Rechercher un utilisateur...",
            }
        ),
    )
