from django.urls import path
from .views import SignupPage, login_view, logout_user

urlpatterns = [
    path("login/", login_view, name="login"),
    path("signup/", SignupPage.as_view(), name="signup"),
    path("logout/", logout_user, name="logout"),
]
