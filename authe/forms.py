from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User                    # from django.contrib.auth import get_user_model
 
 




class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label="Nom d'utilisateur")
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label="Mot de passe")


class SignupForm(UserCreationForm):
    class Meta:
        model = User                            #get_user_model()                             
        fields = ("username", "email","password1","password2")