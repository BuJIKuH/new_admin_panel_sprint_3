from django.urls import path

from movies.api.v1 import views

urlpatterns = [
    path('movies/', views.FilmWorkApiView.as_view()),
    path('movies/<uuid:pk>/', views.DetailFilmWorkApiView.as_view()),
]
