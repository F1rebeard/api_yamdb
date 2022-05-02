from rest_framework import viewsets, status, mixins, filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from users.permissions import IsAdminOrReadOnly
from .filters import TitleSearchFilter
from .models import Title, Category, Genre
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
    """
    Кастомный миксин для создания, запроса списка и удаления объектов.
    """
    pass


class TitleViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для произведений.
    """
    queryset = Title.objects.all()
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
