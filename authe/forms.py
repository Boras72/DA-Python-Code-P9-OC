from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=63,
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre nom d\'utilisateur'
        })
    )
    password = forms.CharField(
        max_length=63,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre mot de passe'
        }),
        label="Mot de passe"
    )

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnalisation des messages d'aide
        self.fields['username'].help_text = "Requis. 150 caractères maximum. Uniquement des lettres, nombres et les caractères « @ », « . », « + », « - » et « _ »."
        self.fields['password1'].help_text = """
            <ul>
                <li>Votre mot de passe ne peut pas trop ressembler à vos autres informations personnelles.</li>
                <li>Votre mot de passe doit contenir au minimum 8 caractères.</li>
                <li>Votre mot de passe ne peut pas être un mot de passe couramment utilisé.</li>
                <li>Votre mot de passe ne peut pas être entièrement numérique.</li>
            </ul>
        """
        self.fields['password2'].help_text = "Saisissez le même mot de passe que précédemment, pour vérification."
