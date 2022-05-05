from rest_framework import viewsets, filters

from users.permissions import IsAdminOrReadOnly
from .mixins import GetPostDelViewSet
from .filters import TitleSearchFilter
from .models import Title, Category, Genre
from .serializers import (
    TitleSerializer,
    CategorySerializer,
    GenreSerializer,
)
from django.db.models import Avg


class TitleViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для произведений.
    """
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleSearchFilter


class CategoryViewSet(GetPostDelViewSet):
    """
    Вьюсет для категорий.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class GenreViewSet(GetPostDelViewSet):
    """
    Вьюсет для жанров.
    Поиск по имени.
    Доступ: пользователи с правами ниже администратора
    получают доступ только для чтения.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
