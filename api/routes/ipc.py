# api/routes/legacy/ipc.py
from flask import Blueprint, request
from api.services.data_loader import get_ipc, get_ipc_history, get_ipc_range
from api.utils.responses import success, error

SUNSET_DATE = "Fri, 01 Jan 2027 00:00:00 GMT"
V1_BASE = "https://api.argly.com.ar/v1/ipc"

ipc_bp = Blueprint("ipc", __name__, url_prefix="/api/ipc")


@ipc_bp.after_request
def add_deprecation_headers(response):
    response.headers["Deprecation"] = "true"
    response.headers["Sunset"] = SUNSET_DATE
    response.headers["Link"] = f'<{V1_BASE}>; rel="successor-version"'
    return response


@ipc_bp.route("/", methods=["GET"])
def obtener_ipc():
    data = get_ipc()
    if not data:
        return error("No hay datos de IPC disponibles", 404)
    return success(data)


@ipc_bp.route("/history", methods=["GET"])
def obtener_ipc_historico():
    data = get_ipc_history()
    if not data:
        return error("No hay histórico de IPC disponible", 404)
    return success(data)


@ipc_bp.route("/range", methods=["GET"])
def obtener_ipc_rango():
    desde = request.args.get("desde")
    hasta = request.args.get("hasta")
    if not desde or not hasta:
        return error("Parámetros 'desde' y 'hasta' requeridos (YYYY-MM)", 400)
    data = get_ipc_range(desde, hasta)
    return success(data)
