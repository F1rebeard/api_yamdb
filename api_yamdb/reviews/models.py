from django.db import models


SCORE = {
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
}


class Category(models.Model):
    """
    Модель категорий произведений.
    """
    name = models.CharField(
        max_length=256,
        unique=True,
        blank=False,
        null=False
    )
    slug = models.SlugField(
        unique=True,
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    """
    Модель жанров произведений.
    """
    name = models.CharField(
        max_length=256,
        unique=True,
        blank=False,
        null=False
    )
    slug = models.SlugField(
        unique=True,
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    """
    Модель произведений.
    """
    name = models.CharField(
        max_length=150,
        blank=False,
        null=False
    )
    year = models.IntegerField()
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    description = models.TextField()
    genre = models.ManyToManyField(Genre, through='GenreTitle')

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """
    Модель для ManyToMany связи между произведенями и жанрами.
    """
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        str = f'{self.title} : {self.genre}'
        return str
