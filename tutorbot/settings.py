# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os.path import join, dirname
from dotenv import load_dotenv
import logging
import dj_database_url

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
logging.basicConfig(level=logging.INFO)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fsch+6!=q+@ol&%0x!nwdl@48^ixbd4clx5f1i!5n^66y+pmn*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [ '0.0.0.0', '127.0.0.1', 'localhost', '.herokuapp.com' ]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'chatterbot.ext.django_chatterbot',
    'tutorbot',
    'taggit',
    'corsheaders',
)

# ChatterBot settings

CHATTERBOT = {
    'name': 'Django ChatterBot Example',
    'trainer': 'chatterbot.trainers.ChatterBotCorpusTrainer',
    'read_only': True,
    'logic_adapters': [
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'tutorbot.adapters.TaggedBestMatch'
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.65,
            'default_response': 'I am sorry, but I do not understand. Can you be a bit more specific please?'
        }
    ],
    'training_data': [
        'tutorbot/data/corpus/greetings.yml',
        # 'chatterbot.corpus.english.greetings',
        'chatterbot.corpus.bangla.greetings',
        'chatterbot.corpus.spanish.greetings',
        'chatterbot.corpus.english.humor',
        'chatterbot.corpus.english.computers',
        'chatterbot.corpus.english.emotion',
        'chatterbot.corpus.chinese.greetings',
    ],
    'django_app_name': 'django_chatterbot'
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
)

CORS_ORIGIN_ALLOW_ALL = True

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'tutorbot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tutorbot.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# load database from the DATABASE_URL environment variable
DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600)

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TAGGIT_CASE_INSENSITIVE = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(
        os.path.dirname(__file__),
        'static',
    ),
)
