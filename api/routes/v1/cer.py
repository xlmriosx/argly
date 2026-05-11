# api/routes/v1/cer.py
from flask import Blueprint, request
from api.services.data_loader import get_cer, get_cer_history, get_cer_range
from api.utils.responses import success, error

cer_v1_bp = Blueprint("cer_v1", __name__, url_prefix="/v1/cer")


@cer_v1_bp.route("/", methods=["GET"])
def obtener_cer():
    desde = request.args.get("desde")
    hasta = request.args.get("hasta")

    if desde and hasta:
        data = get_cer_range(desde, hasta)
        if data is None:
            return error("No hay datos para el rango solicitado", 404)
        return success(data)

    if "historico" in request.args:
        data = get_cer_history()
        if not data:
            return error("No hay historial de CER disponible", 404)
        return success(data)

    data = get_cer()
    if not data:
        return error("No hay datos de CER disponibles", 404)
    return success(data)
