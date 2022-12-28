import uuid
from dataclasses import dataclass, asdict
import datetime


@dataclass
class CurrentTable:

    @property
    def get_values_from_table(self):
        data = []
        for i in asdict(self).values():
            data.append(str(i))
        return '\t'.join(data)


@dataclass
class FilmWork(CurrentTable):
    __slots__ = (
        'id', 'title', 'description', 'creation_date',
        'file_path', 'rating', 'type', 'created_at', 'updated_at'
    )
    id: uuid.UUID
    title: str
    description: str
    creation_date: datetime.datetime
    rating: float
    type: str
    created: datetime.datetime
    modified: datetime.datetime
    certificate: str


@dataclass
class Genre(CurrentTable):
    __slots__ = (
        'id', 'name', 'description', 'created_at', 'updated_at'
    )
    id: uuid.UUID
    name: str
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


@dataclass
class Person(CurrentTable):
    __slots__ = (
        'id', 'full_name', 'created_at', 'updated_at'
    )
    id: uuid.UUID
    full_name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


@dataclass
class GenreFilmWork(CurrentTable):
    __slots__ = (
        'id', 'film_work_id', 'genre_id', 'created_at'
    )
    id: uuid.UUID
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    created_at: datetime.datetime


@dataclass
class PersonFilmWork(CurrentTable):
    __slots__ = (
        'id', 'film_work_id', 'person_id', 'role', 'created_at'
    )
    id: uuid.UUID
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    created_at: datetime.datetime
