import os
from pathlib import Path
from datetime import timedelta

# ✅ Base directory configuration
BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ Security settings
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-default-secret-key')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# ✅ Installed apps
INSTALLED_APPS = [
    'corsheaders',  # CORS support
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',  # JWT token blacklist support
    'library',  # Our custom app
]

# ✅ Middleware configuration
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS middleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ✅ URL configuration
ROOT_URLCONF = 'library_management.urls'

# ✅ Templates configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # If you keep your project-level templates in BASE_DIR/templates,
        # and your app templates inside the app, APP_DIRS=True will find them.
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

# ✅ WSGI application
WSGI_APPLICATION = 'library_management.wsgi.application'

# ✅ Database configuration (MySQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'my_app_db',
        'USER': 'my_app_user',
        'PASSWORD': 'my_app_password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# ✅ JWT Authentication & DRF settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# ✅ JWT settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# ✅ Static files configuration
STATIC_URL = '/static/'
# For development, include the static directory inside your app.
STATICFILES_DIRS = [BASE_DIR / 'library' / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ✅ Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ✅ CORS settings
CORS_ALLOW_ALL_ORIGINS = True

# ✅ Custom user model
AUTH_USER_MODEL = 'library.AdminUser'
LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/dashboard/'


# ✅ Authentication redirection settings
LOGIN_URL = '/admin/login/'            # Redirect URL for login-required pages
LOGIN_REDIRECT_URL = '/dashboard/'       # Default redirect after a successful login

# ✅ CSRF settings
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
]

# ✅ Logging configuration (for debugging purposes)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
