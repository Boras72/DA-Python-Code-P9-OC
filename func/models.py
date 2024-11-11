from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Ticket(models.Model):
    title = models.CharField(max_length=128, verbose_name='Titre')
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets'
    )
    image = models.ImageField(null=True, blank=True, upload_to='tickets/')
    time_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-time_created']
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

    def __str__(self):
        return f"{self.title} - par {self.user.username}"

    def can_be_reviewed_by(self, user):
        """Vérifie si un utilisateur peut créer une critique pour ce ticket"""
        if not user or user.is_anonymous:
            return False
        if user == self.user:
            return False
        # Vérifie si l'utilisateur a déjà créé une critique pour ce ticket
        return not Review.objects.filter(ticket=self, user=user).exists()

class Review(models.Model):
    ticket = models.ForeignKey(
        to=Ticket,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time_created']
        unique_together = ['ticket', 'user']  # Empêche les critiques multiples
        verbose_name = 'Critique'
        verbose_name_plural = 'Critiques'

    def clean(self):
        if self.rating is not None and (self.rating < 0 or self.rating > 5):
            raise ValidationError('La note doit être comprise entre 0 et 5')
        
        # Vérification de l'existence d'une critique uniquement si le ticket est défini
        if self.ticket_id is not None and self.user_id is not None:
            existing_review = Review.objects.filter(
                ticket=self.ticket, 
                user=self.user
            ).exclude(pk=self.pk).exists()
            
            if existing_review:
                raise ValidationError('Vous avez déjà créé une critique pour ce ticket')

    def __str__(self):
        return f"Critique de {self.ticket.title} par {self.user.username}"

    @property
    def rating_as_stars(self):
        return '★' * self.rating + '☆' * (5 - self.rating)

class UserFollows(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following'
    )
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followed_by'
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'followed_user')
        ordering = ['-created_at']
        verbose_name = 'Abonnement'
        verbose_name_plural = 'Abonnements'

    def clean(self):
        if self.user == self.followed_user:
            raise ValidationError("Un utilisateur ne peut pas se suivre lui-même")

    def __str__(self):
        return f"{self.user.username} suit {self.followed_user.username}"