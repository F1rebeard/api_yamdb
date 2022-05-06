from rest_framework import viewsets, mixins


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
