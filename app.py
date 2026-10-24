"""Rutas de la página Cauce: la ÚNICA tabla de URLs del proyecto (ROOT_URLCONF = "app").

En el paso 4 esta tabla crece con todas las páginas. Atajo: `python app.py` arranca el servidor
de desarrollo (equivale a `manage.py runserver`); `python app.py <comando>` ejecuta cualquier
comando de manage.py, p. ej. `python app.py check`.
"""

from django.urls import path

from web import views

urlpatterns = [
    path("health/", views.health, name="health"),
]


if __name__ == "__main__":
    import os
    import sys

    from django.core.management import execute_from_command_line

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    execute_from_command_line([sys.argv[0], *(sys.argv[1:] or ["runserver"])])
