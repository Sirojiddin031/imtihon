from pathlib import Path
from datetime import timedelta
from drf_yasg.openapi import Parameter, IN_HEADER

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-u%eb@im+)4m*7e19&nbbft5!4q-oji@btgo8@d*jo24np5$u^i'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'yourdomain.com']

INSTALLED_APPS = [
    'django.contrib.admin',          
    'django.contrib.auth',          
    'django.contrib.contenttypes',   
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', 
       
    'drf_yasg',                      
    'app_config',   
    'rest_framework',            
    'rest_framework_simplejwt',   
    'rest_framework_simplejwt.token_blacklist',                 
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

ROOT_URLCONF = 'Config.urls'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "https://yourdomain.com",
]

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

WSGI_APPLICATION = 'Config.wsgi.application'

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "Authorization",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "my_app.serializers.MyTokenObtainPairSerializer",
}

auth_header = Parameter(
    name="Authorization",
    in_=IN_HEADER,
    description="Enter JWT token like this: Bearer <your-token>",
    required=True,
    type="string"
)

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': "JWT tokenni `Bearer <your-token>` formatida yuboring",
        }
    },
    'USE_SESSION_AUTH': False, 
    'JSON_EDITOR': True,
    'DEFAULT_INFO': 'Config.urls.api_info',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'API Documentation',
    'VERSION': '1.0.0',
    'SCHEMA_PATH_PREFIX': '/api/v1/',
    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,
    },
    'COMPONENT_SPLIT_REQUEST': True,
    'SECURITY': [{'Bearer': []}],
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100
}

STATIC_URL = 'static/'

LOGIN_REDIRECT_URL = '/'
AUTH_USER_MODEL = 'app_config.User'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
