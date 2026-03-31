from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movie/<int:movie_id>/add/', views.add_to_list, name='add_to_list'),
    path('actor/<int:actor_id>/favorite/', views.add_favorite_actor, name='add_favorite_actor'),
    path('recommendations/', views.recommendations, name='recommendations'),
]