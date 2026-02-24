from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group
from iam.models import Membership
from iam.utils.viewaction_map import get_perm

class SystemPermission(BasePermission):
    
    def has_permission(self, request, view):
        codename = get_perm(view.action)
        return Group.objects.filter(
            memberships__user=request.user,
            memberships__tenant=request.tenant,
            permissions__codename=codename + "_system"
        ).exists()
    
    def has_object_permission(self, request, view, obj):
        
        membership = Membership.objects.filter(
            user=request.user,
            tenant=request.tenant
        ).select_related("group").first()

        if not membership:
            return False

        role = membership.group

        action_perm_map = {
            "retrieve": "view_system",
            "update": "change_system",
            "partial_update": "change_system",
            "destroy": "delete_system",
        }

        required_perm = action_perm_map.get(view.action)

        if not required_perm:
            return False

        return role.permissions.filter(codename=required_perm).exists()