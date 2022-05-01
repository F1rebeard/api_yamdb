from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import User


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
        Title, on_delete=models.CASCADE,
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



class Comment(models.Model):
    """
    Модель комментариев к отзывам на произведения.
    """
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
