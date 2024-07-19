from rest_framework.views import APIView
from helpers.response import Response
from django.db import DatabaseError
from django.core.exceptions import ObjectDoesNotExist
from todo.models import Todos
import json
from helpers.pagination import Paginator
from django.db.models import (CharField, Exists, OuterRef, Q, Subquery, UUIDField, Value)
from todo.serializers import (TodoPOSTSerializer, TodoGETSerializer, TodoUpdateSerializer)

message_failed = "Failed"
message_success = "Success"
error_user_not_found = {"error": "Todo data not found"}

class Todo(APIView):
  serializer_get_class = TodoGETSerializer
  serializer_post_class = TodoPOSTSerializer
  pagination_class = Paginator
  
  def get(self, request):
    user_id = request.token['id']
    role_name = request.token['role_name']

    f_name = request.GET.get('name')
    f_keyword = request.GET.get('keyword')
    f_detail = request.GET.get('detail')
    
    if role_name == 'user':
      query = Todos.objects.filter(user_id=user_id)
      
    if role_name == 'admin':
      query = Todos.objects.all()
      
    if role_name is None:
      return Response.unauthorized(data={"error": "Role is not available"})
    
    if f_detail:
      return self._get_detail_todo(serializer=self.serializer_get_class, id=f_detail)
    
    if f_name:
      query = query.filter(name=f_name)
      
    if f_keyword:
      query = query.filter(Q(name__icontains=f_keyword)|Q(email__icontains=f_keyword))
    
    if not query.exists():
        data = {"error": f"{self.serializer_get_class.Meta.model.__name__} data does not exist."}
        return Response.notFound(message=message_failed, data=data)
      
    return Response.get_pagination_response(query, self.serializer_get_class, request, self.pagination_class)
      
  def post(self,request):
    try:
      payload_data = request.data
      payload_data['user_id'] = request.token['id']
      serializer = TodoPOSTSerializer(data=payload_data)
            
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
  
  def put(self, request):
    user_key = request.GET.get('id', None)
    
    try:
      instance = Todos.objects.get(id=user_key)
      
      serializer = TodoUpdateSerializer(instance=instance,data=request.data)
      
      if not serializer.is_valid():
        print(serializer.errors)
        return Response.badRequest(
          message= message_failed,
          data= serializer.errors
      )
      
      serializer.update(instance=instance, validated_data=serializer.validated_data)
      
    except Todos.DoesNotExist:
      print("Todo does not exist")
      data = {"error": f"{self.serializer_get_class.Meta.model.__name__} data with ID {user_key} does not exist."}
      return Response.notFound(message=message_failed, data=data)
    
    message = f"{serializer.Meta.model.__name__} updated successfully"
    return Response.ok(data=serializer.data, message=message)
  
  def delete(self, request):
    user_key = request.GET.get('id', None)
    
    try:
      instance = Todos.objects.get(id=user_key)
      instance.delete()
      
    except Todos.DoesNotExist:
      print("Todo does not exist")
      data = {"error": f"{self.serializer_get_class.Meta.model.__name__} data with ID {user_key} does not exist."}
      return Response.notFound(message=message_failed, data=data)
    
    message = f"{Todos.__name__} deleted successfully"
    return Response.ok(message=message)
  
            
  def _get_detail_todo(self, serializer, id):
    try:
      query = Todos.objects.get(id=id)
      
      if not query:
        data = {"error": f"{self.serializer_get_class.Meta.model.__name__} data with ID {id} does not exist."}
        return Response.notFound(message=message_failed, data=data)
      
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