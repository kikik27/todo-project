from rest_framework.views import APIView
from helpers.response import Response
from user.serializers import UserPOSTSerializer
import json
from django.db import DatabaseError

message_failed = "Failed"
message_success = "Success"
error_user_not_found = {"error": "User data not found"}

class Register(APIView):
  def post(self, request):
        try:
            json_data = json.loads(request.body)
            serializer = UserPOSTSerializer(data=json_data)
            
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
            