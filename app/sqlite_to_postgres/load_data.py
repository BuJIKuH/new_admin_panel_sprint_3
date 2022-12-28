import os
import logging
import io
import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from dotenv import load_dotenv

from data_classes import FilmWork, GenreFilmWork, Genre, Person, PersonFilmWork

load_dotenv()

log = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

PACK_SIZE = 100
TABLES_DICT = {
    'film_work': FilmWork,
    'genre_film_work': GenreFilmWork,
    'genre': Genre,
    'person': Person,
    'person_film_work': PersonFilmWork,
}


class SQLiteExtractor:
    """Класс, в котором происходит "выгрузка" фильмов из SQlite """
    def __init__(self, connection, table_name, data_class, verbose=False):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.verbose = verbose
        self.table_name = table_name
        self.data_class = data_class
        self.cursor.execute(f'SELECT * FROM {self.table_name}')

    def extract_movies(self):

        count = 0
        while True:
            packs_rows = self.cursor.fetchmany(size=PACK_SIZE)
            if not packs_rows:
                break
            packs = []
            for row in packs_rows:
                data = self.data_class(*row)
                packs.append(data)
            yield packs
            count += 1

        if self.verbose:
            log.info('Загружено из %s %s пачек', self.table_name, count)

    def __del__(self):
        self.cursor.close()


class PostgresSaver(SQLiteExtractor):
    """Класс, в котором происходит подготовка к записи фильмов в Postgres"""
    def save_all_data(self, data):

        count = 0
        for pack in data:
            objects = []
            for subject in pack:
                objects.append(subject.get_values_from_table)
            pack_values = '\n'.join(objects)
            with io.StringIO(pack_values) as p:
                self.cursor.copy_from(p, table=self.table_name, null='None',
                                      size=PACK_SIZE)
            count += 1

        if self.verbose:
            log.info('В таблицу %s вставлено %s пачек', self.table_name, count)


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""

    for table_name, data_class in TABLES_DICT.items():
        try:
            sqlite_extractor = SQLiteExtractor(connection, table_name,
                                               data_class, verbose=True)
            data = sqlite_extractor.extract_movies()
        except Exception:
            log.exception('error reading SQLite')
            break
        try:
            postgres_saver = PostgresSaver(pg_conn, table_name, data_class,
                                           verbose=True)
            postgres_saver.save_all_data(data)
        except Exception:
            log.exception('error writing Postgres')
            break


if __name__ == '__main__':
    dsl = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST'),
        'port': os.environ.get('DB_PORT'),
        'options': '-c search_path=content'
    }

    with sqlite3.connect('db.sqlite') as sqlite_conn, \
            psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
