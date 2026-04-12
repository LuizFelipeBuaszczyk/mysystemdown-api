from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, extend_schema_view

from tenants.serializers.tenant_serializer import TenantWriteSerializer, TenantReadSerializer, TenantReadClientSerializer
from tenants.service.tenant_service import TenantService
from tenants.models import Client
from tenants.exceptions import NotFoundTenantError

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
    retrieve=extend_schema(
        responses={200: TenantReadClientSerializer}
    ),
)
class TenantView(GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Client.objects.all()

    def get_object(self):
        try:
            return get_object_or_404(Client, pk=self.kwargs['pk'])
        except Http404:
            logger.warning(f"Tenant not found - tenant_id: {self.kwargs['pk']}")
            raise NotFoundTenantError()
        except Exception as e:
            logger.error(f"Error retrieving tenant - tenant_id: {self.kwargs['pk']}, error: {str(e)}")
            raise e

    def list (self, request):
        logger.info(f"List tenants - user_id: {request.user.id}")
        tenants = TenantService.get_tenants_by_user(request.user)

        logger.debug(f"Tenants found - user_id: {request.user.id}, tenants_count: {tenants.count()}")
        return Response(
            TenantReadClientSerializer(tenants, many=True).data,
            status=status.HTTP_200_OK
        )
    
    def retrieve(self, request, pk=None):
        logger.info(f"Retrieve tenant - user_id: {request.user.id}, tenant_id: {pk}")
        tenant = TenantService.get_tenant(request.user, self.get_object)

        logger.debug(f"Tenant found - user_id: {request.user.id}, tenant_id: {tenant.id}")
        return Response(
            TenantReadClientSerializer(tenant).data,
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