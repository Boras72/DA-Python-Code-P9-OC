from django.contrib import admin
from .models import Ticket, Review, UserFollows

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