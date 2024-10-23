from func.views import (ticket_create, ticket_edit, ticket_delete, feed, create_review, create_ticket_review, edit_review, delete_review)
from django.urls import path


urlpatterns = [
    path('feed/', feed, name='feed'),
    path('ticket/create/', ticket_create, name='ticket_create'),
    path('ticket/edit/<int:ticket_id>/', ticket_edit, name='ticket_edit'),
    path('ticket/delete/<int:ticket_id>/', ticket_delete, name='ticket_delete'),
    path('review/create/<int:ticket_id>/', create_review, name='create_review'),
    path('ticket-review/create/', create_ticket_review, name='create_ticket_review'),
    path('review/edit/<int:review_id>/', edit_review, name='edit_review'),
    path('review/delete/<int:review_id>/', delete_review, name='delete_review'),

]

