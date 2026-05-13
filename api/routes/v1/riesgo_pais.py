from flask import Blueprint, request
from api.utils.responses import success, error
from api.services.riesgo_pais import get_actual, get_anterior, get_historico

riesgo_pais_v1_bp = Blueprint("riesgo_pais", __name__, url_prefix="/v1")


@riesgo_pais_v1_bp.route("/riesgo-pais", methods=["GET"])
def riesgo_pais():
    """
    Riesgo País Argentino (EMBI - JP Morgan)

    Fuente: mercados.ambito.com

    Query params opcionales:
      - anterior (true/false)
      - desde (YYYY-MM-DD)  → requiere también 'hasta'
      - hasta (YYYY-MM-DD)  → requiere también 'desde'

    Comportamiento:
      - sin params         → valor actual    (fuente: /variacion-ultimo)
      - anterior=true      → cierre anterior (fuente: /jornada)
      - desde + hasta      → histórico en rango de fechas
    """

    anterior = request.args.get("anterior")
    desde = request.args.get("desde")
    hasta = request.args.get("hasta")

    try:
        # ------------------------
        # VALIDACIÓN PARCIAL
        # ------------------------
        if (desde and not hasta) or (hasta and not desde):
            return error("Debe enviar 'desde' y 'hasta' juntos", 400)

        # ------------------------
        # RANGO HISTÓRICO
        # ------------------------
        if desde and hasta:
            data = get_historico(desde, hasta)

            if not data:
                return error("No hay datos en el rango especificado", 404)

            return success(data)

        # ------------------------
        # CIERRE ANTERIOR
        # ------------------------
        if anterior == "true":
            data = get_anterior()

            if not data:
                return error("No hay datos disponibles", 404)

            return success(data)

        # ------------------------
        # ACTUAL (default)
        # ------------------------
        data = get_actual()

        if not data:
            return error("No hay datos disponibles", 404)

        return success(data)

    except ValueError as e:
        return error(str(e), 400)
    except ConnectionError as e:
        return error(f"Error al conectar con la fuente de datos: {e}", 503)
    except Exception as e:
        return error(f"Error interno: {e}", 500)
