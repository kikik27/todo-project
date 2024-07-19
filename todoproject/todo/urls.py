from django.urls import path
from todo.view.crud import Todo

urlpatterns = [
    path('', Todo.as_view(), name='TodosCRUD'),
]