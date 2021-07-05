from rest_framework import serializers
from .models import Room
from users.serializers import ReadUserSerializer


class RoomSerializer(serializers.ModelSerializer):

    user = ReadUserSerializer()

    class Meta:
        model = Room
        exclude = ("modified",)
        read_only_field = ("user", "id", "created", "updated")

    def create(self, validated_data):
        return Room.objects.create(**validated_data)

    def validate(self, data):
        if self.instance:
            check_in = data.get("check_in", self.instance.check_in)
            check_out = data.get("check_out", self.instance.check_out)
        else:
            check_in = data.get("check_in")
            check_out = data.get("check_out")
        if check_in == check_out:
            raise serializers.ValidationError("Not enought time for changes")
        return data

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.address = validated_data.get("address", instance.address)
        instance.price = validated_data.get("price", instance.price)
        instance.beds = validated_data.get("beds", instance.beds)
        instance.lat = validated_data.get("lat", instance.lat)
        instance.lng = validated_data.get("lng", instance.lng)
        instance.bedrooms = validated_data.get("bedrooms", instance.bedrooms)
        instance.bathrooms = validated_data.get("bathrooms", instance.bathrooms)
        instance.check_in = validated_data.get("check_in", instance.check_in)
        instance.check_out = validated_data.get("check_out", instance.check_out)
        instance.instant_book = validated_data.get("instant_book", instance.instant_book)
        instance.save()
        return instance