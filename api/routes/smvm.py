from flask import Blueprint, request
from api.utils.responses import success, error
from api.services.data_loader import get_smvm, get_smvm_history, get_smvm_range

smvm_bp = Blueprint("smvm", __name__, url_prefix="/v1")


@smvm_bp.route("/smvm", methods=["GET"])
def smvm():
    """
    Salario Mínimo Vital y Móvil (SMVM)

    Query params opcionales:
      - desde (YYYY-MM-DD)
      - hasta (YYYY-MM-DD)
      - historico (true/false)

    Comportamiento:
      - sin params → latest
      - historico=true → todo el histórico
      - desde/hasta → rango
    """

    desde = request.args.get("desde")
    hasta = request.args.get("hasta")
    historico = request.args.get("historico")

    try:
        # ------------------------
        # HISTÓRICO COMPLETO
        # ------------------------
        if historico == "true":
            data = get_smvm_history()
            return success(data)

        # ------------------------
        # RANGO
        # ------------------------
        if desde and hasta:
            data = get_smvm_range(desde, hasta)

            if not data:
                return error("No hay datos en el rango especificado", 404)

            return success(data)

        # ------------------------
        # VALIDACIÓN PARCIAL
        # ------------------------
        if (desde and not hasta) or (hasta and not desde):
            return error("Debe enviar 'desde' y 'hasta' juntos", 400)

        # ------------------------
        # LATEST (default)
        # ------------------------
        data = get_smvm()

        if not data:
            return error("No hay datos disponibles", 404)

        return success(data)

    except FileNotFoundError as e:
        return error(str(e), 503)
    except Exception as e:
        return error(f"Error interno: {e}", 500)
