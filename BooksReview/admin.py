from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from authe.models import User  # Importation du modèle User personnalisé
from func.models import Ticket, Review, UserFollows
 

class CustomUserAdmin(UserAdmin): #(héritage du modèle UserAdmin personnalisé = modèle par défaut de Django)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
# classe CustomUserAdmin qui hérite de UserAdmin pour personnaliser l'affichage et les fonctionnalités de l'interface d'administration pour les utilisateurs.

# Enregistrez le modèle User personnalisé (abstractUser) avec l'admin personnalisé
admin.site.register(User, CustomUserAdmin)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'time_created')
    list_filter = ('user', 'time_created')
    search_fields = ('title', 'description', 'user__username')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('headline', 'rating', 'user', 'ticket', 'time_created')
    list_filter = ('rating', 'user', 'time_created')
    search_fields = ('headline', 'body', 'user__username', 'ticket__title')

@admin.register(UserFollows)
class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ('user', 'followed_user')
    list_filter = ('user', 'followed_user')
    search_fields = ('user__username', 'followed_user__username')

