from config.exceptions import NotFoundError

class NotFoundTenantError(NotFoundError):
    default_detail = "Tenant not found"
    default_code = "tenant_not_found"