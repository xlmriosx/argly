# api/routes/v1/canasta.py
from flask import Blueprint, request
from api.services.data_loader import get_canasta, get_canasta_history, get_canasta_range
from api.utils.responses import success, error

canasta_v1_bp = Blueprint("canasta_v1", __name__, url_prefix="/v1/canasta")


@canasta_v1_bp.route("/", methods=["GET"])
def obtener_canasta():
    desde = request.args.get("desde")
    hasta = request.args.get("hasta")

    if desde and hasta:
        data = get_canasta_range(desde, hasta)
        if data is None:
            return error("No hay datos para el rango solicitado", 404)
        return success(data)

    if "historico" in request.args:
        data = get_canasta_history()
        if not data:
            return error("No hay histórico de canasta disponible", 404)
        return success(data)

    data = get_canasta()
    if not data:
        return error("No hay datos de canasta disponibles", 404)
    return success(data)
