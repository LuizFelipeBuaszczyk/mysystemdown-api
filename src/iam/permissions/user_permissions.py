from rest_framework.permissions import BasePermission

class UserPermission(BasePermission):
    
    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        
        return request.user.id == obj.id
    