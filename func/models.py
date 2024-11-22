"""
Ce module définit les modèles de données pour les tickets et les critiques.

Dépendances:
- django.core.validators
- django.conf
- django.db
- django.core.exceptions
- django.utils

Classes principales:
- Ticket: Modèle pour les demandes de critique de livres/articles
- Review: Modèle pour les critiques
- UserFollows: Modèle pour les abonnements entre utilisateurs

Routes principales:
- Aucune route définie dans ce module
"""

from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Ticket(models.Model):
    """
    Modèle représentant une demande de critique de livre/article.

    Attributes:
        title (str): Titre du ticket (max 128 caractères)
        description (str): Description détaillée (max 2048 caractères)
        user (FK): Utilisateur ayant créé le ticket
        image (ImageField): Image optionnelle du livre/article
        time_created (DateTime): Date et heure de création

    Example:
        ticket = Ticket.objects.create(
            title="Le Petit Prince",
            description="Quelqu'un pourrait-il critiquer ce livre ?",
            user=request.user
        )
    """
    title = models.CharField(max_length=128, verbose_name="Titre")
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tickets")
    image = models.ImageField(null=True, blank=True, upload_to="tickets/")
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-time_created"]
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"

    def __str__(self):
        """
        Représentation textuelle du ticket.

        Returns:
            str: Titre du ticket et nom de l'auteur
        """
        return f"{self.title} - par {self.user.username}"

    def can_be_reviewed_by(self, user):
        """
        Vérifie si un utilisateur peut créer une critique pour ce ticket.

        Args:
            user (User): L'utilisateur à vérifier

        Returns:
            bool: True si l'utilisateur peut créer une critique, False sinon

        Example:
            if ticket.can_be_reviewed_by(request.user):
                # Autoriser la création d'une critique
        """
        if not user or user.is_anonymous:
            return False
        if user == self.user:
            return False
        # Vérifie si l'utilisateur a déjà créé une critique pour ce ticket
        return not Review.objects.filter(ticket=self, user=user).exists()


class Review(models.Model):
    """
    Modèle représentant une critique de livre/article.

    Attributes:
        ticket (FK): Ticket associé à la critique
        rating (int): Note de 0 à 5
        user (FK): Utilisateur ayant créé la critique
        headline (str): Titre de la critique (max 128 caractères)
        body (str): Contenu de la critique (max 8192 caractères)
        time_created (DateTime): Date et heure de création

    Example:
        review = Review.objects.create(
            ticket=ticket,
            rating=5,
            user=request.user,
            headline="Une œuvre magistrale",
            body="Ce livre est un chef-d'œuvre..."
        )
    """
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-time_created"]
        unique_together = ["ticket", "user"]  # Empêche les critiques multiples
        verbose_name = "Critique"
        verbose_name_plural = "Critiques"

    def clean(self):
        if self.rating is not None and (self.rating < 0 or self.rating > 5):
            raise ValidationError("La note doit être comprise entre 0 et 5")

        # Vérification de l'existence d'une critique uniquement si le ticket est défini
        if self.ticket_id is not None and self.user_id is not None:
            existing_review = Review.objects.filter(ticket=self.ticket, user=self.user).exclude(pk=self.pk).exists()

            if existing_review:
                raise ValidationError("Vous avez déjà créé une critique pour ce ticket")

    def __str__(self):
        return f"Critique de {self.ticket.title} par {self.user.username}"

    @property
    def rating_as_stars(self):
        return "★" * self.rating + "☆" * (5 - self.rating)


class UserFollows(models.Model):
    """
    Modèle représentant les relations d'abonnement entre utilisateurs.

    Attributes:
        user (FK): Utilisateur qui suit
        followed_user (FK): Utilisateur suivi
        created_at (DateTime): Date et heure de l'abonnement

    Example:
        follow = UserFollows.objects.create(
            user=request.user,
            followed_user=user_to_follow
        )
    """
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following")
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followed_by",
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("user", "followed_user")
        ordering = ["-created_at"]
        verbose_name = "Abonnement"
        verbose_name_plural = "Abonnements"

    def clean(self):
        """
        Valide que l'utilisateur ne peut pas se suivre lui-même.

        Raises:
            ValidationError: Si l'utilisateur tente de se suivre lui-même

        Example:
            follow = UserFollows(user=user1, followed_user=user2)
            follow.clean()  # Vérifie la validité
            follow.save()
        """
        if self.user == self.followed_user:
            raise ValidationError("Un utilisateur ne peut pas se suivre lui-même")

    def __str__(self):
        """
        Représentation textuelle de la relation d'abonnement.

        Returns:
            str: Description de la relation d'abonnement

        Example:
            follow = UserFollows.objects.get(id=1)
            print(follow)  # "user1 suit user2"
        """
        return f"{self.user.username} suit {self.followed_user.username}"
