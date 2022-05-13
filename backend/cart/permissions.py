from rest_framework.permissions import BasePermission


class IsAdminOrCustomer(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_authenticated and request.user.is_staff or
                    request.user.is_authenticated and request.user == obj.user)
