from rest_framework import permissions


class IsAdministrator(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminModerAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.user == obj.author
                or request.user.is_moder
                or request.user.is_admin
                or request.method in permissions.SAFE_METHODS)
