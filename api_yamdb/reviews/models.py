from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User

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
        return f'{self.title} : {self.genre}'


class Review(models.Model):
    """
    Модель для отзывов к произведенияем.
    """
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(10, 'Максимальная оценка - 10'),
            MinValueValidator(1, 'Минимальная оценка - 1'),
        ]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        # только один отзыв на каждое произведение для одного автора
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text[:10]
