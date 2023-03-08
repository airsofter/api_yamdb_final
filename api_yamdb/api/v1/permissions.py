"""Классы разрешений для приложения API."""
from rest_framework import permissions


class AuthorizedOrModeratorPermission(permissions.BasePermission):
    """Класс для контроля доступа к данным."""

    def has_object_permission(self, request, view, obj):
        return (
                    request.user.role == ('moderator' or 'admin')
                    or request.user == obj.user
        )


class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    """Разрешение для админа и суперюзера"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated and (request.user.is_staff
                                               or request.user.is_superuser)
        )
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsAuthorOrModeRatOrOrAdminOrReadOnly(
    permissions.IsAuthenticatedOrReadOnly
):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )