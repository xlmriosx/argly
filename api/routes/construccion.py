# api/routes/legacy/construccion.py
from flask import Blueprint
from api.services.data_loader import get_construccion
from api.utils.responses import success, error

SUNSET_DATE = "Fri, 01 Jan 2027 00:00:00 GMT"
V1_BASE = "https://api.argly.com.ar/v1/construccion"

construccion_bp = Blueprint("construccion", __name__, url_prefix="/api/construccion")


@construccion_bp.after_request
def add_deprecation_headers(response):
    response.headers["Deprecation"] = "true"
    response.headers["Sunset"] = SUNSET_DATE
    response.headers["Link"] = f'<{V1_BASE}>; rel="successor-version"'
    return response


@construccion_bp.route("/", methods=["GET"])
def obtener_construccion():
    data = get_construccion()
    if not data:
        return error("No hay datos de construcción disponibles", 404)
    return success(data)
