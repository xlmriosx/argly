# api/routes/v1/ipc.py
import re
from flask import Blueprint, request
from api.services.data_loader import get_ipc, get_ipc_history, get_ipc_range
from api.utils.responses import success, error

PARAMS_VALIDOS = {"desde", "hasta", "historico"}
FORMATO_FECHA = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")

ipc_v1_bp = Blueprint("ipc_v1", __name__, url_prefix="/v1/ipc")


def validar_fecha(valor, nombre):
    if not FORMATO_FECHA.match(valor):
        return error(
            f"El parámetro '{nombre}' debe tener formato YYYY-MM (ej: 2024-01)", 400
        )
    return None


@ipc_v1_bp.route("/", methods=["GET"])
def obtener_ipc():
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
        data = get_ipc_history()
        if not data:
            return error("No hay histórico de IPC disponible", 404)
        return success(data)

    if "desde" in params_recibidos or "hasta" in params_recibidos:
        if not desde or not hasta:
            return error(
                "Los parámetros 'desde' y 'hasta' son requeridos en conjunto y no pueden estar vacíos (formato: YYYY-MM)",
                400,
            )

        err = validar_fecha(desde, "desde") or validar_fecha(hasta, "hasta")
        if err:
            return err

        data = get_ipc_range(desde, hasta)
        if data is None:
            return error("No hay datos para el rango solicitado", 404)
        return success(data)

    data = get_ipc()
    if not data:
        return error("No hay datos de IPC disponibles", 404)
    return success(data)
