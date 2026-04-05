from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from iam.serializers.logout_serializer import LogoutSerializer


from iam.services.auth_service import AuthService

@extend_schema_view(
    post=extend_schema(
        request=LogoutSerializer,
        responses={
            204: None
        }
    )
)
class LogoutView(APIView):

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data["refresh_token"]

        AuthService.logout(
            data={"refresh_token": refresh_token}
        )

        response = Response(status=status.HTTP_204_NO_CONTENT)
        
        return response