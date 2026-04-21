from django.shortcuts import get_object_or_404
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter

from uuid import UUID

from systems.models import Service
from iam.permissions.service_permissions import ServicePermission
from services.services.service_service import ServiceService
from services.serializers.service_serializer import ServiceReadSerializer, ServiceDeleteSerializer, ServiceUpdateSerializer

from utils.logger import get_logger

logger = get_logger(__name__)

@extend_schema_view(
    list=extend_schema(
        responses={200: ServiceReadSerializer(many=True)},
    ),
    retrieve=extend_schema(
        responses={200: ServiceReadSerializer},
    ),
    partial_update=extend_schema(
        request=ServiceUpdateSerializer,
        responses={200: ServiceReadSerializer}
    ),
    destroy=extend_schema(
        responses={200: ServiceDeleteSerializer}
    )
)
class ServiceViewSet(GenericViewSet):
    permission_classes = [ServicePermission]
    
    def get_queryset(self):
        return Service.objects.all()
    
    def list(self, request):
        logger.info(f"Listing services - user_id: {request.user.id}")
        services = ServiceService.list_services() 
        
        return Response(
            data=ServiceReadSerializer(services, many=True).data,
            status=200
        )
    
    def retrieve(self, request, pk: UUID):
        logger.info(f"Retrieving service - user_id: {request.user.id}, pk: {pk}")
        service = self.get_object() 
        
        return Response(
            ServiceReadSerializer(service).data, 
            status=200
        )
    
    def partial_update(self, request, pk: UUID):
        logger.info(f"Updating service - user_id: {request.user.id}, pk: {pk}")
        service = self.get_object()

        serializer = ServiceUpdateSerializer(service, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        service = ServiceService.update_service(service, serializer.validated_data)
        
        return Response(
            ServiceReadSerializer(service).data, 
            status=200
        )

    
    def destroy(self, request, pk: UUID):
        logger.info(f"Destroying service - user_id: {request.user.id}, pk: {pk}")
        service = self.get_object()
        ServiceService.destroy_service(service)
        
        serializer = ServiceDeleteSerializer({
            "message": "Service deleted successfully",
            "deleted_id": pk
        })
        
        return Response(
            serializer.data,
            status=200
        )