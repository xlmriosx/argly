# api/routes/legacy/icl.py
from flask import Blueprint, request
from api.services.data_loader import get_icl, get_icl_history, get_icl_range
from api.utils.responses import success, error

SUNSET_DATE = "Fri, 01 Jan 2027 00:00:00 GMT"
V1_BASE = "https://api.argly.com.ar/v1/icl"

icl_bp = Blueprint("icl", __name__, url_prefix="/api/icl")


@icl_bp.after_request
def add_deprecation_headers(response):
    response.headers["Deprecation"] = "true"
    response.headers["Sunset"] = SUNSET_DATE
    response.headers["Link"] = f'<{V1_BASE}>; rel="successor-version"'
    return response


@icl_bp.route("/", methods=["GET"])
def obtener_icl():
    data = get_icl()
    if not data:
        return error("No hay datos de ICL disponibles", 404)
    return success(data)


@icl_bp.route("/history", methods=["GET"])
def obtener_icl_history():
    data = get_icl_history()
    if not data:
        return error("No hay historial de ICL disponible", 404)
    return success(data)


@icl_bp.route("/range", methods=["GET"])
def obtener_icl_rango():
    desde = request.args.get("desde")
    hasta = request.args.get("hasta")
    if not desde or not hasta:
        return error("Parámetros 'desde' y 'hasta' requeridos (YYYY-MM-DD)", 400)
    return success(get_icl_range(desde, hasta))
