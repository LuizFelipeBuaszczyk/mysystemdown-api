import pytest
from tenants.models import Client, Domain
from rest_framework.test import APIClient
from django.core.management import call_command
from django_tenants.utils import schema_context

@pytest.fixture(autouse=True)
def celery_eager(settings):
    """
    - CELERY_TASK_ALWAYS_EAGER: Serve para desabilitar o .delay() durante os testes, executando-as de forma sincrona
    - CELERY_TASK_EAGER_PROPAGATES: Serve para desabilitar possiveis erros durante a execução da task
    """
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True

@pytest.fixture(autouse=True)
def disable_cache(settings):
    """
    Serve para desabilitar o cache durante os testes, para garantir que os testes sejam executados com o cache desligado
    """
    settings.CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }

@pytest.fixture(scope="session")
def public_tenant(django_db_setup, django_db_blocker):
    """Inicializa setup inicial para os testes.
    ---
    - django_db_setup: Garante que o banco está pronto para os testes
    - django_db_bloquer: Bloqueia o acesso ao banco para os testes
    """
    with django_db_blocker.unblock(): ## Desbloqueia o acesso ao banco 
        tenant, created = Client.objects.get_or_create(
            schema_name="public",
            defaults={"name": "public"}
        )

        Domain.objects.get_or_create(
            domain="public",
            tenant=tenant,
            defaults={"is_primary": True}
        )
        
        if created:
            with schema_context(tenant.schema_name):
                call_command("seed_roles", verbosity=0)
                call_command("seed_group_permissions", verbosity=0)

    return tenant

@pytest.fixture(scope="session")
def auth_user(django_db_setup, django_db_blocker, public_tenant):
    from django_tenants.utils import schema_context
    
    from users.models import User
    with django_db_blocker.unblock():
        with schema_context(public_tenant.schema_name):
            return User.objects.create(
                email="test@test.com",
                password="123456",
                first_name="Test",
                last_name="User"
            )

@pytest.fixture
def public_tenant_client(public_tenant):
    client =  APIClient()
    client.credentials(
        HTTP_X_TENANT=public_tenant.schema_name
    )
    client.tenant = public_tenant
    return client


@pytest.fixture(scope="session")
def tenant1(create_tenant, auth_user):
    tenant = create_tenant(
        schema_name="tenant1",
        domain="tenant1",
        name="Tenant 1",
        user=auth_user
    )
    return tenant
    
    
@pytest.fixture
def tenant_client(tenant1, auth_user):
    from rest_framework_simplejwt.tokens import RefreshToken

    client = APIClient()
    token = RefreshToken.for_user(auth_user)
    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {token.access_token}",
        HTTP_X_TENANT=tenant1.schema_name
    )    
    client.tenant = tenant1
    return client


@pytest.fixture
def public_auth_client(public_tenant_client, auth_user):
    from rest_framework_simplejwt.tokens import RefreshToken

    token = RefreshToken.for_user(auth_user)
    public_tenant_client.defaults["HTTP_AUTHORIZATION"] = f"Bearer {token.access_token}"
    return public_tenant_client

pytest_plugins = [
    "tests.fixtures.user_fixture",
    "tests.fixtures.tenant_fixture",
    "tests.fixtures.system_fixture",
    "tests.fixtures.tenant_fixture",
    "tests.fixtures.service_fixture",
    "tests.fixtures.bot_fixture",
    "tests.fixtures.membership_fixture",
]