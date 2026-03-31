from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    poster_path = models.CharField(max_length=255, blank=True, null=True)
    overview = models.TextField(blank=True)
    release_year = models.CharField(max_length=4, blank=True)
    genres = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title

class UserMovie(models.Model):
    STATUS_CHOICES = [
        ('watched', 'Смотрел'),
        ('watchlist', 'Буду смотреть'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    rating = models.IntegerField(null=True, blank=True)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f'{self.user.username} — {self.movie.title} ({self.status})'

class FavoriteActor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tmdb_actor_id = models.IntegerField()
    name = models.CharField(max_length=255)
    profile_path = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('user', 'tmdb_actor_id')

    def __str__(self):
        return f'{self.user.username} — {self.name}'