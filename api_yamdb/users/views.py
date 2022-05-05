from django.core.mail import EmailMessage
from rest_framework import viewsets, views, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    UserSerializer,
    SignUpSerializer,
    SignInSerializer,
    UserInfoUpdateSerializer,
)
from .models import User
from .permissions import IsAdmin


class APISignUp(views.APIView):
    """
    Вью-фукнция для получения запроса для отправки на почту кода подтверждения.
    Для получения требуется предоставить валидные email и username.
    Права доступа: неавторизованный пользователь. Пример запроса:
    POST /v1/auth/signup/ HTTP/1.1
    Content-Type: application/json
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
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
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
    Content-Type: application/json
    {
        "username": "foo",
        "confirmation_code": "bar"
    }
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        token = serializer.validated_data.get('confirmation_code')
        if not User.objects.filter(username=username).exists():
            return Response(
                {'username': f'"{username}" пользователь не найден'},
                status=status.HTTP_404_NOT_FOUND,
            )
        user = User.objects.get(username=username)
        if user.confirmation_code == token:
            token = RefreshToken.for_user(user).access_token
            return Response(
                {'token': str(token)},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {'confirmation_code': 'Некорректный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для CRUD-операций с моделями пользователей.
    Права доступа: администратор. Пример запроса:

    DELETE /v1/users/<username>/ HTTP/1.1

    По url /v1/users/me/ доступно чтение и изменение
    собственных пользовательских атрибутов. Права доступа:
    авторизованный пользователь. Пример запроса:

    PATCH /v1/users/me/ HTTP/1.1
    Content-Type: application/json
    {
        "bio": "foo",
        "first_name": "bar"
    }
    """
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, )
    filter_backends = (SearchFilter, )
    search_fields = ('username', )

    @action(methods=['GET', 'PATCH'], detail=False, url_path='me',
            permission_classes=(permissions.IsAuthenticated, ))
    def user_info(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = UserInfoUpdateSerializer(
                request.user,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
