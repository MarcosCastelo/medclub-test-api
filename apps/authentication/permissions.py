from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser

class IsGroupMemberOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            user_group_names = [group.name for group in request.user.groups.all()]
            return any(group in user_group_names for group in view.required_groups)
        return False

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user or request.user.is_superuser

class IsGroupMemberOrOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.user == request.user
        if request.user.is_authenticated:
            user_group_names = [group.name for group in request.user.groups.all()]
            if any(group in user_group_names for group in view.required_groups) or request.user.is_superuser:
                return True
        return obj.user == request.user