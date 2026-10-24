"""Vistas de acceso (login simulado) y de la aplicación (simulador, simulaciones)."""

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST


def _proximamente(request: HttpRequest, titulo: str) -> HttpResponse:
    return render(request, "web/base.html", {"titulo": titulo})


def login(request: HttpRequest) -> HttpResponse:
    return _proximamente(request, "Iniciar sesión")


def registro(request: HttpRequest) -> HttpResponse:
    return _proximamente(request, "Crear cuenta")


@require_POST
def salir(request: HttpRequest) -> HttpResponse:
    return redirect("inicio")


def simulador(request: HttpRequest) -> HttpResponse:
    return _proximamente(request, "Simulador")


@require_POST
def api_simular(request: HttpRequest) -> JsonResponse:
    return JsonResponse(
        {"error": {"codigo": "no_implementado", "mensaje": "El simulador llega en el paso 11"}},
        status=501,
    )


def simulaciones(request: HttpRequest) -> HttpResponse:
    return _proximamente(request, "Mis simulaciones")


def simulacion_detalle(request: HttpRequest, sim_id: str) -> HttpResponse:
    return _proximamente(request, "Simulación")
