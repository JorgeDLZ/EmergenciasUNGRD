"""Configuración de Django para Cauce.

Todo se lee de variables de entorno. En Render (RENDER=true) se exige DJANGO_SECRET_KEY y
DEBUG queda apagado; en un computador local funciona sin configurar nada.
"""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

# Render define RENDER=true en todos sus servicios.
EN_RENDER = os.environ.get("RENDER") == "true"

DEBUG = os.environ.get("DJANGO_DEBUG", "0" if EN_RENDER else "1") == "1"

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")
if not SECRET_KEY:
    if EN_RENDER:
        raise ImproperlyConfigured("Falta la variable de entorno DJANGO_SECRET_KEY")
    SECRET_KEY = "solo-desarrollo-local-nunca-en-produccion"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
CSRF_TRUSTED_ORIGINS: list[str] = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "web",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if EN_RENDER:
    # WhiteNoise sirve el CSS/JS ya recolectado (collectstatic) en producción. En local lo
    # sirve `runserver` con DEBUG activo.
    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

ROOT_URLCONF = "app"  # rutas en app.py (raíz del proyecto)
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "web.context_processors.sitio",
            ],
        },
    },
]

# Etapa 1: sin base de datos en uso. SQLite queda declarado para que la etapa 2 solo tenga
# que cambiar este bloque (Postgres) y activar django.contrib.auth.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Sesión en una cookie firmada: el login simulado no necesita base de datos.
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = EN_RENDER
CSRF_COOKIE_SECURE = EN_RENDER
if EN_RENDER:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

LANGUAGE_CODE = "es-co"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage.CompressedManifestStaticFilesStorage"
            if EN_RENDER
            else "django.contrib.staticfiles.storage.StaticFilesStorage"
        )
    },
}

# Muestra el aviso "Datos de ejemplo" en todas las páginas mientras no haya resultados reales.
CAUCE_DATOS_DEMO = os.environ.get("CAUCE_DATOS_DEMO", "1") == "1"
