from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReadUserSerializer, WriteUserSerializer
from rooms.serializers import RoomSerializer
from .models import User


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ReadUserSerializer(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = WriteUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(data=request.error, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def user_detail(request, pk):
    pass


class FavsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = RoomSerializer(user.favs.all(), many=True)
        return Response(data=serializer.data)

    def put(self, request):
        pass