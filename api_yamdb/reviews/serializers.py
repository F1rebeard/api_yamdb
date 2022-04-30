from rest_framework import serializers

from reviews.models import Category, Genre, Title, GenreTitle


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


class TitleCategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор модели категорий.
    """
    #def to_internal_value(self, data):
    #    try:
    #        category_slug = data
    #        category = Category.objects.get(slug=category_slug)
    #        data = category
    #    except Category.DoesNotExist:
    #        raise serializers.ValidationError(
    #            f'Категории {category_slug} нет в базе'
    #        )
    #    return data

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


class TitleGenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели жанров.
    """
    # def to_internal_value(self, data):
    #     try:
    #         genre_slugs = data
    #         for slug in genre_slugs:
    #             genre = Genre.objects.get(slug=slug)
    # 
    #             
    #         data['slug'] = category
    #     except Category.DoesNotExist:
    #         raise serializers.ValidationError(
    #             f'Категории {category_slug} нет в базе'
    #         )
    #     return data
    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )


class GenreTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenreTitle
        fields = (
            'title',
            'genre',
        )


class TitleSerializer(serializers.ModelSerializer):
    """
    Сериализатор для тайтлов.
    """

    id = serializers.IntegerField(required=False)
    rating = serializers.SerializerMethodField()
    description = serializers.CharField(required=False)
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer()

    def to_internal_value(self, data):
        name = data.get('name')
        if not name:
            raise serializers.ValidationError({
                'name': 'This field is required.'
            })
        year = data.get('year')
        if not year:
            raise serializers.ValidationError({
                'year': 'This field is required.'
            })
        genre = data.get('genre')
        if not genre:
            raise serializers.ValidationError({
                'genre': 'This field is required.'
            })
        category = data.get('category')
        if not category:
            raise serializers.ValidationError({
                'category': 'This field is required.'
            })
        genre_array = Genre.objects.values_list('slug', flat=True)
        data_copy = data.copy()
        genre_list = []
        genre = ''
        genre_slugs = data_copy.pop('genre')
        for slug in genre_slugs:
            if slug in genre_array:
                genre = Genre.objects.get(slug=slug)
                genre_list.append(genre)
            else:
                raise serializers.ValidationError({
                    'genre': f'Genre {slug} is not in DB'
                })
        data_copy['genre'] = genre_list
        category_slug = data_copy.pop('category')
        category_array = Category.objects.values_list('slug', flat=True)
        if category_slug in category_array:
            category = Category.objects.get(slug=category_slug)
        else:
            raise serializers.ValidationError({
                    'category': f'category {category_slug} is not in DB'
                })
        data_copy['category'] = category
        return data_copy

    def create(self, validated_data):
        genre_list = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre_name in genre_list:
            genre = Genre.objects.get(name=genre_name)
            GenreTitle.objects.create(genre=genre, title=title)
        return title

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
        return 1  # Дописать рассчет рейтинга, когда будет модель ревью


class TitleCreateChangeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания/изменения тайтлов.
    """

    description = serializers.CharField(required=False)
    genre = TitleGenreSerializer(many=True)  # serializers.ListField()
    category = CategorySerializer()  # serializers.CharField()

    class Meta:
        model = Title
        fields = (
            'name',
            'year',
            'description',
            'genre',
            'category',
        )


    # def create(self, validated_data):
    #     category = validated_data.pop('category')
    #     category = Category.objects.get(name=category)
    #     validated_data['category'] = category
    #     # genres = validated_data.pop('genre')
    #     title = Title.objects.create(**validated_data)
    #     # for genre_name in genres:
    #     #     try:
    #     #         genre = Genre.objects.get(name=genre_name)
    #     #         GenreTitle.objects.create(genre=genre, title=title)
    #     #     except Exception:  # Category.DoesNotExist:
    #     #         print('Такого жанра в базе нет.')
    #     return title
#
    # def get_genre(self, obj):
    #     genres = obj.pop('genre')
    #     genre_list = []
    #     for genre_name in genres:
    #         try:
    #             genre = Genre.objects.get(name=genre_name)
    #             genre_list.append(genre)
    #         except Exception:  # Category.DoesNotExist:
    #             print('Такого жанра в базе нет.')
    #     return genre_list