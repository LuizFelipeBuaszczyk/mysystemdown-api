from config.exceptions import AuthenticationError
from config.exceptions import BusinessRuleError

class InvalidCredentialsError(AuthenticationError):
    default_detail = "Invalid credentials"
    default_code = "invalid_credentials"
    
class PermissionDenied(AuthenticationError):
    default_detail = "Permission denied"
    default_code = "permission_denied"

class InvalidApiTokenError(AuthenticationError):
    default_detail = "Invalid API token"
    default_code = "invalid_api_token"

class UserInactiveError(AuthenticationError):
    default_detail = "User account is inactive"
    default_code = "user_inactive"
    
class AccountNotVerifiedError(AuthenticationError):
    default_detail = "Account not verified"
    default_code = "account_not_verified"
    
class InvalidTokenError(AuthenticationError):
    default_detail = "Invalid token"
    default_code = "invalid_token"