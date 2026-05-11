# api/routes/v1/icl.py
from flask import Blueprint, request
from api.services.data_loader import get_icl, get_icl_history, get_icl_range
from api.utils.responses import success, error

icl_v1_bp = Blueprint("icl_v1", __name__, url_prefix="/v1/icl")


@icl_v1_bp.route("/", methods=["GET"])
def obtener_icl():
    desde = request.args.get("desde")
    hasta = request.args.get("hasta")

    if desde and hasta:
        data = get_icl_range(desde, hasta)
        if data is None:
            return error("No hay datos para el rango solicitado", 404)
        return success(data)

    if "historico" in request.args:
        data = get_icl_history()
        if not data:
            return error("No hay historial de ICL disponible", 404)
        return success(data)

    data = get_icl()
    if not data:
        return error("No hay datos de ICL disponibles", 404)
    return success(data)
