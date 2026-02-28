from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


from iam.exceptions import InvalidCredentialsError, UserInactiveError, AccountNotVerifiedError, InvalidTokenError
from config.exceptions import BusinessRuleError

from iam.authentication.token_auth import TokenAuthentication
from users.repositories.user_repository import UserRepository

from utils.logger import get_logger

logger = get_logger(__name__)

class AuthService:
    
    @staticmethod
    def login(data: dict):
        logger.debug(f"Starting AuthService login - email: {data['email']}")
        email = data.get("email")
        password = data.get("password")
        
        user = authenticate(email=email, password=password)
        if not user:
            raise InvalidCredentialsError("Invalid email or password")
        if not user.is_active:
            raise UserInactiveError("User is inactive")
        if not user.is_verified:
            raise AccountNotVerifiedError("User is not verified")
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        return {
            "access_token": access_token,
            "refresh": str(refresh)
        }
        
    @staticmethod
    def refresh_token(data: dict):
        logger.debug(f"Starting AuthService refresh_token - refresh: {data['refresh']}")
        try:
            refresh = RefreshToken(data["refresh"])

            return {
                "access": str(refresh.access_token),
                "refresh": str(refresh),  
            }

        except TokenError:
            raise BusinessRuleError("Refresh token is invalid or expired")
        
    @staticmethod
    def confirm_user(data: dict):
        logger.debug(f"Starting AuthService confirm_user - token: {data['token']}")
        token = data.get("token", "")
        decode_jwt = TokenAuthentication.decode_jwt(token)
        
        if not decode_jwt["id"]:
            raise InvalidTokenError()
                
        user = UserRepository.get_user_by_id(decode_jwt["id"])
        user.is_verified = True
        user.save()
        
        return user
        
    @staticmethod
    def reset_password(data: dict):
        logger.debug(f"Starting AuthService reset_password - token: {data['token']}")
        token = data.get("token", "")
        decode_jwt = TokenAuthentication.decode_jwt(token)
        
        if not decode_jwt["id"]:
            raise InvalidTokenError()
                
        user = UserRepository.get_user_by_id(decode_jwt["id"])

        if not user.previous_password:
            raise BusinessRuleError("Password already reset")

        user.password = user.previous_password
        user.previous_password = None
        
        return UserRepository.save_user(user)