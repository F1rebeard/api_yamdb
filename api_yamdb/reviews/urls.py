from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views


router = SimpleRouter()

router.register(
    prefix='titles',
    viewset=views.TitleViewSet,
    basename='titles',
)
router.register(
    prefix='categories',
    viewset=views.CategoryViewSet,
    basename='categories',
)
router.register(
    prefix='genres',
    viewset=views.GenreViewSet,
    basename='genres',
)


urlpatterns = [
    path('', include(router.urls)),
]
