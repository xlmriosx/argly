# api/routes/v1/riesgo_pais.py
import re
from flask import Blueprint, request
from api.utils.responses import success, error
from api.services.riesgo_pais import get_actual, get_anterior, get_historico

PARAMS_VALIDOS = {"desde", "hasta", "anterior"}
FORMATO_FECHA = re.compile(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$")

riesgo_pais_v1_bp = Blueprint("riesgo_pais_v1", __name__, url_prefix="/v1/riesgo-pais")


def validar_fecha(valor, nombre):
    if not FORMATO_FECHA.match(valor):
        return error(
            f"El parámetro '{nombre}' debe tener formato YYYY-MM-DD (ej: 2024-01-15)",
            400,
        )
    return None


@riesgo_pais_v1_bp.route("/", methods=["GET"])
def obtener_riesgo_pais():
    params_recibidos = set(request.args.keys())
    params_invalidos = params_recibidos - PARAMS_VALIDOS

    if params_invalidos:
        return error(
            f"Parámetro(s) no reconocido(s): {', '.join(params_invalidos)}. Parámetros válidos: {', '.join(PARAMS_VALIDOS)}",
            400,
        )

    desde = request.args.get("desde")
    hasta = request.args.get("hasta")
    anterior = request.args.get("anterior", "").lower()

    if "anterior" in params_recibidos:
        if anterior != "true":
            return error(
                "El parámetro 'anterior' solo acepta el valor 'true' (ej: ?anterior=true)",
                400,
            )
        try:
            data = get_anterior()
            if not data:
                return error("No hay datos disponibles", 404)
            return success(data)
        except ConnectionError as e:
            return error(f"Error al conectar con la fuente de datos: {e}", 503)
        except Exception as e:
            return error(f"Error interno: {e}", 500)

    if "desde" in params_recibidos or "hasta" in params_recibidos:
        if not desde or not hasta:
            return error(
                "Los parámetros 'desde' y 'hasta' son requeridos en conjunto y no pueden estar vacíos (formato: YYYY-MM-DD)",
                400,
            )

        err = validar_fecha(desde, "desde") or validar_fecha(hasta, "hasta")
        if err:
            return err

        try:
            data = get_historico(desde, hasta)
            if not data:
                return error("No hay datos en el rango especificado", 404)
            return success(data)
        except ValueError as e:
            return error(str(e), 400)
        except ConnectionError as e:
            return error(f"Error al conectar con la fuente de datos: {e}", 503)
        except Exception as e:
            return error(f"Error interno: {e}", 500)

    try:
        data = get_actual()
        if not data:
            return error("No hay datos disponibles", 404)
        return success(data)
    except ConnectionError as e:
        return error(f"Error al conectar con la fuente de datos: {e}", 503)
    except Exception as e:
        return error(f"Error interno: {e}", 500)
