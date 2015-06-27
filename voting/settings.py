import os

import dj_database_url
from django.core.urlresolvers import reverse_lazy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = bool(os.environ.get('DEBUG', False))

SECRET_KEY = os.environ.get('SECRET_KEY', 'development_only_key')

ALLOWED_HOSTS = ['pyconuk-voting.herokuapp.com', 'voting.pyconuk.org']


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',
    'opbeat.contrib.django',
    'social.apps.django_app.default',

    'voting',
)

MIDDLEWARE_CLASSES = (
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'voting.urls'

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

WSGI_APPLICATION = 'voting.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {'default': dj_database_url.config(default='postgres://localhost/voting')}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = False
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'


LOGIN_URL = reverse_lazy('login')
LOGOUT_URL = reverse_lazy('logout')
LOGIN_REDIRECT_URL = '/'


# Auth
AUTHENTICATION_BACKENDS = (
    'social.backends.email.EmailAuth',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.github.GithubOAuth2',
    'social.backends.twitter.TwitterOAuth',

    'django.contrib.auth.backends.ModelBackend',
)
SOCIAL_AUTH_USER_MODEL = 'auth.User'
SOCIAL_AUTH_EMAIL_FORM_URL = '/login/'
SOCIAL_AUTH_EMAIL_FORM_HTML = 'login.html'
SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get('SOCIAL_AUTH_FACEBOOK_KEY', '')
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get('SOCIAL_AUTH_FACEBOOK_SECRET', '')
SOCIAL_AUTH_GITHUB_KEY = os.environ.get('SOCIAL_AUTH_GITHUB_KEY', '')
SOCIAL_AUTH_GITHUB_SECRET = os.environ.get('SOCIAL_AUTH_GITHUB_SECRET', '')
SOCIAL_AUTH_TWITTER_KEY = os.environ.get('SOCIAL_AUTH_TWITTER_KEY', '')
SOCIAL_AUTH_TWITTER_SECRET = os.environ.get('SOCIAL_AUTH_TWITTER_SECRET', '')


# OpBeat
OPBEAT = {
    'ORGANIZATION_ID': os.environ.get('OPBEAT_ORGANIZATION_ID'),
    'APP_ID': os.environ.get('OPBEAT_APP_ID'),
    'SECRET_TOKEN': os.environ.get('OPBEAT_SECRET_TOKEN'),
}
