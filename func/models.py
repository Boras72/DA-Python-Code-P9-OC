from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Ticket(models.Model): # billet demandant une critique
    # Your Ticket model definition goes here 
    title = models.CharField(max_length=128, verbose_name='Title')
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
       

class Review(models.Model): # critique
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])  # validates that rating must be between 0 and 5 (commentaires/critiques)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model): # suivis des utilisateurs (abonnements)
    # Your UserFollows model definition goes here 
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')    #refèrence à l'utilisateur personnalisé au lieu du user prédefinit par django
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed_by')

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user', )  
        



