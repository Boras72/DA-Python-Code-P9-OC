from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Ticket, Review, UserFollows

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
        