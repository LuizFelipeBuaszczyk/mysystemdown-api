from django.shortcuts import get_object_or_404
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from uuid import UUID

from iam.permissions.bot_permissions import BotPermission

from systems.services.bot_service import BotService
from systems.models import System, Bot
from systems.serializers.bot_serializer import BotReadSerializer, BotWriteSerializer, BotReadCreateSerializer, BotDeleteSerializer

from utils.logger import get_logger

logger = get_logger(__name__)

@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="system_pk",
                type=UUID,
                location=OpenApiParameter.PATH,
                description="System's UUID"
            ),
        ]
    ),
    create=extend_schema(
        request=BotWriteSerializer,
        responses={201: BotReadCreateSerializer},
        parameters=[
            OpenApiParameter(
                name="system_pk",
                type=UUID,
                location=OpenApiParameter.PATH,
                description="System's UUID"
            ),
        ]
    ),
    destroy=extend_schema(
        responses={200: BotDeleteSerializer},
        parameters=[
            OpenApiParameter(
                name="system_pk",
                type=UUID,
                location=OpenApiParameter.PATH,
                description="System's UUID"
            ),
            OpenApiParameter(
                name="id",
                type=UUID,
                location=OpenApiParameter.PATH,
                description="Bot's UUID"
            ),
        ]
    )
)
class BotViewSet(GenericViewSet):
    permission_classes = [BotPermission]
    
    ## Declara qual serializer será utilizado de acordo com a ação
    def get_serializer_class(self):
        if self.action == "create":
            return BotWriteSerializer
        return BotReadSerializer
    
    def list(self, request, system_pk: UUID):
        logger.info(f"Listing bots - user_id: {request.user.id}, system_pk: {system_pk}")
        system = get_object_or_404(System, id=system_pk)
        bots = BotService.get_all(system=system)
        
        return Response(
            data=BotReadSerializer(bots, many=True).data,
            status=status.HTTP_200_OK
        )
    
    def create(self, request, system_pk: UUID):
        logger.info(f"Create bot - user_id: {request.user.id}, system_pk: {system_pk}")
        system = get_object_or_404(System, id=system_pk)

        serializer = BotWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bot = BotService.create_bot(
            data=serializer.validated_data,
            system=system
        )
        
        return Response(
            BotReadCreateSerializer(bot).data,
            status=status.HTTP_201_CREATED
        )