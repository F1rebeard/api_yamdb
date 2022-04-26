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
    # Эндпоинт для отправки кода подтверждения регистрации на указанный email
    path('auth/signup/', views.APISignUp.as_view(), name='signup'),
    # Эндпоинт для получения JWT-токена
    path('auth/token/', views.APIReceiveToken.as_view(), name='get_token'),
    # Роутер для CRUD-операций с моделями пользователей для администратора
    path('', include(router.urls)),
]
