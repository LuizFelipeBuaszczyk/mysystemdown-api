from rest_framework import serializers

from tenants.serializers.client_serializer import ClientReadSerializer, ClientWriteSerializer
from tenants.serializers.domain_serializer import DomainReadSerializer, DomainWriteSerializer

class TenantWriteSerializer(serializers.Serializer):
    client = ClientWriteSerializer()

class TenantReadSerializer(serializers.Serializer):
    client = ClientReadSerializer()
    domain = DomainReadSerializer()