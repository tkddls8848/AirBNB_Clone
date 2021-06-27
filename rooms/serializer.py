from rest_framework import serializers
from .models import Room
from users.serializer import UserSerializer


class RoomSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Room
        exclude = ("modified",)

