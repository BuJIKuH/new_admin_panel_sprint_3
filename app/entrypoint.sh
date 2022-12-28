#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"

fi

python manage.py migrate
python manage.py collectstatic --no-input
python manage.py compilemessages

cd sqlite_to_postgres

echo "python load_data.py"
python load_data.py -e $DB_NAME=movies_db $DB_USER=app
$DB_PASSWORD=123qwe $DB_HOST=db $DB_PORT=5432

cd ../

exec "$@"