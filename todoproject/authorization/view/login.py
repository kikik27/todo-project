from rest_framework.views import APIView
from helpers.response import Response
from authorization.serializers import ValidationLoginSerializer
from django.contrib.auth.hashers import check_password
from user.models import Users
from authorization.view.jwt import generate_token

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
      user = Users.objects.get(email=email)  # Ubah sesuai model pengguna Anda
      password_correct = check_password(password, user.password)
      
      if not password_correct:
        return Response.unauthorized(
        data="Password incorrect",
        message="Failed"
        )
      payload_user = {
        "user_id": user.id,
        "email": user.email,
      }
      token = generate_token(payload_user)
      
      return Response.ok(data=token, message="Login successful")
      
    except Exception as e:
      return Response.serverError(
        data={"error": f"An unexpected error occurred: {str(e)}"},
        message="Failed"
      )