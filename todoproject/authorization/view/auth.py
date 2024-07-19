from rest_framework.views import APIView
from helpers.response import Response
from authorization.serializers import ValidationLoginSerializer
from django.contrib.auth.hashers import check_password
from user.models import Users
from authorization.view.jwt import generate_token
from user.serializers import UserPOSTSerializer
import json
from django.db import DatabaseError
from user.models import (Users, Roles, UserRoles)
from authorization.serializers import AuthSerializer
from django.db.models import OuterRef, Subquery, IntegerField
from django.db.models.functions import Cast

message_failed = "Failed"
message_success = "Success"
error_user_not_found = {"error": "User data not found"}

def _get_user_permissions(user_query):
  user_roles_data = UserRoles.objects.filter(user_id=Cast(OuterRef('id'), IntegerField())).values_list('role_id', flat=True)
  role_data = Roles.objects.filter(id=Cast(OuterRef('role_id'), IntegerField())).values('name')
  
  query = user_query.annotate(
      role_id=Subquery(user_roles_data.values('role_id')[:1]),
      role_name=Subquery(role_data.values('name')[:1])
  ).first()
  
  return AuthSerializer(query).data

class Login(APIView):
  def post(self,request):
    password = request.data.get('password')
    try:
      serializer = ValidationLoginSerializer(data=request.data)
      
      if not serializer.is_valid():
        print(serializer.errors)
        return Response.badRequest(
          message= "Validation errors occurred.",
          data= serializer.errors
        )
        
      email = serializer.validated_data['email']
      user_query = Users.objects.filter(email=email).values('id', 'email', 'name', 'is_active', 'password')
      user_password = user_query.get()
      password_correct = check_password(password, user_password.get('password'))
      
      print(password_correct)
      
      if not password_correct:
        return Response.unauthorized(
        data="Password incorrect",
        message="Failed"
        )
        
      payload_user = _get_user_permissions(user_query)
      token = generate_token(payload_user)
      
      return Response.ok(data=token, message="Login successful")
      
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
            print(request.data)
            serializer = UserPOSTSerializer(data=request.data)
            
            if not serializer.is_valid():
                print(serializer.errors)
                
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