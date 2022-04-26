from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Данный Пермишен предоставляет доступ ко всем CRUD операциям c
    объектом только при наличии у пользователя флага .is_admin
    """
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or request.user.is_superuser
