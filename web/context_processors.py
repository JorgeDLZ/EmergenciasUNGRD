"""Variables disponibles en todas las plantillas."""

from django.conf import settings
from django.http import HttpRequest


def sitio(request: HttpRequest) -> dict:
    return {
        "sitio": {
            "nombre": "Cauce",
            "subtitulo": "Asignación inteligente de recursos ante emergencias",
            "datos_demo": settings.CAUCE_DATOS_DEMO,
        }
    }
