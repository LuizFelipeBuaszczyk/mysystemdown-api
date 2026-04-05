import jwt
import hashlib
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from iam.exceptions import InvalidCredentialsError, UserInactiveError, AccountNotVerifiedError, InvalidTokenError
from config.exceptions import BusinessRuleError
from infra.cache.redis import RedisCache

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
        
        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)
        lifetime = refresh_token.lifetime.total_seconds()
        refresh_token = str(refresh_token)
        
        token = jwt.decode(refresh_token, options={"verify_signature": False})
        RedisCache.set(f"refresh_token:{token['jti']}", hashlib.sha256(refresh_token.encode()).hexdigest(), timeout=lifetime)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        
    @staticmethod
    def logout(data: dict):
        logger.debug(f"Starting AuthService logout - refresh_token: {data['refresh_token']}")
        if not data.get("refresh_token"):
            raise InvalidTokenError("Refresh token is required")
        
        token = jwt.decode(data["refresh_token"], options={"verify_signature": False})
        return RedisCache.delete(f"refresh_token:{token['jti']}")
        

    @staticmethod
    def refresh_token(data: dict):
        logger.debug(f"Starting AuthService refresh_token - refresh_token: {data['refresh_token']}")
        try:
            token = jwt.decode(data["refresh_token"], options={"verify_signature": False})
            refresh_token = RedisCache.get(f"refresh_token:{token['jti']}")
            if refresh_token != hashlib.sha256(data["refresh_token"].encode()).hexdigest():
                raise InvalidTokenError("Refresh token is invalid or expired")
            
            refresh = RefreshToken(data["refresh_token"])

            return {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),  
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