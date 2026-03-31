from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from movies.models import UserMovie, FavoriteActor
from collections import Counter

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    watched = UserMovie.objects.filter(
        user=request.user,
        status='watched'
    ).select_related('movie')

    watchlist = UserMovie.objects.filter(
        user=request.user,
        status='watchlist'
    ).select_related('movie')

    favorite_actors = FavoriteActor.objects.filter(user=request.user)

    # Подсчёт жанров
    all_genres = []
    for item in watched:
        if item.movie.genres:
            genres = [g.strip() for g in item.movie.genres.split(',')]
            all_genres.extend(genres)

    genre_counts = Counter(all_genres)
    top_genres = genre_counts.most_common(5)

    # Средняя оценка
    ratings = [item.rating for item in watched if item.rating]
    avg_rating = round(sum(ratings) / len(ratings), 1) if ratings else None

    return render(request, 'users/profile.html', {
        'watched': watched,
        'watchlist': watchlist,
        'favorite_actors': favorite_actors,
        'image_base_url': 'https://image.tmdb.org/t/p/w500',
        'top_genres': top_genres,
        'avg_rating': avg_rating,
        'ratings_count': len(ratings),
    })