from rest_framework import serializers
from user.models import Users
from django.contrib.auth import authenticate

class ValidationLoginSerializer(serializers.Serializer):
  username_or_email = serializers.CharField(max_length=150)
  password = serializers.CharField(max_length=128, write_only=True)

  def validate_username_or_email(self, value):
      if not value:
          raise serializers.ValidationError("Username/email is required.")
      return value

  def validate_password(self, value):
      if not value:
          raise serializers.ValidationError("Password is required.")
      return value

  def validate(self, data):
      username = data.get('username_or_email')
      password = data.get('password')

      if not username or not password:
          raise serializers.ValidationError(
              "Both username/email and password are required.")

      return data
  # email = serializers.CharField(required=True)
  # password = serializers.CharField(required=True, write_only=True)
  
  # def validate_email(self,data):
  #   if not Users.objects.filter(email=data).exists():
  #     raise serializers.ValidationError("Email is not registered")
  #   return data
  
  # def validate(self,data):
  #   email = data.get('email')
  #   password = data.get('password')
  #   user = authenticate(email=email, password=password)
    
  #   if not user: 
  #     raise serializers.ValidationError("Passwords do not match")
  #   return user;
  
class AuthSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    class Meta:
      model = Users
      fields = ['id', 'name', 'username', 'email', 'is_active', 'last_login', 'is_staff']