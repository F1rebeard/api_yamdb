from rest_framework import viewsets, status, mixins, filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from users.permissions import IsAdminOrReadOnly
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
    permission_classes = (IsAdminOrReadOnly,)


class CategoryViewSet(GetPostDelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)

    def destroy(self, request, *args, **kwargs):
        get_object_or_404(Category, slug=kwargs['pk']).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(GetPostDelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)

    def destroy(self, request, *args, **kwargs):
        get_object_or_404(Genre, slug=kwargs['pk']).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)