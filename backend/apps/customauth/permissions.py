from rest_framework import permissions


class IsCreator(permissions.BasePermission):
    """
    Permission to check if user is a creator.
    """

    def has_permission(self, request, view):
        """Check if user is authenticated and is a creator."""
        return request.user and request.user.is_authenticated and request.user.is_creator()


class IsAdminUser(permissions.BasePermission):
    """
    Permission to check if user is staff or admin.
    """

    def has_permission(self, request, view):
        """Check if user is authenticated and is admin or staff."""
        return request.user and request.user.is_authenticated and request.user.is_admin_user()


class IsStaffUser(permissions.BasePermission):
    """
    Permission to check if user is staff or superuser.
    """

    def has_permission(self, request, view):
        """Check if user is staff or superuser."""
        return request.user and request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission to check if user is the owner or is admin/staff.
    """

    def has_object_permission(self, obj, request, view):
        """Check if user is owner or admin."""
        return obj.user == request.user or request.user.is_admin_user()
