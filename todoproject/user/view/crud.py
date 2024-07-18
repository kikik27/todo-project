from rest_framework.views import APIView
from helpers.response import Response
from django.db import DatabaseError
from django.core.exceptions import ObjectDoesNotExist
from user.models import Users
import json
from django.db.models import (CharField, Exists, OuterRef, Q, Subquery,
                              UUIDField, Value)
from user.serializers import (UserPOSTSerializer, UserGETSerializer)

message_failed = "Failed"
message_success = "Success"
error_user_not_found = {"error": "User data not found"}

class User(APIView):
  serializer_class = UserGETSerializer
  def get(self, request, id=None):
    f_name = request.GET.get('name')
    f_email = request.GET.get('email')
    f_keyword = request.GET.get('keyword')
    
    query = Users.objects.all()
    
    if id:
      return self._get_detail_user(serializer=self.serializer_class, id=id)
    
    if f_name:
      query = query.filter(name=f_name)
      
    if f_email:
      query = query.filter(email=f_email)
      
    if f_keyword:
      query = query.filter(Q(name=f_keyword)|Q(email=f_keyword))
    
    if not query.exists():
        return Response.notFound(message=message_failed)
      
    serializer = UserGETSerializer(query, many=True)
    return Response.ok(data=serializer.data, message=message_success)
      
  def post(self,request):
        try:
            json_data = json.loads(request.body)
            serializer = UserPOSTSerializer(data=json_data)
            
            if not serializer.is_valid():
                print(serializer.errors)
                
                return Response.badRequest(
                    message= message_failed,
                    data= serializer.errors
                )
            
            serializer.save()

            return Response.ok(
                data=serializer.data,
                message=message_success
            )
        except ObjectDoesNotExist:
            print("Object does not exist")
            return Response.badRequest(
                    data=error_user_not_found,
                    message=message_failed
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
            
  def _get_detail_user(self, serializer, id):
    try:
      query = Users.objects.filter(id=id).first()
      
      if not query:
        return Response.notFound(message=message_failed)
      
    except ObjectDoesNotExist:
            print("Object does not exist")
            return Response.badRequest(
                    data=error_user_not_found,
                    message=message_failed
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
            
    data = serializer(query).data
    return Response.ok(data=data, message=message_success)