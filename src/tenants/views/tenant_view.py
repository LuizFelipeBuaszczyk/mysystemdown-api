from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, extend_schema_view

from tenants.serializers.tenant_serializer import TenantWriteSerializer, TenantReadSerializer, TenantReadClientSerializer
from tenants.service.tenant_service import TenantService

from utils.logger import get_logger

logger = get_logger(__name__)

# Create your views here.

@extend_schema_view(
    create=extend_schema(
        request=TenantWriteSerializer,
        responses={201: TenantReadSerializer}
    ),
    list=extend_schema(
        responses={200: TenantReadClientSerializer(many=True)}
    ),
)
class TenantView(GenericViewSet):
    permission_classes = [IsAuthenticated]

    def list (self, request):
        logger.info(f"List tenants - user_id: {request.user.id}")
        tenants = TenantService.get_tenants_by_user(request.user)

        logger.debug(f"Tenants found - user_id: {request.user.id}, tenants_count: {tenants.count()}")
        return Response(
            TenantReadClientSerializer(tenants, many=True).data,
            status=status.HTTP_200_OK
        )
    
    def create(self, request):
        logger.info(f"Create tenant - user_id: {request.user.id}")
        serializer = TenantWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        tenant = TenantService.create_tenant(serializer.validated_data, request.user)
        
        return Response(
            TenantReadSerializer(tenant).data,
            status=status.HTTP_201_CREATED
        )