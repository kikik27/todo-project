from django.urls import path
from user.view.crud import User

urlpatterns = [
    path('', User.as_view(), name='index'),
    path('<int:id>', User.as_view(), name='show'),
]