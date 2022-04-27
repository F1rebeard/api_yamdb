from django.core.exceptions import ValidationError


def validate_username(username):
    """
    Проверка никнейма пользователя на корректность.
    Согласно ТЗ, никнейм "me" запрещен.
    """
    if username == 'me':
        raise ValidationError('Некорректное имя')
