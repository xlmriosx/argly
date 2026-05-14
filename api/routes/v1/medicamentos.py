from flask import Blueprint, request
from api.services.medicamentos_service import obtener_medicamentos
from api.utils.responses import success, error
from urllib.parse import unquote

PARAMS_VALIDOS = {"nombre"}

medicamentos_v1_bp = Blueprint(
    "medicamentos_v1", __name__, url_prefix="/v1/medicamentos"
)


@medicamentos_v1_bp.route("/", methods=["GET"])
def obtener_medicamento():
    params_recibidos = set(request.args.keys())
    params_invalidos = params_recibidos - PARAMS_VALIDOS

    if params_invalidos:
        return error(
            f"Parámetro(s) no reconocido(s): {', '.join(params_invalidos)}. Parámetros válidos: {', '.join(PARAMS_VALIDOS)}",
            400,
        )

    nombre = unquote(request.args.get("nombre", "").strip())

    if not nombre:
        return error("El parámetro 'nombre' es requerido (ej: ?nombre=ibuprofeno)", 400)

    try:
        data = obtener_medicamentos(nombre)
        return success(data)
    except Exception as e:
        return error(f"Error consultando medicamentos: {e}", 500)
