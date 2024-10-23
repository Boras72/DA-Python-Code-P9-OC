from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Ticket(models.Model):
    title = models.CharField(max_length=128, verbose_name='Title')
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
        return f"{self.title} - by {self.user.username}"

    def can_be_reviewed_by(self, user):
        """Vérifie si un utilisateur peut créer une critique pour ce ticket"""
        if not user or user.is_anonymous:
            return False
        if user == self.user:
            return False
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
        unique_together = ['ticket', 'user']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def clean(self):
        if self.rating < 0 or self.rating > 5:
            raise ValidationError('La note doit être comprise entre 0 et 5')
        if Review.objects.filter(ticket=self.ticket, user=self.user).exists():
            raise ValidationError('Vous avez déjà créé une critique pour ce ticket')

    def __str__(self):
        return f"Review of {self.ticket.title} by {self.user.username}"

    @property
    def rating_as_stars(self):
        """Retourne la note sous forme d'étoiles"""
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
        verbose_name = 'User follow'
        verbose_name_plural = 'User follows'

    def clean(self):
        if self.user == self.followed_user:
            raise ValidationError("Un utilisateur ne peut pas se suivre lui-même")

    def __str__(self):
        return f"{self.user.username} follows {self.followed_user.username}"