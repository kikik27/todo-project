from rest_framework import serializers
from user.models import Users
from django.contrib.auth import authenticate

class ValidationLoginSerializer(serializers.Serializer):
  email = serializers.EmailField(required=True)
  password = serializers.CharField(required=True)
  
  def validate_email(self,data):
    if not Users.objects.filter(email=data).exists():
      raise serializers.ValidationError("Email is not registered")
    return data
  
  # def validate(self,data):
  #   email = data.get('email')
  #   password = data.get('password')
  #   user = authenticate(email=email, password=password)
    
  #   if not user: 
  #     raise serializers.ValidationError("Passwords do not match")
  #   return user;
  
class AuthSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    role_id = serializers.IntegerField(read_only=True)
    role_name = serializers.CharField(read_only=True)
    
    class Meta:
      model = Users
      fields = ['id', 'name', 'email', 'is_active', 'role_id', 'role_name']