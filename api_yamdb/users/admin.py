from django.contrib import admin

from .models import User
from reviews.models import Cathegory, Genre, Title

admin.site.register(User)
admin.site.register(Cathegory)
admin.site.register(Genre)
admin.site.register(Title)
