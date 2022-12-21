import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UUIDMixin(models.Model):
    """Дополнительная таблица, чтобы убрать дублирование кода"""
    id = models.UUIDField(
        _('unique key'),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True


class TimeStampedMixin(models.Model):
    """Дополнительная таблица, чтобы убрать дублирование кода"""
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True


class Genre(TimeStampedMixin, UUIDMixin):
    """Таблица Жанр"""
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True,
                                   default='Описание')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')


class FilmWork(UUIDMixin, TimeStampedMixin):
    """Таблица Кинопроизведения"""

    class TypeChoices(models.TextChoices):
        """Выбор типов произведений"""
        MOVIE = 'movies', _('movies')
        TV_SHOW = 'tv_show', _('tv_show')

    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    creation_date = models.DateField(_("creation date"), blank=True)
    rating = models.FloatField(
        _("rating"),
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    type = models.TextField(
        _("type"), choices=TypeChoices.choices, default=TypeChoices.MOVIE
    )
    genres = models.ManyToManyField(Genre, verbose_name='genres',
                                    through="GenreFilmWork")
    persons = models.ManyToManyField("Person", through="PersonFilmWork")
    file_path = models.FileField(
        _("file"), blank=True, null=True, upload_to="movies/"
    )

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _("film work")
        verbose_name_plural = _("film works")

    def __str__(self):
        return self.title


class Person(TimeStampedMixin, UUIDMixin):
    """Таблица о людях принявших участие в кинопроизведении"""
    full_name = models.CharField(_('full name'), max_length=150)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('person')
        verbose_name_plural = _('persons')


class GenreFilmWork(UUIDMixin):
    """Дополнительная таблица Жанры к Произведениям"""
    film_work = models.ForeignKey(
        'FilmWork', on_delete=models.CASCADE, verbose_name=_('film work'))
    genre = models.ForeignKey(
        'Genre', on_delete=models.CASCADE, verbose_name=_('genre'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('genre', 'film_work')
        db_table = "content\".\"genre_film_work"


class RoleChoices(models.TextChoices):
    """Выбираем роль"""
    ACTOR = 'actor', _('actor')
    DIRECTOR = 'director', _('director')
    SCREENWRITER = 'writer', _('writer')


class PersonFilmWork(UUIDMixin):
    """Дополнительная таблица Людей к Кинопроизведениям"""

    film_work = models.ForeignKey(
        'FilmWork', on_delete=models.CASCADE, verbose_name=_('film work'))
    person = models.ForeignKey(
        'Person', on_delete=models.CASCADE, verbose_name=_('person'))
    role = models.TextField(_('role'), choices=RoleChoices.choices,
                            default=RoleChoices.ACTOR)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        constraints = [
            models.UniqueConstraint(
                fields=["film_work", "person", "role"],
                name="film_work_person_role_idx",
            ),
        ]
        verbose_name = _("Person - FilmWork")
        verbose_name_plural = _("Persons - FilmWorks")
