import os

from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from pathlib import Path

from environs import Env

env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')
TELEGRAM_BOT_TOKEN=env.str('TELEGRAM_BOT_TOKEN')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(env.int('DEBUG'))

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', ['localhost', '127.0.0.1'])


# Application definition

INSTALLED_APPS = [
    # 3rd party apps
    'unfold',

    # Django Model Translation
    'modeltranslation',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # DRF
    'rest_framework',

    # Apps
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'PROJECT.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
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

WSGI_APPLICATION = 'PROJECT.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        },
        'bot': {
            # Telegram bot DB
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'hitium_assistant',
            'USER': 'root',
            'PASSWORD': '12345678',
            'HOST': '127.0.0.1',
            'PORT': '3306',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env.str('DB_NAME'),
            'USER': env.str('DB_USER'),
            'PASSWORD': env.str('DB_PASSWORD'),
            'HOST': env.str('DB_HOST'),
            'PORT': env.str('DB_PORT'),
        },
        'bot': {
            # Telegram bot DB
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'hitium_assistant',
            'USER': 'bot_user',
            'PASSWORD': 'password',
            'HOST': '127.0.0.1',
            'PORT': '3306',
        }
    }

DATABASE_ROUTERS = ['PROJECT.routers.DayRouter']

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True

LANGUAGES = (
    ('uz', _('Узбекский')),
    ('ru', _('Русский'))
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATICFILES_DIRS = [
    BASE_DIR / 'staticfiles'
]
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'api.User'

UNFOLD = {
    "SITE_TITLE": "Админ панель Hitium",
    "SITE_HEADER": "Панель управления",
    "SITE_URL": None,
    "SITE_SYMBOL": "joystick",
    "LOGIN": {
        "TITLE": "Вход в систему Hitium",
        "SUBTITLE": "Панель администратора",
    },
    "SHOW_BACK_BUTTON": True,

    "SIDEBAR": {
        "show_search": True,  # Search in applications and models names
        "command_search": False,  # Replace the sidebar search with the command search
        "show_all_applications": False,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": _("Основное"),
                # "collapsible": True,
                "items": [
                    {
                        "title": _("Задачи"),
                        "icon": "list",
                        "link": reverse_lazy("admin:api_task_changelist"),
                        "badge": "api.views.tasks",
                        "badge_variant": "success", # info, success, warning, primary, danger
                        # "badge_style": "solid", # background fill style
                        # "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Бригады"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:api_brigade_changelist"),
                    },
                ],
            },
            {
                "title": _("Команда"),
                "separator": True,
                # "collapsible": True,
                "items": [
                    {
                        "title": _("Все"),
                        "icon": "people",
                        "link": reverse_lazy("admin:api_user_changelist"),
                        # "badge": "3",
                        # "badge_variant": "success", # info, success, warning, primary, danger
                        # "badge_style": "solid", # background fill style
                        # "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Бригадиры"),
                        "icon": "person",
                        "link": reverse_lazy("admin:api_foreman_changelist"),
                    },
                ],
            },
            {
                "title": _("Другое"),
                "separator": True,  # Top border
                # "collapsible": True,  # Collapsible group of links
                "items": [
                    {
                        "title": _("Отметки"),
                        "icon": "check",
                        "link": reverse_lazy("admin:api_attendance_changelist"),
                    },
                    {
                        "title": _("Работники"),
                        "icon": "engineering",
                        "link": reverse_lazy("admin:api_worker_changelist"),
                    },
                    {
                        "title": _("Рабочие дни"),
                        "icon": "calendar_month",
                        "link": reverse_lazy("admin:api_day_changelist"),
                    },
                    {
                        "title": _("Специализации"),
                        "icon": "work",
                        "link": reverse_lazy("admin:api_specialization_changelist"),
                    },
                ],
            },
        ],
    },
}


LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} [{levelname}] {name}: {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{levelname}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'tasks.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'task_logger': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]
