"""Vistas públicas de Cauce."""

from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from web import datos


def _proximamente(request: HttpRequest, titulo: str) -> HttpResponse:
    """Página provisional: base.html muestra "Próximamente" en su bloque de contenido."""
    return render(request, "web/base.html", {"titulo": titulo})


def inicio(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "web/inicio.html",
        {"titulo": "Inicio", "resumen": datos.resultados()["resumen"]},
    )


def metodologia(request: HttpRequest) -> HttpResponse:
    return _proximamente(request, "Metodología")


def resultados(request: HttpRequest) -> HttpResponse:
    return _proximamente(request, "Resultados")


def styleguide(request: HttpRequest) -> HttpResponse:
    if not settings.DEBUG:
        raise Http404("La guía de estilo solo existe en desarrollo")
    return _proximamente(request, "Guía de estilo")


def health(request: HttpRequest) -> JsonResponse:
    """Chequeo de salud para Render: confirma que el proceso responde."""
    return JsonResponse({"status": "ok", "app": "cauce"})
