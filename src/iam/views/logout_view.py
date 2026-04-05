from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter


from iam.services.auth_service import AuthService

@extend_schema_view(
    post=extend_schema(
        request=None,
        responses={
            204: None
        },
        parameters=[
            OpenApiParameter(location=OpenApiParameter.COOKIE, name="refresh_token", required=True, description="Refresh token to invalidate")
        ]
    )
)
class LogoutView(APIView):

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        
        AuthService.logout(
            data={"refresh_token": refresh_token}
        )

        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("refresh_token", path="/")
        response.delete_cookie("auth_token", path="/")
        
        return response