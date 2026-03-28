import pytest
import json
from django.urls import reverse
from django_tenants.utils import schema_context

from systems.models import System

@pytest.mark.django_db
def test_create_system_success(tenant_client, system_post_data):
    url = reverse("systems-list")
    response = tenant_client.post(
        path=url, 
        data=json.dumps(system_post_data), 
        content_type="application/json"
        )

    
    assert response.status_code == 201
    
    with schema_context(tenant_client.tenant.schema_name):
        system = System.objects.get(id=response.data["id"])
    
    assert system is not None
    assert system.name == system_post_data["name"]
    assert system.description == system_post_data["description"]
    
    