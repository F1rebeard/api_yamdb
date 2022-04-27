from django.db import models

from .validators import validate_slug


class Cathegory(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True,
        blank=False,
        null=False
    )
    slug = models.CharField(
        max_length=50,
        unique=True,
        validators=[validate_slug]
    )


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True,
        blank=False,
        null=False
    )
    slug = models.CharField(
        max_length=50,
        unique=True,
        validators=[validate_slug]
    )


class Title(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    year = models.IntegerField()
    description = models.TextField()
    cathegory = models.ForeignKey(
        Cathegory, related_name='titles',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
