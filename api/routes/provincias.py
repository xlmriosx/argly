# api/routes/legacy/provincias.py
from flask import Blueprint
from api.services.data_loader import get_provincias
from api.utils.responses import success, error

SUNSET_DATE = "Fri, 01 Jan 2027 00:00:00 GMT"
V1_BASE = "https://api.argly.com.ar/v1/provincias"

provincias_bp = Blueprint("provincias", __name__, url_prefix="/api/provincias")


@provincias_bp.after_request
def add_deprecation_headers(response):
    response.headers["Deprecation"] = "true"
    response.headers["Sunset"] = SUNSET_DATE
    response.headers["Link"] = f'<{V1_BASE}>; rel="successor-version"'
    return response


@provincias_bp.route("/", methods=["GET"])
def obtener_provincias():
    data = get_provincias()
    if not data:
        return error("No hay datos geográficos disponibles", 404)
    return success(data)
