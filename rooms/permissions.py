from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

    def has_room_permission(self, request, view, room):
        return request.user == room.user