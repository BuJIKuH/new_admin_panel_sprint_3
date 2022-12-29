Для запуска приложения необходимо выполнить следующие действия:

Для корректной работы приложения необходима создать файл .env по образцу .env.example.
Запускаем "docker-compose up -d --build"
Подключаемся к сервису django командой "docker exec -it <номер контейнера> /bin/sh"
Создаем супер пользователя "python manage.py createsuperuser"
Переходим по адресу "http://localhost/api/v1/movies/" и наблюдаем весь список фильмов.
Переходим по адресу "http://localhost/api/v1/movies/uuid:pk" и получаем детальную информацию о конкретном фильме.
Переходим по адресу "http://localhost/admin/" и редактируем фильмы.
Переходим по адресу "http://localhost:5601/app/dev_tools#/console" и перед 
нами открывается "кибана", далее вставляем "
GET movies/_search
{
    "query": {
        "multi_match": {
            "query": "camp",
            "fuzziness": "auto",
            "fields": [
                "actors_names",
                "writers_names",
                "title",
                "description",
                "genre"
            ]
        }
    }
}
", в этом запросе мы ищем где встречается название "camp".
Для запуска тестов в постман, используем ссылку 
"https://code.s3.yandex.net/middle-python/learning-materials/ETLTests-2.json"
Для просмотра информации через swagger переходим по адресу "http://localhost:8080/"
