from rest_framework import permissions


class IsModer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False

class IsOwnerAndNotModer(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.groups.filter(name='moders').exists()

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
