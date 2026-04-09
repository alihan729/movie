import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('TMDBAPI_KEY')
BASE_URL = 'https://api.themoviedb.org/3'
IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'

def search_movies(query):
    url = f'{BASE_URL}/search/movie'
    params = {
        'api_key': API_KEY,
        'query': query,
        'language': 'ru-RU',
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data.get('results', [])

def get_movie_details(movie_id):
    url = f'{BASE_URL}/movie/{movie_id}'
    params = {
        'api_key': API_KEY,
        'language': 'ru-RU',
        'append_to_response': 'credits',
    }
    response = requests.get(url, params=params)
    return response.json()
def get_recommendations(genre_ids):
    url = f'{BASE_URL}/discover/movie'
    params = {
        'api_key': API_KEY,
        'language': 'ru-RU',
        'with_genres': ','.join(map(str, genre_ids)),
        'sort_by': 'popularity.desc',
        'page': 1,
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data.get('results', [])[:8]

def get_actor_details(actor_id):
    url = f'{BASE_URL}/person/{actor_id}'
    params = {
        'api_key': API_KEY,
        'language': 'ru-RU',
        'append_to_response': 'movie_credits',
    }
    response = requests.get(url, params=params)
    return response.json()


def get_movies_by_genre(genre_id, page=1):
    url = f'{BASE_URL}/discover/movie'
    params = {
        'api_key': API_KEY,
        'language': 'ru-RU',
        'with_genres': genre_id,
        'sort_by': 'popularity.desc',
        'page': page,
    }
    response = requests.get(url, params=params)
    return response.json().get('results', [])