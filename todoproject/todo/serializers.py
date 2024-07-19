
from rest_framework import serializers
from .models import Todos
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator

class TodoGETSerializer(serializers.ModelSerializer):
    class Meta:
        model= Todos
        fields= '__all__'

class TodoPOSTSerializer(serializers.ModelSerializer):
  

    name = serializers.CharField(required=True)
    date = serializers.DateField(required=True)
    status = serializers.BooleanField(required=True)
    
    class Meta:
        model= Todos
        fields= '__all__'
    
class TodoUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Todos.objects.all(), message="This email is already in use.")]
    )
    class Meta:
        model= Todos
        fields= ['user_id', 'name', 'date', 'status']