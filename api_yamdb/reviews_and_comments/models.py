from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User
from reviews.models import Title


class Review(models.Model):
    """
    Модель для отзывов к произведенияем.
    """
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name = 'reviews',
    )
    title = models.ForeignKey(
        Title,
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

    class Meta:
        ordering = ('-pub_date',)
        #только один отзыв на каждое произведение для одного автора
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text[:10]


class Comment(models.Model):
    """
    Модель комментариев к отзывам на произведения.
    """
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:10]


