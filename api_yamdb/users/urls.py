from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(
    prefix='users',
    viewset=views.UserViewSet,
    basename='users',
)

urlpatterns = [
    path('auth/signup/', views.APISignUp.as_view(), name='signup'),
    path('auth/token/', views.APISignIn.as_view(), name='signin'),
    path('', include(router.urls)),
]
