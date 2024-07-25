from django.shortcuts import render
from decouple import config
from django.utils import timezone
import jwt
from django.urls import reverse
from helpers.response import Response
from user.models import Users

expired_time = config("JWT_TOKEN_EXPIRED")

def _get_private_key():
    with open('private_key.pem') as private_key:
      return private_key.read()

def generate_token(payload_user):
    private_key = _get_private_key()
    payload = {
        "exp": timezone.now() + timezone.timedelta(hours=int(expired_time)),
        **payload_user
    }
    return jwt.encode(payload, private_key, algorithm='RS256')

class JWTMiddleware:
  
  def __init__(self, get_response):
    self.get_response = get_response
    self.exempt_urls = {reverse('login'), reverse('register')}
    self.public_key = self._get_public_key()

  def _get_public_key(self):
    with open('public_key.pem') as public_key:
      return public_key.read()
    
  def _get_token_from_header(self, request):
    auth_header = request.headers.get('Authorization', '')
    parts = auth_header.split()
    return parts[1] if len(parts) == 2 and parts[0].lower() == 'bearer' else None
  
  def _validate_token(self, token):
    try:
      return jwt.decode(token, self.public_key, algorithms=['RS256'])
    except jwt.ExpiredSignatureError:
      raise PermissionError('Token has expired')
    except jwt.InvalidTokenError:
      raise PermissionError('Invalid token')
    except Exception as e:
      print(f"Token validation error: {str(e)}")
    raise PermissionError(str(e))

  def __call__(self, request):
    if request.path in self.exempt_urls:
      return self.get_response(request)
    
    token = self._get_token_from_header(request)
    
    if not token: 
      return Response.unauthorized(message='Authorization header missing or Token has expired')
    
    try:
      decode_payload = self._validate_token(token)
      user = Users.objects.filter(id=decode_payload['id'], is_active=1).first()
      if not user:
          return Response.unauthorized()
      
      request.token = decode_payload
      request.user = user
    
    except Exception as e:
      return Response.serverError(
        data={"error": f"An unexpected error occurred: {str(e)}"},
        message="Failed"
      )
    return self.get_response(request)