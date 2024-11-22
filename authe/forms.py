"""
Ce module contient les formulaires utilisés pour l'authentification des utilisateurs dans l'application Django.
Dépendances :
- django
- django.contrib.auth.forms
- django.contrib.auth.get_user_model

Classes principales :
- LoginForm : Formulaire de connexion des utilisateurs.
- SignupForm : Formulaire d'inscription des utilisateurs.

Routes principales :
- /login/ : Route pour la connexion des utilisateurs.
- /signup/ : Route pour l'inscription des utilisateurs.
- /logout/ : Route pour la déconnexion des utilisateurs.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    """
    Formulaire de connexion des utilisateurs.

    Args:
        username (str): Nom d'utilisateur.
        password (str): Mot de passe.

    Returns:
        None

    Exemple d'utilisation :
        form = LoginForm(data=request.POST)
        if form.is_valid():
            # Traiter la connexion
    """
    username = forms.CharField(
        max_length=63,
        label="Nom d'utilisateur",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Entrez votre nom d'utilisateur",
                "aria-label": "Nom d'utilisateur", #WCAG
                "aria-required": "true"
            }
        ),
    )
    password = forms.CharField(
        max_length=63,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control", 
                "placeholder": "Entrez votre mot de passe",
                "aria-label": "Mot de passe",  #WCAG
                "aria-required": "true"
            }
        ),
        label="Mot de passe",
    )


class SignupForm(UserCreationForm):
    """
    Formulaire d'inscription des utilisateurs.

    Args:
        username (str): Nom d'utilisateur.
        password1 (str): Mot de passe.
        password2 (str): Confirmation du mot de passe.

    Returns:
        None

    Exemple d'utilisation :
        form = SignupForm(data=request.POST)
        if form.is_valid():
            form.save()
            # Traiter l'inscription
    """
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        """
        Initialise le formulaire avec des messages d'aide personnalisés.

        Args:
            *args: Arguments positionnels.
            **kwargs: Arguments nommés.

        Returns:
            None
        """
        super().__init__(*args, **kwargs)
        # Ajout des classes pour les messages d'erreur
        self.error_class = 'error-message'
        self.error_css_class = 'form-error'
        self.required_css_class = 'required'

        # Configuration des widgets avec attributs d'accessibilité
        widget_attrs = {
            'aria-invalid': 'true',
            'role': 'alert',
            'aria-live': 'polite'
        }

        # Application des attributs aux champs
        for field in self.fields.values():
            field.widget.attrs.update(widget_attrs)

        # Attributs ARIA et messages d'aide
        self.fields['username'].widget.attrs.update({
            'aria-label': "Nom d'utilisateur",
            'aria-required': "true",
            'aria-describedby': "username-help"
        })
        self.fields['username'].help_text = (
            "Requis. 150 caractères maximum. Uniquement des lettres, nombres "
            "et les caractères « @ », « . », « + », « - » et « _ »."
        )

        self.fields['password1'].widget.attrs.update({
            'aria-label': "Mot de passe",
            'aria-required': "true",
            'aria-describedby': "password1-help"
        })
        self.fields['password1'].help_text = """
            <ul>
                <li>Votre mot de passe doit contenir au minimum 8 caractères.</li>
                <li>Votre mot de passe ne peut pas être un mot courant.</li>
                <li>Votre mot de passe ne peut pas être entièrement numérique.</li>
            </ul>
        """

        self.fields['password2'].widget.attrs.update({
            'aria-label': "Confirmation du mot de passe",
            'aria-required': "true",
            'aria-describedby': "password2-help"
        })
        self.fields['password2'].help_text = "Saisissez le même mot de passe que précédemment."


