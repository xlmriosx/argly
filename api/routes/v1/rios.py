# api/routes/v1/rios.py
from flask import Blueprint, request
from api.services.data_loader import get_rios, get_rio_by_nombre
from api.utils.responses import success, error

PARAMS_VALIDOS = {"nombre"}

rios_v1_bp = Blueprint("rios_v1", __name__, url_prefix="/v1/rios")


@rios_v1_bp.route("/", methods=["GET"])
def obtener_rios():
    params_recibidos = set(request.args.keys())
    params_invalidos = params_recibidos - PARAMS_VALIDOS

    if params_invalidos:
        return error(
            f"Parámetro(s) no reconocido(s): {', '.join(params_invalidos)}. Parámetros válidos: {', '.join(PARAMS_VALIDOS)}",
            400,
        )

    nombre = request.args.get("nombre")

    if nombre:
        data = get_rio_by_nombre(nombre)
        if not data:
            return error("Río no encontrado", 404)
        return success(data)

    data = get_rios()
    if not data:
        return error("No hay datos de ríos disponibles", 404)
    return success(data)
