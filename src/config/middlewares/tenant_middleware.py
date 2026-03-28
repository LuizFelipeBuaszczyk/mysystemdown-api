from django.http import Http404
from django.db import connection
from tenants.models import Domain

class TenantMiddleware:
    TENANT_NOT_FOUND_EXCEPTION = Http404
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        connection.set_schema_to_public()

        tenant_header = request.headers.get("X-Tenant")

        if tenant_header:
            try:
                domain: Domain = Domain.objects.get(domain=tenant_header)
                request.tenant = domain.tenant
                connection.set_tenant(domain.tenant)
            except Domain.DoesNotExist:
                raise Http404("Tenant not found")
        else:
            domain: Domain = Domain.objects.get(domain='public')
            request.tenant = domain.tenant

        
        try:
            response = self.get_response(request)
        finally:
            connection.set_schema_to_public()

        return response
        