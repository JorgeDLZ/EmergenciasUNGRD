"""Vistas públicas de Cauce."""

from django.http import HttpRequest, JsonResponse


def health(request: HttpRequest) -> JsonResponse:
    """Chequeo de salud para Render: confirma que el proceso responde."""
    return JsonResponse({"status": "ok", "app": "cauce"})
