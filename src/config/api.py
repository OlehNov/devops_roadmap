from django.http import HttpResponse


def ping_pong_view(request):
    if request.method.upper() == "GET":
        return HttpResponse("{'ping': 'pong'}")
    else:
        return HttpResponse("POST, PUT, PATCH methods are not allowed")
