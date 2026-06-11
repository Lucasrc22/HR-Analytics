

import os
from pathlib import Path
from decouple import config, Csv

# Compatibilidade do driver oracledb com o backend Oracle do Django
# (oracledb substitui o antigo cx_Oracle). Mantém o "thin mode", sem
# necessidade do Oracle Instant Client instalado na máquina.
import sys
import oracledb
oracledb.version = "8.3.0"
sys.modules["cx_Oracle"] = oracledb

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: a SECRET_KEY é obrigatória e deve vir do ambiente (.env).
# Sem default no código: se faltar a variável, o Django falha ao iniciar
# (em vez de subir silenciosamente com uma chave insegura).
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: nunca rode com DEBUG=True em produção.
# Sem DEBUG no .env, o dev local cai no default True; o container define DEBUG=False.
DEBUG = config('DEBUG', default=True, cast=bool)

# Hosts permitidos e origens CSRF confiáveis (separados por vírgula no .env).
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='', cast=Csv())


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user',
    'pj_rh',
    'authentication',
    'cat',
    'treinamento',
    'vagas',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise serve os estáticos com cache/compressão (logo após o SecurityMiddleware).
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [BASE_DIR / "app" / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        # Usando SERVICE_NAME (não SID): monta o DSN no formato host:port/service_name.
        # Por isso o NAME recebe o DSN completo e HOST/PORT ficam vazios.
        'NAME': '{host}:{port}/{service}'.format(
            host=config('ORACLE_HOST'),                
            port=config('ORACLE_PORT', default='1521'),
            service=config('ORACLE_SERVICE_NAME'),
        ),
        'USER': config('ORACLE_USER'),
        'PASSWORD': config('ORACLE_PASSWORD'),
    }
}

# Fallback local em SQLite (descomente para desenvolver sem o Oracle disponível):
#DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'pt-BR'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'app', 'templates')]

# Arquivos de mídia (uploads de usuários)
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# WhiteNoise: compressão dos estáticos. Sem manifest, para não quebrar caso
# algum arquivo referenciado não exista no momento do collectstatic.
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# --- Segurança (aplicada atrás do proxy nginx) ---
# O nginx repassa o protocolo original neste header (http/https).
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Endurecimento aplicado apenas fora do modo DEBUG (produção/container).
if not DEBUG:
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"

    # IMPORTANTE: cookies "Secure" e redirecionamento SSL só funcionam sob HTTPS.
    # Em acesso por HTTP puro (ex.: rede interna via IP:porta), ligá-los QUEBRA o
    # login — o navegador não envia cookie Secure por HTTP. Por isso ficam atrelados
    # ao HTTPS_ENABLED: deixe False enquanto for HTTP; mude para True ao ativar TLS.
    HTTPS_ENABLED = config('HTTPS_ENABLED', default=False, cast=bool)
    SESSION_COOKIE_SECURE = HTTPS_ENABLED
    CSRF_COOKIE_SECURE = HTTPS_ENABLED
    SECURE_SSL_REDIRECT = HTTPS_ENABLED
    if HTTPS_ENABLED:
        SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int)
        SECURE_HSTS_INCLUDE_SUBDOMAINS = True
        SECURE_HSTS_PRELOAD = True