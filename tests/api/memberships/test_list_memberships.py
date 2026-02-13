import pytest
from django.urls import reverse
from django_tenants.utils import schema_context

@pytest.mark.django_db
def test_list_empty_memberships(tenant_client, auth_user):
    """Apenas o owner do tenant deve aparecer"""
    url = reverse("tenant-memberships-list")
    
    response = tenant_client.get(path=url)
    
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["user"]["id"] == str(auth_user.id)
    
@pytest.mark.django_db
def test_list_memberships(tenant_client, memberships, auth_user):
    """Deve retornar o owner sendo o primeiro da lista e os demais usuários"""
    with schema_context(tenant_client.tenant.schema_name):
        for membership in memberships:
            membership.user.save()
            membership.save()
            
    url = reverse("tenant-memberships-list")
    
    response = tenant_client.get(path=url)
    print(response)
    assert response.status_code == 200
    assert len(response.data) == 3
    assert response.data[0]["user"]["id"] == str(auth_user.id)
    assert response.data[1]["user"]["id"] == str(memberships[0].user.id)
    assert response.data[2]["user"]["id"] == str(memberships[1].user.id)