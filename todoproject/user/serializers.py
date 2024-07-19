
from rest_framework import serializers
from .models import (Users, Roles, UserRoles)
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator

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
        UserRoles.objects.create(user_id=user.id, role_id=1)
        return user
    
class UserUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Users.objects.all(), message="This email is already in use.")]
    )
    class Meta:
        model= Users
        fields= ['id','name','email']
    
    def validate_email(self, data):
        user_id = self.instance.id if self.instance else None
        if Users.objects.filter(email=data).exclude(id=user_id).exists():
            raise serializers.ValidationError("This email is already in use.")
        return data
    
class RoleGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['id', 'name']

class RolePOSTSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    
    class Meta:
        model= Roles
        fields= ['name']
        