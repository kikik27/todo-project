from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest
from rest_framework.views import APIView
from helpers.response import Response
from django.contrib.auth import authenticate as authLogin
from authorization.serializers import ValidationLoginSerializer
from user.models import Users
from django.contrib.auth.hashers import check_password
from authorization.view.jwt import generate_token
from user.serializers import UserPOSTSerializer
import json
from django.db import DatabaseError
from user.models import Users
from authorization.serializers import AuthSerializer
from django.db.models import OuterRef, Subquery, IntegerField, Q
from django.db.models.functions import Cast
from django.contrib.auth.backends import ModelBackend
from django.utils import timezone

message_failed = "Failed"
message_success = "Success"
error_user_not_found = {"error": "User data not found"}

# def _get_user_permissions(user_id):
#   user_query = Users.objects.filter(id=user_id).values('id', 'email', 'name','username','is_active', 'password')
#   user_roles_data = UserRoles.objects.filter(user_id=Cast(OuterRef('id'), IntegerField())).values_list('role_id', flat=True)
#   role_data = Roles.objects.filter(id=Cast(OuterRef('role_id'), IntegerField())).values('name')
  
#   query = user_query.annotate(
#       role_id=Subquery(user_roles_data.values('role_id')[:1]),
#       role_name=Subquery(role_data.values('name')[:1])
#   ).first()
  
#   return AuthSerializer(query).data

class UsernameOrEMailBackend(ModelBackend):
  def authenticate(self, request, email=None, password=None, **kwargs):
    try:
      user = Users.objects.get(Q(email=email) | Q(username=email))
    except Users.DoesNotExist:
      return None
    else:
      if user.check_password(password):
        user.last_login = timezone.now()
        user.save()
        return user
      else:
        return None
      
  def get_user(self, user_id):
    try:
        return Users.objects.get(pk=user_id)
    except Users.DoesNotExist:
        return None


class Login(APIView):
  def post(self,request):
    try:
      serializer = ValidationLoginSerializer(data=request.data)
      
      if not serializer.is_valid():
        return Response.badRequest(
          message= "Validation errors occurred.",
          data= serializer.errors
        )
        
      email = serializer.validated_data.get('username_or_email')
      password = serializer.validated_data.get('password')
      
      user = authLogin(email=email, password=password)
      
      if user is None:
        return Response.notFound(
        data="Username/email are not registered",
        message="Failed"
        )
        
      payload_user = AuthSerializer(user).data
      token = generate_token(payload_user)
      
      return Response.ok(data={"token": token}, message="Login successful")
      
    except Exception as e:
      return Response.serverError(
        data={"error": f"An unexpected error occurred: {str(e)}"},
        message="Failed"
      )
      
class Profile(APIView):
  def get(self, request):
    if request.token is None:
      return Response.unauthorized(message='Authorization header missing or Token has expired')
    return Response.ok(data=request.token, message="User data retrieved successfully")
  
class Register(APIView):
  def post(self, request):
        try:
            serializer = UserPOSTSerializer(data=request.data)
            
            if not serializer.is_valid():
                # Return a response with the validation errors
                return Response.badRequest(
                    message= message_failed,
                    data= serializer.errors
                )
            
            serializer.save()

            return Response.ok(
                data=serializer.data,
                message=message_success
            )
        except DatabaseError as e:
            print({str(e)})
            return Response.badRequest(
                    data={"error": f"Database error: {str(e)}"},
                    message=message_failed
                )
        except Exception as e:
            print({str(e)})
            return Response.serverError(
                    data={"error": f"An unexpected error occurred: {str(e)}"},
                    message=message_failed
                )