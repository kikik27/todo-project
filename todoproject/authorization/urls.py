from django.urls import path

# from authorization.views import Login
from authorization.view.login import Login
from authorization.view.register import Register
from . import views

urlpatterns = [
    path("login", Login.as_view(), name="login"),
    path("register", Register.as_view(), name="register"),
    path("profile", views.UserLogin, name="profile"),
]
