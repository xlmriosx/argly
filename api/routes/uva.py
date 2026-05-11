# api/routes/legacy/uva.py
from flask import Blueprint, request
from api.services.data_loader import get_uva, get_uva_history, get_uva_range
from api.utils.responses import success, error

SUNSET_DATE = "Fri, 01 Jan 2027 00:00:00 GMT"
V1_BASE = "https://api.argly.com.ar/v1/uva"

uva_bp = Blueprint("uva", __name__, url_prefix="/api/uva")


@uva_bp.after_request
def add_deprecation_headers(response):
    response.headers["Deprecation"] = "true"
    response.headers["Sunset"] = SUNSET_DATE
    response.headers["Link"] = f'<{V1_BASE}>; rel="successor-version"'
    return response


@uva_bp.route("/", methods=["GET"])
def obtener_uva():
    data = get_uva()
    if not data:
        return error("No hay datos de UVA disponibles", 404)
    return success(data)


@uva_bp.route("/history", methods=["GET"])
def obtener_uva_history():
    data = get_uva_history()
    if not data:
        return error("No hay historial de UVA disponible", 404)
    return success(data)


@uva_bp.route("/range", methods=["GET"])
def obtener_uva_rango():
    desde = request.args.get("desde")
    hasta = request.args.get("hasta")
    if not desde or not hasta:
        return error("Parámetros 'desde' y 'hasta' requeridos (YYYY-MM-DD)", 400)
    return success(get_uva_range(desde, hasta))
