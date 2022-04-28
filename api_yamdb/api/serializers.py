from rest_framework import serializers

from reviews.models import Category, Genre, Title
from users.models import User


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


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор модели категорий.
    """
    class Meta:
        model = Category
        fields = [
            'name',
            'slug',
        ]


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели жанров.
    """
    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )


class TitleSierializer(serializers.ModelSerializer):
    """
    Сериализатор для тайтлов.
    """

    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )

    def get_rating(self, obj):
        return 1  # Дописать рассчет рейтинга, когда будет модель ревью
