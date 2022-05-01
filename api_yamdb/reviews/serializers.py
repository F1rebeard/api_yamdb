from rest_framework import serializers
from django.db.models import Avg

from .models import Category, Genre, Title
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
    Сериализатор модели тайтлов.
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

    # def to_internal_value(self, data):
    #     name = data.get('name')
    #     if not name:
    #         raise serializers.ValidationError({
    #             'name': 'This field is required.'
    #         })
    #     year = data.get('year')
    #     if not year:
    #         raise serializers.ValidationError({
    #             'year': 'This field is required.'
    #         })
    #     genre = data.get('genre')
    #     if not genre:
    #         raise serializers.ValidationError({
    #             'genre': 'This field is required.'
    #         })
    #     category = data.get('category')
    #     if not category:
    #         raise serializers.ValidationError({
    #             'category': 'This field is required.'
    #         })
    #     genre_array = Genre.objects.values_list('slug', flat=True)
    #     data_copy = data.copy()
    #     genre_list = []
    #     genre = ''
    #     genre_slugs = data_copy.pop('genre')
    #     for slug in genre_slugs:
    #         if slug in genre_array:
    #             genre = Genre.objects.get(slug=slug)
    #             genre_list.append(genre)
    #         else:
    #             raise serializers.ValidationError({
    #                 'genre': f'Genre {slug} is not in DB'
    #             })
    #     data_copy['genre'] = genre_list
    #     category_slug = data_copy.get('category')
    #     category_array = Category.objects.values_list('slug', flat=True)
    #     if category_slug in category_array:
    #         category = Category.objects.get(slug=category_slug)
    #     else:
    #         raise serializers.ValidationError({
    #                 'category': f'category {category_slug} is not in DB'
    #             })
    #     data_copy['category'] = category
    #     return data_copy

    # def create(self, validated_data):
    #     genre_list = validated_data.pop('genre')
    #     title = Title.objects.create(**validated_data)
    #     for genre_name in genre_list:
    #         genre = Genre.objects.get(name=genre_name)
    #         GenreTitle.objects.create(genre=genre, title=title)
    #     return title

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
