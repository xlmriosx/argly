# api/routes/legacy/cer.py
from flask import Blueprint, request
from api.services.data_loader import get_cer, get_cer_history, get_cer_range
from api.utils.responses import success, error

SUNSET_DATE = "Fri, 01 Jan 2027 00:00:00 GMT"
V1_BASE = "https://api.argly.com.ar/v1/cer"

cer_bp = Blueprint("cer", __name__, url_prefix="/api/cer")


@cer_bp.after_request
def add_deprecation_headers(response):
    response.headers["Deprecation"] = "true"
    response.headers["Sunset"] = SUNSET_DATE
    response.headers["Link"] = f'<{V1_BASE}>; rel="successor-version"'
    return response


@cer_bp.route("/", methods=["GET"])
def obtener_cer():
    data = get_cer()
    if not data:
        return error("No hay datos de CER disponibles", 404)
    return success(data)


@cer_bp.route("/history", methods=["GET"])
def obtener_cer_history():
    data = get_cer_history()
    if not data:
        return error("No hay historial de CER disponible", 404)
    return success(data)


@cer_bp.route("/range", methods=["GET"])
def obtener_cer_rango():
    desde = request.args.get("desde")
    hasta = request.args.get("hasta")
    if not desde or not hasta:
        return error("Parámetros 'desde' y 'hasta' requeridos (YYYY-MM-DD)", 400)
    return success(get_cer_range(desde, hasta))
