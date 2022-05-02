from django.contrib import admin

from .models import User
from reviews.models import Category, Genre, Title, GenreTitle
from reviews_and_comments.models import Review, Comment

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(GenreTitle)
admin.site.register(Review)
admin.site.register(Comment)
