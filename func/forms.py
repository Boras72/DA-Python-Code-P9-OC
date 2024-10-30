from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Ticket, Review, UserFollows
from django.contrib.auth import get_user_model

User = get_user_model()

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']

class UserFollowsForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ['followed_user']

class UserSearchForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Rechercher un utilisateur...',
            'class': 'search-input'
        })
    )

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2')