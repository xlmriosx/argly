# api/routes/v1/uva.py
from flask import Blueprint, request
from api.services.data_loader import get_uva, get_uva_history, get_uva_range
from api.utils.responses import success, error

uva_v1_bp = Blueprint("uva_v1", __name__, url_prefix="/v1/uva")


@uva_v1_bp.route("/", methods=["GET"])
def obtener_uva():
    desde = request.args.get("desde")
    hasta = request.args.get("hasta")

    if desde and hasta:
        data = get_uva_range(desde, hasta)
        if data is None:
            return error("No hay datos para el rango solicitado", 404)
        return success(data)

    if "historico" in request.args:
        data = get_uva_history()
        if not data:
            return error("No hay historial de UVA disponible", 404)
        return success(data)

    data = get_uva()
    if not data:
        return error("No hay datos de UVA disponibles", 404)
    return success(data)
