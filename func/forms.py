from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Ticket, Review, UserFollows
from django.contrib.auth import get_user_model

User = get_user_model()

# les fichiers de formulaires sont utilisés pour définir et gérer les champs des formulaires des pages web
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'body']

class UserFollowsForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ['followed_user']
        
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2')
        