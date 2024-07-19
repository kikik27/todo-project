from django.urls import path

from authorization.view.auth import (Login, Register, Profile)

urlpatterns = [
    path("login", Login.as_view(), name="login"),
    path("register", Register.as_view(), name="register"),
    path("profile", Profile.as_view(), name="profile"),
]
