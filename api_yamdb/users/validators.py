from django.core.exceptions import ValidationError


def validate_username(username):
    """
    Проверка никнейма пользователя на корректность.
    """
    if username == 'me':
        raise ValidationError('Некорректное имя')
