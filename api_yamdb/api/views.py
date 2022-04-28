from django.core.mail import EmailMessage
from rest_framework import viewsets, views, permissions, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Title, Category, Genre
from users.models import User
from .permissions import IsAdmin
from .serializers import (
    UserSerializer,
    SignUpSerializer,
    SignInSerializer,
    UserInfoUpdateSerializer,
    TitleSierializer,
    CategorySerializer,
    GenreSerializer,
)


class APISignUp(views.APIView):
    """
    Вью-фукнция для получения запроса для отправки на почту кода подтверждения.
    Для получения требуется предоставить валидные email и username.
    Права доступа: неавторизованный пользователь. Пример запроса:
    POST /v1/auth/signup/ HTTP/1.1
    {
        "email": "foo@mail.com",
        "username": "foo"
    }
    """
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def send_email(message):
        EmailMessage(
            subject=message.get('subject'),
            body=message.get('body'),
            to=[message.get('address')]
        ).send()

    def post(self, request):
        # Сериализация полученных от пользователя данных и
        # извлечение из них никнейма и электронной почты
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # В случае успешной валидации данных в
            # БД создается экземпляр пользователя
            user = serializer.save()
            # Далее на указанную почту отправляется код
            # подтверждения, необходимый для авторизации
            message = {
                'subject': 'Код подтвержения к API_YAMDB',
                'body': (
                    'Код доступа к аккаунту '
                    f'{user.username}: {user.confirmation_code}'
                ),
                'address': user.email
            }
            self.send_email(message)
            return Response(serializer.data, status=status.HTTP_200_OK)


class APISignIn(views.APIView):
    """
    Вью-фукнция для получения JWT-токена. Для получения требуется
    предоставить валидные никнейм и код подтверждения пользователя.
    Права доступа: неавторизованный пользователь. Пример  запроса:

    POST /v1/auth/token/ HTTP/1.1
    {
        "username": "foo",
        "confirmation_code": "bar"
    }
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        # Сериализация полученных от пользователя данных
        # получения из них кода подтверждения и никнейма пользователя
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data.get('username')
            code = serializer.validated_data.get('confirmation_code')

        # Поиск пользователя в базе данных
        if not User.objects.filter(username=username).exists():
            return Response(
                {'username': f'"{username}" пользователь не найден'},
                status=status.HTTP_404_NOT_FOUND,
            )
        user = User.objects.get(username=username)

        # Валидация кода подтверждения присланного пользователем
        if code == user.confirmation_code:
            # В случае успеха пользователь получает JWT-токен
            token = RefreshToken.for_user(user).access_token
            return Response(
                {'token': token},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {'confirmation_code': 'Некорректный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST,
        )


class APIUserInfo(views.APIView):
    """
    Вью-фукнция для чтения и изменения собственных
    пользовательских атрибутов. Права доступа:
    авторизованный пользователь. Пример запроса:

    PATCH /v1/users/me/ HTTP/1.1
    Content-Type: application/json
    {
        "bio": "foo",
        "first_name": "bar"
    }
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserInfoUpdateSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для CRUD-операций с моделями пользователей.
    Права доступа: администратор. Пример запроса:

    DELETE /v1/users/<username>/ HTTP/1.1
    """
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin)
    filter_backends = (SearchFilter, )
    search_fields = ('username', )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSierializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
