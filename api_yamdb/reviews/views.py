from rest_framework import viewsets, views, permissions, status, mixins, filters
from rest_framework.response import Response
from reviews.models import Title, Category, Genre, GenreTitle
from .serializers import (
    TitleSerializer,
    CategorySerializer,
    GenreSerializer,
)


class GetPostDelViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet
        ):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (filters.SearchFilter, )
    search_fields = (
        'name',
        'year',
        'category__slug',
        'genre__slug'
    )

    # def get_serializer_class(self):
    #     if self.action != 'list':
    #         return TitleCreateChangeSerializer
    #     return TitleSierializer

    # def create(self, request):
    #     title_data = request.data
    #     if "name" not in title_data:
    #         raise AssertionError('Expected name field')
    #     category_slug = title_data.get('category')
    #     category = Category.objects.get(slug=category_slug)
    #     # title_data['category'] = category
    #     genres = title_data.get('genre')
    #     title = Title.objects.create(
    #         name=title_data["name"],
    #         year=title_data["year"],
    #         category=category,
    #         description=title_data["description"],
    #     )
    #     # genre_list = []
    #     for genre_slug in genres:
    #         try:
    #             genre = Genre.objects.get(slug=genre_slug)
    #             GenreTitle.objects.create(genre=genre, title=title)
    #         except Exception:  # Category.DoesNotExist:
    #             print(f'Жанра {genre_slug} в базе нет.')
    #         # try:
    #         #     genre = Genre.objects.get(name=genre_name)
    #         #     genre_list.append(genre)
    #         # except Exception:  # Category.DoesNotExist:
    #         #     print('Такого жанра в базе нет.')
    #     # title_data['genre'] = genre_list
    #     serializer = TitleSerializer(title)
    #     return Response(serializer.data)


class CategoryViewSet(GetPostDelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get', 'post', 'delete']
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)


class GenreViewSet(GetPostDelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    http_method_names = ['get', 'post', 'delete']
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
