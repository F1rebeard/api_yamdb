from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(
    prefix='users',
    viewset=views.UserViewSet,
    basename='users',
)
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
    # Эндпоинт для отправки кода подтверждения на указанный email (регистрация)
    path('auth/signup/', views.APISignUp.as_view()),
    # Эндпоинт для получения JWT-токена (аторизация)
    path('auth/token/', views.APISignIn.as_view()),
    # Эндпоинт для чтения и редактирования персональных атрибутов пользователя
    path('users/me/', views.APIUserInfo.as_view()),
    # Роутер для CRUD-операций с моделью пользователя
    path('', include(router.urls)),
]
