from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q

from rest_framework import generics

from movies.models import FilmWork, RoleChoices
from .pagination import StandardResultsSetPagination
from .serializer import FilmWorkSerializer


class FilmWorkApiViewMixin:
    """Класс миксин"""
    queryset = FilmWork.objects.prefetch_related(
        'genres', 'persons',
    ).values().all().annotate(
        genres=ArrayAgg(
            'genres__name', distinct=True
        ),
        actors=ArrayAgg(
            'persons__full_name',
            filter=Q(personfilmwork__role__icontains=RoleChoices.ACTOR),
            distinct=True,
        ),
        directors=ArrayAgg(
            'persons__full_name',
            filter=Q(personfilmwork__role__icontains=RoleChoices.DIRECTOR),
            distinct=True,
        ),
        screenwriters=ArrayAgg(
            'persons__full_name',
            filter=Q(personfilmwork__role__icontains=RoleChoices.SCREENWRITER),
            distinct=True,
        ),
    )
    serializer_class = FilmWorkSerializer


class FilmWorkApiView(FilmWorkApiViewMixin, generics.ListAPIView):
    """Представление данных таблицы Кинопроизведения и связанных с ней."""
    pagination_class = StandardResultsSetPagination


class DetailFilmWorkApiView(FilmWorkApiViewMixin, generics.RetrieveAPIView):
    """Детальное представление таблицы Кинопроизведений"""
    ...
