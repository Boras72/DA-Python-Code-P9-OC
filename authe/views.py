from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import SignupForm, LoginForm
from django.contrib.auth.decorators import login_required


class SignupPage(View):
    def get(self, request):
        form = SignupForm()
        return render(request, 'authe/signup.html', {'form': form})
    
    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
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
                return redirect('feed')
            else:
                form.add_error(None, 'Identifiants invalides')
    else:
        form = LoginForm()
    return render(request, 'authe/login.html', {'form': form})

#def logout_user(request):
    #if request.user.is_authenticated:
    #    logout(request)
    #return redirect('login')

@login_required
def logout_user(request):
    logout(request)
    return redirect('login')