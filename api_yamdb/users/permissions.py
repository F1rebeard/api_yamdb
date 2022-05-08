from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Данный Пермишен предоставляет доступ ко всем CRUD операциям c объектом
    только при наличии у пользователя флага .is_admin или is_superuser
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Данный Пермишен предоставляет доступ к чтению всем пользователям,
    а ко всем CRUD операциям c объектом только при наличии
    у пользователя флага .is_admin или is_superuser
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )


class IsAdminOrModerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return(
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_moderator)
                )
        )
