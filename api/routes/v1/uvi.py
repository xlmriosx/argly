# api/routes/v1/uvi.py
from flask import Blueprint, request
from api.services.data_loader import get_uvi, get_uvi_history, get_uvi_range
from api.utils.responses import success, error

uvi_v1_bp = Blueprint("uvi_v1", __name__, url_prefix="/v1/uvi")


@uvi_v1_bp.route("/", methods=["GET"])
def obtener_uvi():
    desde = request.args.get("desde")
    hasta = request.args.get("hasta")

    if desde and hasta:
        data = get_uvi_range(desde, hasta)
        if data is None:
            return error("No hay datos para el rango solicitado", 404)
        return success(data)

    if "historico" in request.args:
        data = get_uvi_history()
        if not data:
            return error("No hay historial de UVI disponible", 404)
        return success(data)

    data = get_uvi()
    if not data:
        return error("No hay datos de UVI disponibles", 404)
    return success(data)
