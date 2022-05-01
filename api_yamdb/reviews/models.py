from django.db import models

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

    # Хз хачем это, уже не помню зачем написал.
    # Если не найду смысл этой конструкции - потом удалю
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['name', 'year'],
    #             name='unique_title'
    #         )
    #     ]

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        str = f'{self.title} : {self.genre}'
        return str


class Review(models.Model):
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(default=None, choices=SCORE)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        str = f'{self.title_id} : {self.text[:20]}'
        return str
