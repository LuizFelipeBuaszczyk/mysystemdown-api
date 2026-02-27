from datetime import datetime
from users.repositories.user_repository import UserRepository
from django.conf import settings
from django.contrib.auth.models import Group

from users.models import User
from utils.token import create_token_jwt
from utils.logger import get_logger
from infra.queue.tasks.email import send_email
from infra.email.email import EmailType

logger = get_logger(__name__)

class UserService:

    @staticmethod
    def update_user(user: User, data: dict):
        logger.debug(f"Starting service update_user - user_id: {user.id}")

        for field, value in data.items():
            if field == "password":
                user.previous_password = user.password
                user.password_change_at = datetime.now()
                user.set_password(value)
                
                reset_password_token = create_token_jwt({"id": str(user.id)})
                context = {
                    "username": user.first_name + " " + user.last_name,
                    "reset_password_url": f"{settings.DOMAIN_URL}/auth/password-reset?token={reset_password_token}"
                }
                send_email.delay("Password Changed", user.email, EmailType.RESET_ACCOUNT_PASSWORD.value, context)
                continue



            setattr(user, field, value)

        return UserRepository.save_user(user)
    
    @staticmethod
    def create_user(data: dict):
        logger.debug(f"Starting service create_user - email: {data['email']}")
        group = Group.objects.get(name="user_base")
        
        user = UserRepository.create_user(data)  
        
        confirmation_token = create_token_jwt({"id": str(user.id)})
        context = {
            "username": user.first_name + " " + user.last_name,
            "confirmation_url": f"{settings.DOMAIN_URL}/auth/confirm-email?token={confirmation_token}"
        }
        send_email.delay("Verify your email", user.email, EmailType.CONFIRM_EMAIL_USER.value, context)
        user.groups.add(group)
        return user
    
    @staticmethod
    def delete_user(user: User):
        logger.debug(f"Starting service delete_user - user_id: {user.id}")
        user.is_active = False
        return UserRepository.save_user(user)
        
    @staticmethod
    def get_user_by_email(email: str):
        return UserRepository.get_user_by_email(email)