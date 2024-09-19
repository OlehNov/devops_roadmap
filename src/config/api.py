from rest_framework.response import Response
from rest_framework.views import APIView


class PingView(APIView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return Response({'response': 'pong'})
