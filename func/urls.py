from django.urls import path
from .views import (
    ticket_create, ticket_edit, ticket_delete, feed, create_review, 
    create_ticket_review, edit_review, delete_review, posts, 
    subscriptions, follow_user, unfollow_user, create_standalone_review
)

urlpatterns = [
    path('feed/', feed, name='feed'),
    path('posts/', posts, name='posts'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('follow/<int:user_id>/', follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow_user'),
    path('ticket/create/', ticket_create, name='ticket_create'),
    path('ticket/edit/<int:ticket_id>/', ticket_edit, name='ticket_edit'),
    path('ticket/delete/<int:ticket_id>/', ticket_delete, name='ticket_delete'),
    path('review/create/<int:ticket_id>/', create_review, name='create_review'),
    path('review/create/', create_standalone_review, name='create_standalone_review'),
    path('ticket-review/create/', create_ticket_review, name='create_ticket_review'),
    path('review/edit/<int:review_id>/', edit_review, name='edit_review'),
    path('review/delete/<int:review_id>/', delete_review, name='delete_review'),
]