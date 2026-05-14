# api/routes/v1/diputados.py
from flask import Blueprint, request
from api.utils.responses import success, error
from api.services.diputados_service import get_diputados

PARAMS_VALIDOS = {"distrito", "bloque"}

diputados_v1_bp = Blueprint("diputados_v1", __name__, url_prefix="/v1/diputados")


@diputados_v1_bp.route("/", methods=["GET"])
def obtener_diputados():
    params_recibidos = set(request.args.keys())
    params_invalidos = params_recibidos - PARAMS_VALIDOS

    if params_invalidos:
        return error(
            f"Parámetro(s) no reconocido(s): {', '.join(params_invalidos)}. Parámetros válidos: {', '.join(PARAMS_VALIDOS)}",
            400,
        )

    distrito = request.args.get("distrito", "").strip()
    bloque = request.args.get("bloque", "").strip()

    if "distrito" in params_recibidos and not distrito:
        return error(
            "El parámetro 'distrito' no puede estar vacío (ej: ?distrito=chaco)", 400
        )

    if "bloque" in params_recibidos and not bloque:
        return error(
            "El parámetro 'bloque' no puede estar vacío (ej: ?bloque=ucr)", 400
        )

    if " " in distrito:
        return error(
            "El parámetro 'distrito' no puede contener espacios, usá guiones (ej: ?distrito=buenos-aires)",
            400,
        )

    if " " in bloque:
        return error(
            "El parámetro 'bloque' no puede contener espacios, usá guiones (ej: ?bloque=la-libertad-avanza)",
            400,
        )

    try:
        data = get_diputados(distrito=distrito or None, bloque=bloque or None)
        if not data["datos"]:
            return error("No se encontraron diputados con los filtros indicados", 404)
        return success(data)
    except FileNotFoundError as e:
        return error(str(e), 503)
    except Exception as e:
        return error(f"Error interno: {e}", 500)
