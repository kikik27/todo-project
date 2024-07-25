
from rest_framework import serializers
from .models import Users
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator

class UserGETSerializer(serializers.ModelSerializer):
    class Meta:
        model= Users
        fields= ['id','name','username','email']

class UserPOSTSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Users.objects.all(), message="This username is already in use.")]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Users.objects.all(), message="This email is already in use.")]
    )
    password = serializers.CharField(required=True, write_only=True)
    
    class Meta:
        model= Users
        fields= ['id','name','username', 'email', 'password']
        
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = Users.objects.create(**validated_data)
        return user
    
class UserUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Users.objects.all(), message="This username is already in use.")]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Users.objects.all(), message="This email is already in use.")]
    )
    class Meta:
        model= Users
        fields= ['id','name','username','email']
    
    def validate_email(self, data):
        user_id = self.instance.id if self.instance else None
        if Users.objects.filter(email=data).exclude(id=user_id).exists():
            raise serializers.ValidationError("This email is already in use.")
        return data
        