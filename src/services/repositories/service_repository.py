from uuid import UUID  

from systems.models import Service

from utils.logger import get_logger

logger = get_logger(__name__)

class ServiceRepository:
    
    @staticmethod
    def get_by_id(service_id: UUID):
        logger.debug(f"Starting ServiceRepository get_by_id - service_id: {service_id}")
        return Service.objects.filter(id=service_id).first()
    
    @staticmethod
    def save(service: Service):
        logger.debug(f"Starting ServiceRepository save - service_id: {service.id}")
        service.save()
        return service

    @staticmethod
    def destroy(service: Service):
        logger.debug(f"Starting ServiceRepository destroy - service_id: {service.id}")
        return service.delete()