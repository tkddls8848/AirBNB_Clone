from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Room
from .serializers import RoomSerializer


class OwnPagination(PageNumberPagination):
    page_size = 10


class RoomsView(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        paginator = OwnPagination()
        result = paginator.paginate_queryset(rooms, request)
        serializer = RoomSerializer(result, many=True)
        return Response(data=serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            room = serializer.save(user=request.user)
            room_serializer = RoomSerializer(room)
            return Response(data=room_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SeeRoomView(APIView):

    def get_room(self, pk):
        try:
            room = Room.objects.get(pk=pk)
            return room
        except Room.DoesNotExist:
            return None

    def get(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            serializer = RoomSerializer(room)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif room is None:
            return Response(data="room isn`t exist", status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        room = self.get_room(pk)
        if room.user != request.user:
            return Response(data="Unauthorized User", status=status.HTTP_401_UNAUTHORIZED)
        if room is not None:
            serializer = RoomSerializer(room)
            room.delete()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            if room.user != request.user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            serializer = RoomSerializer(room, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data="room for update isn`t exist", status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def room_search(request):
    rooms = Room.objects.filter()
    paginator = OwnPagination()
    result = paginator.paginate_queryset(rooms, request)
    serializer = RoomSerializer(result, many=True)
    return paginator.get_paginated_response(serializer.data)