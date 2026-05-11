# api/routes/v1/medicamentos.py
from flask import Blueprint
from api.services.medicamentos_service import obtener_medicamentos
from api.utils.responses import success, error
from urllib.parse import unquote

medicamentos_v1_bp = Blueprint(
    "medicamentos_v1", __name__, url_prefix="/v1/medicamentos"
)


@medicamentos_v1_bp.route("/<medicamento>", methods=["GET"])
def obtener_medicamento(medicamento):
    try:
        nombre = unquote(medicamento)
        data = obtener_medicamentos(nombre)
        return success(data)
    except Exception as e:
        return error(f"Error consultando medicamentos: {e}", 500)
