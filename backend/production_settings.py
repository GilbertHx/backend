from .base_settings import *

ALLOWED_HOSTS = ['159.89.221.21', ]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'assets'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'redb',
        'USER': 'rebdbuser',
        'PASSWORD': 'admintest',
        'HOST': 'localhost',
        'PORT': '',
    }
}

CORS_ORIGIN_WHITELIST = (
    '159.89.221.21',
)

WEBPACK_LOADER = {
    'DEFAULT': {
            'BUNDLE_DIR_NAME': 'bundles/',
            'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.prod.json'),
        }
}

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}