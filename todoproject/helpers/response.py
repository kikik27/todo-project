from django.http import JsonResponse


class Response:

    def base(self, data=None, message="", status=200):
        if data is None:
            data = []

        return JsonResponse({
            'data': data,
            'message': message
        }, status=status)

    @staticmethod
    def ok(data=None, message=""):
        return Response().base(data=data, message=message, status=200)

    @staticmethod
    def badRequest(data=None, message=""):
        return Response().base(data=data, message=message, status=400)
    def notFound(data=None, message=""):
        return Response().base(data=data, message=message, status=404)
    def unauthorized(data=None, message=None):
        return Response().base(data=data, message= message if message is not None else "Unauthorized", status=401)
    @staticmethod 
    def serverError(data=None, message=""):
        return Response().base(data=data, message=message, status=500)
    
    def get_pagination_response(data, serializer, request, pagination_class):
        paginator = pagination_class()
        paginated_data = paginator.paginate_queryset(data, request)

        response_data = serializer(paginated_data, many=True).data

        return paginator.get_paginated_response(response_data, f"{serializer.Meta.model.__name__} data retrieved")