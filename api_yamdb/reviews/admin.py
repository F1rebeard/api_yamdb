from django.contrib import admin

from reviews.models import Category, Genre, Title, Review, Comment


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
        'review_id',
        'text',
        'author',
        'pub_date',
    )
    search_fields = ('review_id',)
    list_filter = ('review_id',)
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
