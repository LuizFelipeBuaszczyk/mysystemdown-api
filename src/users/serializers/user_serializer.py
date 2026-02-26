from rest_framework import serializers
from users.models import User

class UserReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]

class UserWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]