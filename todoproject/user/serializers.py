
from rest_framework import serializers
from .models import Users
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator
import jwt
from django.utils import timezone
from authorization.view.jwt import generate_token

class UserGETSerializer(serializers.ModelSerializer):
    class Meta:
        model= Users
        fields= ['id','name','email']

class UserPOSTSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Users.objects.all(), message="This email is already in use.")]
    )
    password = serializers.CharField(required=True, write_only=True)
    
    class Meta:
        model= Users
        fields= ['id','name', 'email', 'password']
        
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = Users.objects.create(**validated_data)
        return user