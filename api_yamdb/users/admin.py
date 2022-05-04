from django.contrib import admin

from .models import User
from reviews.models import Category, Genre, Title, Review
from reviews_and_comments.models import Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '--empty--'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'review',
        'text',
        'author',
        'pub_date',
    )
    search_fields = ('review',)
    list_filter = ('review',)
    empty_value_display = '--empty--'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name', 'slug')
    list_filter = ('name',)
    empty_value_display = '--empty--'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'author',
        'score',
    )
    search_fields = ('pub_date', 'author')
    list_filter = ('pub_date',)
    empty_value_display = '--empty--'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'category',
        'description',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '--empty--'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'bio',
        'first_name',
        'last_name',
        'confirmation_code',
    )
    search_fields = ('username', 'first_name', 'last_name', 'role',)
    list_filter = ('username',)
    empty_value_display = '--empty--'
