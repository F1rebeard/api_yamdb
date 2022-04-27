from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели пользователя.
    """
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        ]


class UserInfoUpdateSerializer(UserSerializer):
    """
    Сериализатор модели пользователя.
    Изменения статуса (роли) невозможно.
    """
    role = serializers.CharField(read_only=True)


class SignUpSerializer(serializers.ModelSerializer):
    """
    Сериализатор данных для создания экземляра пользователя.
    """
    class Meta:
        model = User
        fields = (
            'email',
            'username',
        )


class SignInSerializer(serializers.ModelSerializer):
    """
    Сериализатор данных для авторизации пользователя.
    """
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code',
        )
