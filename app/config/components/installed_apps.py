from config.settings import DEBUG

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'movies.apps.MoviesConfig',
]

if DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]
