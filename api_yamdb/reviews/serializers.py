from rest_framework import serializers

from .models import Category, Genre, Title, GenreTitle


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор модели категорий.
    """
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели жанров.
    """
    class Meta:
        model = Genre
        exclude = ('id',)


class GenreTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenreTitle
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели произведений.
    Year не может быть больше нынешнего года.
    Rating - среднеарифметическое оценок с дочерних Review.
    Genre и Category - на входе при создании принимают slug,
    а на выходе выдают соответствующие объекты.
    """
    rating = serializers.IntegerField(
        default=None,
        read_only=True
    )
    description = serializers.CharField(required=False)
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )


class CreateTitleSerializer(TitleSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
