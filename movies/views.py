from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .tmdb import search_movies, get_movie_details, IMAGE_BASE_URL
from .models import Movie, UserMovie, FavoriteActor
from .forms import UserMovieForm

def home(request):
    query = request.GET.get('q', '')
    movies = []

    if query:
        movies = search_movies(query)

    return render(request, 'movies/home.html', {
        'movies': movies,
        'query': query,
        'image_base_url': IMAGE_BASE_URL,
    })

def movie_detail(request, movie_id):
    movie = get_movie_details(movie_id)
    cast = movie.get('credits', {}).get('cast', [])[:10]

    user_movie = None
    form = None

    if request.user.is_authenticated:
        db_movie = Movie.objects.filter(tmdb_id=movie_id).first()
        if db_movie:
            user_movie = UserMovie.objects.filter(
                user=request.user,
                movie=db_movie
            ).first()

        if user_movie:
            if request.method == 'POST' and 'save_review' in request.POST:
                form = UserMovieForm(request.POST, instance=user_movie)
                if form.is_valid():
                    form.save()
                    return redirect('movie_detail', movie_id=movie_id)
            else:
                form = UserMovieForm(instance=user_movie)

    return render(request, 'movies/detail.html', {
        'movie': movie,
        'cast': cast,
        'image_base_url': IMAGE_BASE_URL,
        'user_movie': user_movie,
        'form': form,
    })

@login_required
def add_to_list(request, movie_id):
    if request.method == 'POST':
        status = request.POST.get('status')

        movie_data = get_movie_details(movie_id)
        genres = ', '.join([g['name'] for g in movie_data.get('genres', [])])
        release_year = movie_data.get('release_date', '')[:4]

        movie, created = Movie.objects.get_or_create(
            tmdb_id=movie_id,
            defaults={
                'title': movie_data['title'],
                'poster_path': movie_data.get('poster_path', ''),
                'overview': movie_data.get('overview', ''),
                'release_year': release_year,
                'genres': genres,
            }
        )

        user_movie, created = UserMovie.objects.get_or_create(
            user=request.user,
            movie=movie,
            defaults={'status': status}
        )

        if not created:
            user_movie.status = status
            user_movie.save()

    return redirect('movie_detail', movie_id=movie_id)

@login_required
def add_favorite_actor(request, actor_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        profile_path = request.POST.get('profile_path')

        FavoriteActor.objects.get_or_create(
            user=request.user,
            tmdb_actor_id=actor_id,
            defaults={
                'name': name,
                'profile_path': profile_path,
            }
        )

    return redirect(request.META.get('HTTP_REFERER', 'home'))
@login_required
def recommendations(request):
    from movies.tmdb import get_recommendations
    watched = UserMovie.objects.filter(
        user=request.user,
        status='watched'
    ).select_related('movie')

    # Собираем жанры из просмотренных фильмов
    from collections import Counter
    all_genres = []
    for item in watched:
        if item.movie.genres:
            all_genres.extend([g.strip() for g in item.movie.genres.split(',')])

    # TMDB genre IDs для популярных жанров
    genre_map = {
        'боевик': 28, 'приключения': 12, 'анимация': 16,
        'комедия': 35, 'криминал': 80, 'документальный': 99,
        'драма': 18, 'семейный': 10751, 'фэнтези': 14,
        'история': 36, 'ужасы': 27, 'музыка': 10402,
        'мелодрама': 10749, 'фантастика': 878, 'триллер': 53,
        'война': 10752, 'вестерн': 37, 'мультфильм': 16,
    }

    top_genres = Counter(all_genres).most_common(3)
    genre_ids = [genre_map[g] for g, _ in top_genres if g.lower() in genre_map]

    movies = get_recommendations(genre_ids) if genre_ids else []

    # Убираем уже просмотренные
    watched_ids = set(item.movie.tmdb_id for item in watched)
    movies = [m for m in movies if m['id'] not in watched_ids]

    return render(request, 'movies/recommendations.html', {
        'movies': movies,
        'top_genres': [g for g, _ in top_genres],
        'image_base_url': IMAGE_BASE_URL,
    })