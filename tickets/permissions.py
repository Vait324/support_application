from rest_framework import permissions


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class IsAuthorOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.user.is_staff
