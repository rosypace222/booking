# Додатки
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',
    'booking_app.apps.BookingAppConfig',
    'crispy_forms',
    'crispy_bootstrap5',
]

# Користувацька модель користувача
AUTH_USER_MODEL = 'auth.User'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# База даних
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'booking_db',
        'USER': 'booking_user',
        'PASSWORD': 'securepassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Часова зона
TIME_ZONE = 'Europe/Kiev'
USE_TZ = True

# Статичні файли
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Медіа файли
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'