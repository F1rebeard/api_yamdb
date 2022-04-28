from django.db import models

from .validators import validate_slug


class Category(models.Model):
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
        blank=False,
        null=False
    )
    year = models.IntegerField()
    cathegory = models.ForeignKey(
        Category, related_name='titles',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    description = models.TextField()
    genre = models.ManyToManyField(Genre, through='GenreTitle')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'year'],
                name='unique_title'
            )
        ]


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
