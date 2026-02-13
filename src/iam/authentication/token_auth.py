import jwt
from django.contrib.auth.hashers import check_password
from django.conf import settings

from iam.exceptions import InvalidApiTokenError, PermissionDenied

from systems.models import Bot
from systems.utils.token import PREFIX_BOT_TOKEN
from systems.repositories.bot_repository import BotRepository

from utils.logger import get_logger

logger = get_logger(__name__)

class TokenAuthentication:
    
    @staticmethod
    def validate_bot_token(header: dict, **kwargs) -> bool :
        logger.debug(f"Starting TokenAuthentication validate_bot_token")
        """Validate API Token for bot"""
        api_token = header.get("api-token", None)
        
        if not api_token:
            raise InvalidApiTokenError()
        
        if not api_token.startswith(PREFIX_BOT_TOKEN):
            raise InvalidApiTokenError()
        
        prefix = api_token[len(PREFIX_BOT_TOKEN):len(PREFIX_BOT_TOKEN)+10]        
        token = api_token[len(PREFIX_BOT_TOKEN) + len(prefix) + 1:]
    
        bot = BotRepository.get_bot_by_prefix(prefix)  
              
        if not bot:
            raise InvalidApiTokenError()
        
        if not check_password(token, bot.api_token):
            raise InvalidApiTokenError()
        
        if kwargs.get('service_pk'):
            if not bot.system.services.filter(id=kwargs.get('service_pk')).exists():
                raise PermissionDenied("You don't have permission to access this service")

        if kwargs.get('system_pk'):
            if not str(bot.system.id) == kwargs.get('system_pk'):
                raise PermissionDenied("You don't have permission to access this system")
        
        return True
    
    @staticmethod
    def create_token_jwt(data: dict) -> str:
        logger.debug(f"Starting TokenAuthentication create_token_jwt - data: {data}")
        return jwt.encode(
            data, 
            settings.SECRET_KEY, 
            algorithm='HS256'
            )
        
    @staticmethod
    def decode_jwt(token: str) -> dict:
        logger.debug(f"Starting TokenAuthentication decode_jwt - token: {token}")
        try:
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=['HS256']
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise InvalidApiTokenError()
        except jwt.InvalidTokenError:
            raise InvalidApiTokenError()