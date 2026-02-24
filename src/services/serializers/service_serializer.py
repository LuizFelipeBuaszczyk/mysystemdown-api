from rest_framework import serializers
from systems.models import Service

class ServiceReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "title", "url", "description", "is_active", "health_check_interval"]
        
class ServiceDeleteSerializer(serializers.Serializer):
    message = serializers.CharField()
    deleted_id = serializers.UUIDField()

class ServiceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["title", "url", "description", "is_active", "health_check_interval"]
        