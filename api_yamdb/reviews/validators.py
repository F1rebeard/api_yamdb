from django.core.exceptions import ValidationError
import re


def validate_slug(value):
    slug = re.compile('^[-a-zA-Z0-9_]+$')
    if not slug.match(value):
        raise ValidationError('Поле slug заполнено некорректно.')
