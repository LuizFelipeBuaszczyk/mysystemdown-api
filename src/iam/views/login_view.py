from config.settings import SIMPLE_JWT

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from iam.serializers.login_serializer import LoginRequestSerializer, LoginResponseSerializer
from iam.services.auth_service import AuthService

from utils.logger import get_logger

logger = get_logger(__name__)

# Create your views here.

class LoginView(APIView):
    
    @extend_schema(
        request=LoginRequestSerializer,
        responses={
            200: LoginResponseSerializer
        }
    )
    def post(self, request):
        logger.info(f"Starting Login")
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        result = AuthService.login(
            data=serializer.validated_data
        )

        response = Response(result, status=status.HTTP_200_OK)
        response.set_cookie(
            key="refresh_token",
            value=result["refresh_token"],
            httponly=True,
            max_age=SIMPLE_JWT.get("REFRESH_TOKEN_LIFETIME").total_seconds(),
            path="/"
        )
        response.set_cookie(
            key="auth_token",
            value=result["access_token"],
            httponly=True,
            max_age=SIMPLE_JWT.get("ACCESS_TOKEN_LIFETIME").total_seconds(),
            path="/"
        )
    
        return response
        