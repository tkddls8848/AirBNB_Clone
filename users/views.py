from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializer import UserSerializer


class MeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        pass
    def put(self, request):
        pass

@api_view(["GET"])
def user_detail(request, pk):
    pass

class FavsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        pass
    def put(self, request):
        pass