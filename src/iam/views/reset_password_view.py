from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from iam.serializers.password_serializer import ResetPasswordRequestSerializer, ResetPasswordResponseSerializer
from iam.services.auth_service import AuthService

from utils.logger import get_logger

logger = get_logger(__name__)


@extend_schema_view(
    get=extend_schema(
        responses={
            200: None
        },
        parameters=[
            OpenApiParameter(
                "token",
                type=str,
                required=True,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
)
class ResetPasswordView(APIView):
    
    def get(self, request):
        logger.info(f"Starting reset password - token: {request.query_params.get('token')}")
        serializer = ResetPasswordRequestSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        result = AuthService.reset_password(
            data=serializer.validated_data
        )

        data = {
            "message": "Password reset successfully"
        }
        
        return Response(
            ResetPasswordResponseSerializer(data).data,
            status=status.HTTP_200_OK
        )