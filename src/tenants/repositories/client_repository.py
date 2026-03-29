from uuid import UUID

from tenants.models import Client

from utils.logger import get_logger

logger = get_logger(__name__)

class ClientRepository():

    @staticmethod
    def create_client(data: dict):
        logger.debug(f"Starting repository create_client - name: {data['name']}")
        return Client.objects.create(**data)
    
    @staticmethod
    def get_clients_by_user_id(user_id: UUID):
        logger.debug(f"Starting repository get_clients_by_user_id - user_id: {user_id}")
        return Client.objects.filter(memberships__user_id=user_id)