from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission

from users.models import USER, ADMIN, MODERATOR


User = get_user_model()


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.role == ADMIN
                    or request.user.is_superuser)
        return False


class IsModerator(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == MODERATOR:
                return True
        return False


class IsUser(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == USER:
                return True
        return False


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return obj.author == request.user
        return False


class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return (request.user.is_staff
                    or request.user.is_superuser)
        return False


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return (request.user.role == ADMIN
                    or request.user.is_superuser)


class ReviewCommentPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return not request.user.is_anonymous()

        if request.method in ('PATCH', 'DELETE'):
            return (request.user == obj.author
                    or request.user.role == ADMIN
                    or request.user.role == MODERATOR)

        if request.method in permissions.SAFE_METHODS:
            return True
        return False
