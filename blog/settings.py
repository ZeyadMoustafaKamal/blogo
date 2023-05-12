from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6hn*$hme98=3peqb%mxg(3+46111h8i@7_wmf(2jv!*p@#fg9_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # local

    'core.apps.CoreConfig',
    'accounts.apps.AccountsConfig',
    'posts.apps.PostsConfig',
    'blogs.apps.BlogsConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third party
    
    'crispy_forms',
    'crispy_bootstrap5',
    'tinymce',
    'debug_toolbar',
    'rest_framework'
]

# rest framwork and simple jwt

REST_FRAMEWORK = {
   'DEFAULT_AUTHENTICATION_CLASSES':[
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
}

SIMPLE_JWT = {
    'REFRESH_TOKEN_LIFETIME':timedelta(days=30),
    'ACCESS_TOKEN_LIFETIME':timedelta(days=1),
    'ROTATE_REFRESH_TOKENS':True
}

# crispy

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'

CRISPY_TEMPLATE_PACK = 'bootstrap5'


# TinyMCE config

TINYMCE_DEFAULT_CONFIG = {
    'height': 200,
    'width': 900,
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
    'selector': 'textarea.tinymce',
    'theme': 'modern',
    'plugins': '''
        advlist autolink lists link image charmap print preview hr anchor
        searchreplace wordcount visualblocks code fullscreen
        insertdatetime media nonbreaking save table contextmenu
        directionality emoticons template paste textcolor colorpicker textpattern
    ''',
    'toolbar': '''
        undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify |
        bullist numlist outdent indent | link image | print preview media fullpage |
        forecolor backcolor emoticons | fontsizeselect
    ''',
    'fontsize_formats': '8pt 10pt 12pt 14pt 18pt 24pt 36pt',
}

TINYMCE_JS_URL = 'https://cdn.tiny.cloud/1/khgo7qw2j3rly9d0nklt7ccwy2b8j696np0a0xlmt6gkxxo0/tinymce/5/tinymce.min.js'

TINYMCE_COMPRESSOR = False


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # third party
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
INTERNAL_IPS = ['127.0.0.1']

ROOT_URLCONF = 'blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'blog.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'accounts.CustomUser'

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'

# the media configuration

MEDIA_URL = 'media/'

MEDIA_ROOT = 'media/'




