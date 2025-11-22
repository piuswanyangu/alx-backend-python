from rest_framework import permissions
class IsOwnerOfObject(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # write permissions are only allowed to owner of the object
        return obj.owner == request.user
    