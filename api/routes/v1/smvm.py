# api/routes/v1/smvm.py
import re
from flask import Blueprint, request
from api.utils.responses import success, error
from api.services.data_loader import get_smvm, get_smvm_history, get_smvm_range

PARAMS_VALIDOS = {"desde", "hasta", "historico"}
FORMATO_FECHA = re.compile(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$")

smvm_v1_bp = Blueprint("smvm_v1", __name__, url_prefix="/v1/smvm")


def validar_fecha(valor, nombre):
    if not FORMATO_FECHA.match(valor):
        return error(
            f"El parámetro '{nombre}' debe tener formato YYYY-MM-DD (ej: 2024-01-15)",
            400,
        )
    return None


@smvm_v1_bp.route("/", methods=["GET"])
def obtener_smvm():
    params_recibidos = set(request.args.keys())
    params_invalidos = params_recibidos - PARAMS_VALIDOS

    if params_invalidos:
        return error(
            f"Parámetro(s) no reconocido(s): {', '.join(params_invalidos)}. Parámetros válidos: {', '.join(PARAMS_VALIDOS)}",
            400,
        )

    desde = request.args.get("desde")
    hasta = request.args.get("hasta")
    historico = request.args.get("historico", "").lower()

    if "historico" in params_recibidos:
        if historico != "true":
            return error(
                "El parámetro 'historico' solo acepta el valor 'true' (ej: ?historico=true)",
                400,
            )
        data = get_smvm_history()
        if not data:
            return error("No hay histórico de SMVM disponible", 404)
        return success(data)

    if "desde" in params_recibidos or "hasta" in params_recibidos:
        if not desde or not hasta:
            return error(
                "Los parámetros 'desde' y 'hasta' son requeridos en conjunto y no pueden estar vacíos (formato: YYYY-MM-DD)",
                400,
            )

        err = validar_fecha(desde, "desde") or validar_fecha(hasta, "hasta")
        if err:
            return err

        data = get_smvm_range(desde, hasta)
        if not data:
            return error("No hay datos en el rango especificado", 404)
        return success(data)

    try:
        data = get_smvm()
        if not data:
            return error("No hay datos disponibles", 404)
        return success(data)
    except FileNotFoundError as e:
        return error(str(e), 503)
    except Exception as e:
        return error(f"Error interno: {e}", 500)
