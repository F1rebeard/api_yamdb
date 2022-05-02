"""Кастомные валидаторы"""
from django.core.exceptions import ValidationError
from datetime import datetime


def validate_year(value):
    """Валидатор года выпуска title"""
    year = datetime.now().year
    if value > year:
        raise ValidationError(
            'Нельзя добавлять фильмы из будущего! '
            'Временная полиция не дремлет.'
        )
