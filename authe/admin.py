from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
#from django.contrib.auth.models import User
from .models import User

# Register your models here.
#admin.site.register(UserAdmin) # pour gérer un superUser et les users dans l'admin interface



class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)


# Enregistrez le modèle User personnalisé avec l'admin personnalisé
admin.site.register(User, CustomUserAdmin)
