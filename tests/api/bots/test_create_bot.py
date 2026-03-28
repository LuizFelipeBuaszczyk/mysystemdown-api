import pytest
import json
from django.urls import reverse
from django_tenants.utils import schema_context
from systems.models import Bot
from iam.authentication.token_auth import PREFIX_BOT_TOKEN

@pytest.mark.django_db
def test_create_bot_success(tenant_client, bot_post_data, system):    
    with schema_context(tenant_client.tenant.schema_name):
        system.save()
        
    url = reverse("system-bots-list", kwargs={"system_pk": system.id})
    
    response = tenant_client.post(
        path=url, 
        data=json.dumps(bot_post_data), 
        content_type="application/json"
    )
    
    assert response.status_code == 201
    
    with schema_context(tenant_client.tenant.schema_name):
        bot = Bot.objects.get(id=response.data["id"])
    
    assert bot is not None
    assert bot.bot_name == bot_post_data["bot_name"]
    assert f"{PREFIX_BOT_TOKEN}{bot.prefix_token}" == response.data["api_token"][:14]