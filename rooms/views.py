from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import Room
from .serializer import RoomSerializer


class ListRoomsView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


