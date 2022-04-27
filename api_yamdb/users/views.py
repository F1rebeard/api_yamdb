from django.core.mail import EmailMessage
from rest_framework import viewsets, views, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    UserSerializer,
    SignUpSerializer,
    ReceiveTokenSerializer,
    UserInfoUpdateSerializer,
)
from .models import User
from .permissions import IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для CRUD-операций с моделями пользователей.
    Права доступа: администратор. Пример запроса:

    DELETE /v1/users/<username>/ HTTP/1.1

    По url /v1/users/me/ для авторизованного пользователя
    доступно чтение и изменение собственных атрибутов. Пример запроса:

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
    permission_classes = (permissions.IsAuthenticated, IsAdmin)
    filter_backends = (SearchFilter, )
    search_fields = ('username', )

    @action(
        methods=['GET', 'PATCH'],
        url_path='me',
        detail=False,
        permission_classes=(permissions.IsAuthenticated, ),
    )
    def user_info_update(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UserSerializer(
                    request.user,
                    data=request.data,
                    partial=True
                )
            else:
                serializer = UserInfoUpdateSerializer(
                    request.user,
                    data=request.data,
                    partial=True
                )

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class APISignUp(views.APIView):
    """
    Вью-фукнция для получения запроса на отправку на почту кода подтверждения.
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
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            to=[data['address']]
        )
        email.send()

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            data = {
                'subject': 'Код подтвержения к API_YAMDB',
                'body': (
                    'Код доступа к аккаунту '
                    f'{user.username}: {user.confirmation_code}'
                ),
                'address': user.email
            }
            self.send_email(data)
            return Response(serializer.data, status=status.HTTP_200_OK)


class APIReceiveToken(views.APIView):
    """
    Вью-фукнция для получения JWT-токена. Для получения требуется
    предоставить валидные username и confirmation code.
    Права доступа: неавторизованный пользователь. Пример  запроса:

    POST /v1/auth/token/ HTTP/1.1
    {
        "username": "foo",
        "confirmation_code": "bar"
    }
    """

    def post(self, request):
        serializer = ReceiveTokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data

        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response(
                {'token': str(token)},
                status=status.HTTP_201_CREATED
            )

        return Response(
            {'confirmation_code': 'Некорректный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST,
        )
