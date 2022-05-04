"""Кастомные валидаторы"""
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    """Валидатор года выпуска title"""
    year = timezone.now().year
    if value > year:
        raise ValidationError(
            'Нельзя добавлять фильмы из будущего! '
            'Временная полиция не дремлет.'
        )
