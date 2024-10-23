from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import SignupPage, login_view, logout_user

urlpatterns = [
   
    #path('login/', LoginView.as_view(template_name='authe/login.html'), name='login'),
    path('login/', login_view, name='login'),
    path('signup/', SignupPage.as_view(), name='signup'),
    path('logout/', logout_user, name='logout'),
]