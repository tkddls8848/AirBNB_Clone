from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .models import Room
from .serializers import RoomSerializer
from .permissions import IsOwner


class OwnPagination(PageNumberPagination):
    page_size = 20


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [permissions.AllowAny]
        elif self.action == "create":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]


@api_view(["GET"])
def room_search(request):
    rooms = Room.objects.filter()
    paginator = OwnPagination()
    result = paginator.paginate_queryset(rooms, request)
    serializer = RoomSerializer(result, many=True)
    return paginator.get_paginated_response(serializer.data)