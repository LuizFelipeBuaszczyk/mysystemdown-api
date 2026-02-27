from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from iam.serializers.confirm_serializer import ConfirmResponseSerializer, ConfirmRequestSerializer
from iam.services.auth_service import AuthService

from utils.logger import get_logger

logger = get_logger(__name__)

@extend_schema_view(
    get=extend_schema(
        summary="Confirm email",
        description="Confirm email",
        responses={
            200: ConfirmResponseSerializer,
        },
        parameters=[
            OpenApiParameter(
                name="token",
                type=str,
                required=True,
                location=OpenApiParameter.QUERY
            )
        ]
    )
)
class ConfirmationEmailView(APIView):
    
    def get(self, request, *args, **kwargs):
        logger.info(f"Starting confirmation email - token: {request.query_params.get('token')}")
        token = request.query_params.get('token', None)
        serializer = ConfirmRequestSerializer(data={"token": token})
        serializer.is_valid(raise_exception=True)
        
        result = AuthService.confirm_user(serializer.validated_data)
        
        data = {
            "message": "Email confirmed"
        }
        
        return Response(
            ConfirmResponseSerializer(data).data, 
            status=status.HTTP_200_OK
        )        