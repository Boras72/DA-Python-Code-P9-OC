from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm
from django.contrib import messages


class SignupPage(View):
    def get(self, request):
        form = SignupForm()
        return render(request, 'authe/signup.html', {'form': form})
    
    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription réussie ! Bienvenue {user.username} !")
            return redirect('feed')
        return render(request, 'authe/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenue, {user.username} !")
                return redirect('feed')
            else:
                messages.error(request, "Identifiants invalides")
    else:
        form = LoginForm()
    return render(request, 'authe/login.html', {'form': form})


@login_required
def logout_user(request):
    username = request.user.username  # Récupérer le nom d'utilisateur avant la déconnexion
    logout(request)
    messages.success(request, f"Au revoir, {username} !")
    return redirect('login')
