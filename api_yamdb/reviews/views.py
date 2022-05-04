from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from users.permissions import IsAdminOrReadOnly
from .mixins import GetPostDelViewSet
from .filters import TitleSearchFilter
from .models import Title, Category, Genre
from .serializers import (
    TitleSerializer,
    CreateTitleSerializer,
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

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return CreateTitleSerializer
        return TitleSerializer


class CategoryViewSet(GetPostDelViewSet):
    """
    Вьюсет для категорий.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)

    def destroy(self, request, *args, **kwargs):
        get_object_or_404(Category, slug=kwargs['pk']).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

    def destroy(self, request, *args, **kwargs):
        get_object_or_404(Genre, slug=kwargs['pk']).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
