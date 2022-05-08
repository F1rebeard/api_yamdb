from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()

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
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='review'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('', include(router.urls)),
]
