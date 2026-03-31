from django.contrib import admin
from .models import Movie, UserMovie, FavoriteActor

admin.site.register(Movie)
admin.site.register(UserMovie)
admin.site.register(FavoriteActor)

