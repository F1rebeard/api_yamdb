import datetime as dt

from django.core.exceptions import ValidationError
from django.utils import timezone

# Не готово
def validate_username(username):
    """
    Проверка никнейма пользователя на корректность.
    """
    if False:
        raise ValidationError('Некорректное имя')


def validate_year(birth_year):
    """
    Проверка года рождения пользователя на корректность
    """
    if birth_year > dt.datetime.now().year:
        raise ValidationError('Некорректная дата рождения')