from django.contrib.auth import authenticate
from django.conf import settings
import jwt
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer, RelatedUserSerializer
from rooms.serializers import RoomSerializer
from rooms.models import Room
from .models import User
from .permissions import IsSelf


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAdminUser]
        elif self.action == "create" or self.action == "retrieve":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsSelf | IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["post"])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is not None:
            encoded_jwt = jwt.encode(
                {"id": user.pk}, settings.SECRET_KEY, algorithm="HS256"
            )
            return Response(data={"token": encoded_jwt, "id": user.id, "message": "Hello, world"})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class FavsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = RoomSerializer(user.favs.all(), many=True)
        return Response(data=serializer.data)

    def put(self, request):
        pk = request.data.get("pk", None)
        user = request.user
        if pk is not None:
            try:
                room = Room.objects.get(pk=pk)
                if room in user.favs.all():
                    user.favs.remove(room)
                else:
                    user.favs.add(room)
                return Response(data=UserSerializer(user).data)
            except Room.DoesNotExist:
                pass
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
        serializer = RelatedUserSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)




