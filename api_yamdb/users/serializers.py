from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели пользователя
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

class SignUpSerializer(serializers.ModelSerializer):
    """
    Сериализатор данных, необходимых для создания пользователя
    """
    class Meta:
        model = User
        fields = ('email', 'username')


class GetTokenSerializer(serializers.ModelSerializer):
    """
    Сериализатор данных, для авторизации пользователя
    """
    username = serializers.CharField(
        required=True)
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )