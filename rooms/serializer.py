from rest_framework import serializers
from .models import Room
from users.serializer import UserSerializer


class ReadRoomSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Room
        exclude = ("modified",)

    def validate(self, data):
        if data["beds"] < 5:
            raise serializers.ValidationError("Room is too small")
        else:
            if data["check_in"] == data["check_out"]:
                raise serializers.ValidationError("Room is Big. but, Not Enough Time to Check out")
            else:
                print("Validate Room OK")
                return data


class WriteRoomSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=140)
    address = serializers.CharField(max_length=140)
    price = serializers.IntegerField(help_text="USD per night")
    beds = serializers.IntegerField(default=1)
    lat = serializers.DecimalField(max_digits=10, decimal_places=6)
    lng = serializers.DecimalField(max_digits=10, decimal_places=6)
    bedrooms = serializers.IntegerField(default=1)
    bathrooms = serializers.IntegerField(default=1)
    check_in = serializers.TimeField(default="00:00:00")
    check_out = serializers.TimeField(default="00:00:00")
    instant_book = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return Room.objects.create(**validated_data)

    def validate(self, data):
        if not self.instance:
            if data.get("check_in") == data.get("check_out"):
                print(data.get("check_in"), data.get("check_out"))
                raise serializers.ValidationError("Room is Big. but, Not Enough Time to Check out")
        else:
            print("Validate Room OK")
            return data

    def update(self, instance, validated_data):
        pass