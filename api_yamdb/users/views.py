from django.core.mail import EmailMessage
from rest_framework import viewsets, views, permissions
from django.http import JsonResponse

from .serializers import UserSerializer, SignUpSerializer
from .models import User

def simpleview(request):
    return JsonResponse({'foo': 'bar'})

class UserViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для CRUD-операций с моделями пользователей.
    Права доступа: администратор. Пример запроса:

    PATCH /v1/users/<username>/ HTTP/1.1
    Content-Type: application/json
    {
        "bio": "foo",
        "first_name": "bar"
    }
    """
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email_body = (
            f'Доброе время суток, {user.username}.'
            f'\nКод подтвержения для доступа к API: {user.confirmation_code}'
        )
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Код подтвержения для доступа к API'
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
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден!'},
                status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)