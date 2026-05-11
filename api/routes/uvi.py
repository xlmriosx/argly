# api/routes/legacy/uvi.py
from flask import Blueprint, request
from api.services.data_loader import get_uvi, get_uvi_history, get_uvi_range
from api.utils.responses import success, error

SUNSET_DATE = "Fri, 01 Jan 2027 00:00:00 GMT"
V1_BASE = "https://api.argly.com.ar/v1/uvi"

uvi_bp = Blueprint("uvi", __name__, url_prefix="/api/uvi")


@uvi_bp.after_request
def add_deprecation_headers(response):
    response.headers["Deprecation"] = "true"
    response.headers["Sunset"] = SUNSET_DATE
    response.headers["Link"] = f'<{V1_BASE}>; rel="successor-version"'
    return response


@uvi_bp.route("/", methods=["GET"])
def obtener_uvi():
    data = get_uvi()
    if not data:
        return error("No hay datos de UVI disponibles", 404)
    return success(data)


@uvi_bp.route("/history", methods=["GET"])
def obtener_uvi_history():
    data = get_uvi_history()
    if not data:
        return error("No hay historial de UVI disponible", 404)
    return success(data)


@uvi_bp.route("/range", methods=["GET"])
def obtener_uvi_rango():
    desde = request.args.get("desde")
    hasta = request.args.get("hasta")
    if not desde or not hasta:
        return error("Parámetros 'desde' y 'hasta' requeridos (YYYY-MM-DD)", 400)
    return success(get_uvi_range(desde, hasta))
