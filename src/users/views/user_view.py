from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema_view, extend_schema
from uuid import UUID

from users.serializers.user_serializer import UserReadSerializer, UserWriteSerializer, UserUpdateSerializer
from users.services.user_service import UserService
from iam.permissions.user_permissions import UserPermission

from utils.logger import get_logger
from users.models import User

logger = get_logger(__name__)

# Create your views here.
@extend_schema_view(
    partial_update=extend_schema(
        request=UserUpdateSerializer,
        responses={
            200: UserReadSerializer
        }
    ),
    create=extend_schema(
        request=UserWriteSerializer,
        responses={201: UserReadSerializer},
    ),
    destroy=extend_schema(
        responses={
            204: None
        }
    )
)
class UserViewSet(GenericViewSet):
    permission_classes = [UserPermission]
    
    def get_queryset(self):
        return User.objects.all()
    
    
    def partial_update(self, request, pk: UUID):
        logger.info(f"Updating user - user_id: {request.user.id}, pk: {pk}")
        user = self.get_object()

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        updated_user = UserService.update_user(user=user, data=serializer.validated_data)
        
        return Response(
            UserReadSerializer(updated_user).data,
            status=status.HTTP_200_OK
        )

    def create(self, request):
        logger.info(f"Create user")
        serializer = UserWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = UserService.create_user(serializer.validated_data)
        
        logger.info("User created")
        return Response(
            UserReadSerializer(user).data,
            status=status.HTTP_201_CREATED
        )
    
    def destroy(self, request, pk: UUID):
        logger.info(f"Destroying user - user_id: {request.user.id}, pk: {pk}")
        user = self.get_object()

        UserService.delete_user(user=user)
        
        return Response(
            status=status.HTTP_204_NO_CONTENT
            )