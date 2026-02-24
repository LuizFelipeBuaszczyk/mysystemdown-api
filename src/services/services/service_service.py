from uuid import UUID

from services.repositories.service_repository import ServiceRepository
from systems.models import Service

from utils.logger import get_logger

logger = get_logger(__name__)

class ServiceService:
    
    @staticmethod
    def get_service(service_id: UUID):
        logger.info(f"Starting ServiceService get_service - service_id: {service_id}")
        return ServiceRepository.get_by_id(service_id)
    
    @staticmethod
    def update_service(service: Service, data: dict):
        logger.info(f"Starting ServiceService update_service - service_id: {service.id}")

        # Setando os campos
        for field, value in data.items():
            setattr(service, field, value)

        return ServiceRepository.save(service)
    
    @staticmethod
    def destroy_service(service: Service):      
        logger.info(f"Starting ServiceService destroy_service - service_id: {service.id}")  
        return ServiceRepository.destroy(service)
    