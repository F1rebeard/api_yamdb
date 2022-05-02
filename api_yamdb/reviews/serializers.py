from rest_framework import serializers
from django.db.models import Avg

from .models import Category, Genre, Title
from .validators import validate_year
from reviews_and_comments.models import Review


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор модели категорий.
    """
    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )


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


class TitleSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели произведений.
    Year не может быть больше нынешнего года.
    Rating - среднеарифметическое оценок с дочерних Review.
    Genre и Category - на входе при создании принимают slug,
    а на выходе выдают соответствующие объекты.
    """
    rating = serializers.SerializerMethodField()
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
    year = serializers.IntegerField(validators=[validate_year])

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

    def get_rating(self, obj):
        score = Review.objects.filter(
            title_id=obj.id
        ).aggregate(Avg('score'))
        if score['score__avg'] is None:
            return None
        return int(score['score__avg'])

    def to_representation(self, instance):
        data = super(TitleSerializer, self).to_representation(instance)
        genre_list = instance.genre
        genre = []
        for obj in genre_list.all():
            obj_dict = {
                'name': obj.name,
                'slug': obj.slug
            }
            genre.append(obj_dict)
        category = instance.category
        return {
            "id": data['id'],
            "name": data['name'],
            "year": data['year'],
            "rating": data['rating'],
            "description": data['description'],
            "genre": genre,
            "category": {
                'name': category.name,
                'slug': category.slug}
        }
