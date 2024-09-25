from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView, status


class PingPongAPIView(APIView):
    permission_classes = [AllowAny]
    allowed_methods = ['GET']

    def get(self, request, *args, **kwargs):
        return Response({'ping': 'pong'}, status=status.HTTP_200_OK)
