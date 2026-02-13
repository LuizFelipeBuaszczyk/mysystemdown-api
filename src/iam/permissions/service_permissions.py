from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group
from iam.utils.viewaction_map import get_perm

from iam.authentication.token_auth import TokenAuthentication

BOT_ACTIONS = ["list"]
class ServicePermission(BasePermission):
    
    def has_permission(self, request, view):
        system_pk = view.kwargs.get('system_pk', None)
        
        codename = get_perm(view.action)
        
        if not request.user.is_authenticated:
            if view.action not in BOT_ACTIONS:
                return False
            return TokenAuthentication.validate_bot_token(request.headers, system_pk=system_pk)
        
        return Group.objects.filter(
            memberships__user=request.user,
            memberships__tenant=request.tenant,
            permissions__codename=f"{codename}_service"
        ).exists()
              

    def has_object_permission(self, request, view, obj):       
        service = obj.system.memberships.filter(
            user=request.user
        ).select_related("group").first()
        
        if not service:
            return False
        
        role = service.group

        action_perm_map = {
            "retrieve": "view_service",
            "update": "change_service",
            "partial_update": "change_service",
            "destroy": "delete_service",
        }

        required_perm = action_perm_map.get(view.action)

        if not required_perm:
            return False

        return role.permissions.filter(codename=required_perm).exists()