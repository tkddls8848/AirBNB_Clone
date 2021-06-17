from rest_framework import serializers
from .models import Room
from users.serializer import TinyUserSerializer


class RoomSerializer(serializers.ModelSerializer):

    user = TinyUserSerializer()

    class Meta:
        model = Room
        fields = ("pk", "name", "price", "instant_book", "user")


class BigRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        exclude = ()