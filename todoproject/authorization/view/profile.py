from rest_framework.views import APIView
from helpers.response import Response


class Profile(APIView):
  def get(self, request):
    if not request.user == None:
      return Response.unauthorized(message='Authorization header missing or Token has expired')
    return Response.ok(data=request.user, message="Data retrieved successfully")