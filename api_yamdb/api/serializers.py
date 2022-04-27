from rest_framework import serializers

from ..reviews.models import Cathegory, Genre, Title


class CathegorySerializer(serializers.ModelSerializer):
    """
    Сериализатор модели категорий.
    """
    class Meta:
        model = Cathegory
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
    class Meta:
        model = Title
        fields = (
            'name',
            'year',
            'category',
        )
