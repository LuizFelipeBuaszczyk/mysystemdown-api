from rest_framework import serializers

class ResetPasswordRequestSerializer(serializers.Serializer):
    token = serializers.CharField()

class ResetPasswordResponseSerializer(serializers.Serializer):
    message = serializers.CharField()