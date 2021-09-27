from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Role based permission to only allow admins to this resource
    """

    def has_permission(self, request, view):
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser