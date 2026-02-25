from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from uuid import UUID

from systems.models import Bot
from iam.permissions.bot_permissions import BotPermission
from bots.services.bot_service import BotService
from bots.serializers.bot_serializer import BotResponseDeleteSerializer, BotUpdateSerializer, BotReadSerializer

from utils.logger import get_logger

logger = get_logger(__name__)


# Create your views here.
@extend_schema_view(
    partial_update=extend_schema(
        request=BotUpdateSerializer,
        responses={
            200:{BotReadSerializer}
        }
    ),
    destroy=extend_schema(
        responses={
            200:{BotResponseDeleteSerializer}
        }
    )
)
class BotViewSet (GenericViewSet):
    permission_classes = [BotPermission]

    def get_queryset(self):
        return Bot.objects.filter(id=self.kwargs.get('pk'))
    
    def partial_update(self, request, pk: UUID):
        logger.info(f"Updating bot - user_id: {request.user.id}, pk: {pk}")
        bot = self.get_object()

        serializer = BotUpdateSerializer(bot, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        bot = BotService.update_bot(bot=bot, data=serializer.validated_data)
        
        return Response(
            BotReadSerializer(bot).data,
            status=status.HTTP_200_OK
        )


    def destroy(self, request, pk: UUID):
        logger.info(f"Destroying bot - user_id: {request.user.id}, pk: {pk}")
        bot = self.get_object()

        BotService.destroy_bot(bot=bot)
        
        serializer = BotResponseDeleteSerializer({
            "message": "Bot deleted successfully",
            "deleted_id": pk
        })
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
            )