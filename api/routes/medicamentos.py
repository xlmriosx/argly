# api/routes/legacy/medicamentos.py
from flask import Blueprint, jsonify
from api.services.medicamentos_service import obtener_medicamentos
from urllib.parse import unquote

SUNSET_DATE = "Fri, 01 Jan 2027 00:00:00 GMT"
V1_BASE = "https://api.argly.com.ar/v1/medicamentos"

medicamentos_bp = Blueprint("medicamentos", __name__, url_prefix="/api/medicamentos")


@medicamentos_bp.after_request
def add_deprecation_headers(response):
    response.headers["Deprecation"] = "true"
    response.headers["Sunset"] = SUNSET_DATE
    response.headers["Link"] = f'<{V1_BASE}>; rel="successor-version"'
    return response


@medicamentos_bp.route("/<medicamento>", methods=["GET"])
def medicamentos(medicamento):
    try:
        nombre = unquote(medicamento)
        data = obtener_medicamentos(nombre)
        return jsonify(data)
    except Exception as e:
        return (
            jsonify({"error": "Error consultando medicamentos", "detalle": str(e)}),
            500,
        )
