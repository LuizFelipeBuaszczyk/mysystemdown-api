from typing import Callable
from django.db import transaction
from tenants.repositories.client_repository import ClientRepository
from tenants.repositories.domain_repository import DomainRepository
from iam.services.membership_service import MembershipService

from django.contrib.auth.models import Group
from users.models import User

from utils.logger import get_logger

logger = get_logger(__name__)

class TenantService():

    @staticmethod
    def create_tenant(data: dict, user: User):
        logger.info(f"Starting tenant service create_tenant - user_id: {user.id}")
        
        with transaction.atomic():
            client = data["client"]
            client = ClientRepository.create_client(client)

            domain = {
                'domain': client.schema_name,
                'tenant': client
            } 
            domain = DomainRepository.create_domain(domain)

            membership = MembershipService.create_membership(
                data={
                    "user": user,
                    "group": Group.objects.get(name="owner"),
                    "tenant": client
                }
            )

        return {
            "client": client,
            "domain": domain
        }
    
    @classmethod
    def get_tenants_by_user(cls, user: User) -> dict:
        logger.info(f"Starting service get_tenants_by_user - user_id: {user.id}")
        clients = ClientRepository.get_clients_by_user_id(user.id)
        return clients

    @classmethod
    def get_tenant(cls, user: User, get_object: Callable) -> dict:
        logger.info(f"Starting service get_tenant - user_id: {user.id}")
        
        
        return get_object()