from .models import User
from rest_framework import serializers


class RelatedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("groups",
                   "user_permissions",
                   "password",
                   "last_login",
                   "is_superuser",
                   "is_staff",
                   "is_active",
                   "date_joined",
                   "favs")

class ReadUserSerializer(serializers.ModelSerializer):
    pass

class WriteUserSerializer(serializers.ModelSerializer):
    pass
