from users.models import User
from utils.logger import get_logger

logger = get_logger(__name__)

class UserRepository:
    
    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        logger.debug(f"Starting repository get_user_by_id - user_id: {user_id}")
        return User.objects.get(id=user_id)
    
    @staticmethod
    def create_user(data: dict) -> User:
        logger.debug(f"Starting repository create_user - email: {data['email']}")
        password = data.pop("password")
        user = User(**data)
        user.set_password(password)
        user.save()
        return user
    
    @staticmethod
    def get_user_by_email(email: str):
        return User.objects.filter(email=email).values()
    
    @staticmethod
    def save_user(user: User):
        logger.debug(f"Starting repository save_user - user_id: {user.id}")
        user.save()
        return user