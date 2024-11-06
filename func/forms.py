from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Ticket, Review
from django.contrib.auth import get_user_model

User = get_user_model()

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre du livre/article'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Décrivez le livre ou l\'article',
                'rows': 5
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control-file'
            })
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        widgets = {
            'headline': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de votre critique'
            }),
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(6)]),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Écrivez votre critique',
                'rows': 5
            })
        }

class UserSearchForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rechercher un utilisateur...'
        })
    )