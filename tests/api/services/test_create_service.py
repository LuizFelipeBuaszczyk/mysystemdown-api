import pytest
import json
from django.urls import reverse
from django_tenants.utils import schema_context

from systems.models import Service

@pytest.mark.django_db
def test_create_service_success(tenant_client, service_post_data, system):    
    with schema_context(tenant_client.tenant.schema_name):
        system.save()
        
    url = reverse("system-services-list", kwargs={"system_pk": system.id})
    
    response = tenant_client.post(
        path=url, 
        data=json.dumps(service_post_data), 
        content_type="application/json"
    )
    
    assert response.status_code == 201
    
    with schema_context(tenant_client.tenant.schema_name):
        service = Service.objects.get(id=response.data["id"])
    
    assert service is not None
    assert service.title == service_post_data["title"]
    assert service.url == service_post_data["url"]
    assert service.description == service_post_data["description"]
    assert service.health_check_interval == service_post_data["health_check_interval"]