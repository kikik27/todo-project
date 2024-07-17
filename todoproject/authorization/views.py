from helpers.response import Response

def UserLogin(request):
    if not request.token == None:
        return Response.ok(data=request.token, message="Success")