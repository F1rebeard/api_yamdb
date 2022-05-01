from django.urls import include, path
from rest_framework import routers

from reviews_and_comments.views import ReviewViewSet, CommentViewSet

router_v1 = routers.DefaultRouter()

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('', include(router_v1.urls))
]