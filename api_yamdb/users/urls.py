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
    path('v1/auth/signup/', views.APISignUp.as_view(), name='signup'),
    path('v1/auth/token/', views.APISignIn.as_view(), name='signin'),
    path('v1/', include(router.urls)),
]
