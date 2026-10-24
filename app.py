"""Rutas de la página Cauce: la ÚNICA tabla de URLs del proyecto (ROOT_URLCONF = "app").

Todas las rutas existen desde el paso 4 (con una página "Próximamente" donde aún no hay
contenido), así la navegación nunca apunta a una URL inexistente.

Atajo: `python app.py` arranca el servidor de desarrollo (equivale a `manage.py runserver`);
`python app.py <comando>` ejecuta cualquier comando de manage.py, p. ej. `python app.py check`.
"""

from django.urls import path

from web import views, views_app

urlpatterns = [
    # Públicas: web/views.py (Persona A)
    path("", views.inicio, name="inicio"),
    path("metodologia/", views.metodologia, name="metodologia"),
    path("resultados/", views.resultados, name="resultados"),
    path("styleguide/", views.styleguide, name="styleguide"),
    path("health/", views.health, name="health"),
    # Acceso y aplicación: web/views_app.py (Persona B)
    path("login/", views_app.login, name="login"),
    path("registro/", views_app.registro, name="registro"),
    path("salir/", views_app.salir, name="salir"),
    path("app/simulador/", views_app.simulador, name="simulador"),
    path("app/api/simular/", views_app.api_simular, name="api_simular"),
    path("app/simulaciones/", views_app.simulaciones, name="simulaciones"),
    path(
        "app/simulaciones/<slug:sim_id>/",
        views_app.simulacion_detalle,
        name="simulacion_detalle",
    ),
]


if __name__ == "__main__":
    import os
    import sys

    from django.core.management import execute_from_command_line

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    execute_from_command_line([sys.argv[0], *(sys.argv[1:] or ["runserver"])])
