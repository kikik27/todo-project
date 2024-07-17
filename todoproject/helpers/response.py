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
    def unauthorized(data=None, message=""):
        return Response().base(data=data, message=message, status=401)
    @staticmethod 
    def serverError(data=None, message=""):
        return Response().base(data=data, message=message, status=500)