from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group

from iam.utils.viewaction_map import get_perm
from systems.models import Bot
from iam.models import Membership

class BotPermission(BasePermission):
    
    def has_permission(self, request, view):
        codename = get_perm(view.action)
        return Group.objects.filter(
            memberships__user=request.user,
            memberships__tenant=request.tenant,
            permissions__codename=f"{codename}_bot"
        ).exists()
    
    def has_object_permission(self, request, view, obj):
        member = Membership.objects.filter(
            user=request.user,
            tenant=request.tenant
        ).select_related("group").first()

        if not member:
            return False

        role = member.group

        action_perm_map = {
            "retrieve": "view_bot",
            "update": "change_bot",
            "partial_update": "change_bot",
            "destroy": "delete_bot",
        }

        required_perm = action_perm_map.get(view.action)

        if not required_perm:
            return False

        return role.permissions.filter(codename=required_perm).exists()