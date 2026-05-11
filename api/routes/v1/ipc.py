# api/routes/v1/ipc.py
from flask import Blueprint, request
from api.services.data_loader import get_ipc, get_ipc_history, get_ipc_range
from api.utils.responses import success, error

ipc_v1_bp = Blueprint("ipc_v1", __name__, url_prefix="/v1/ipc")


@ipc_v1_bp.route("/", methods=["GET"])
def obtener_ipc():
    desde = request.args.get("desde")
    hasta = request.args.get("hasta")

    if desde and hasta:
        data = get_ipc_range(desde, hasta)
        if data is None:
            return error("No hay datos para el rango solicitado", 404)
        return success(data)

    if "historico" in request.args:
        data = get_ipc_history()
        if not data:
            return error("No hay histórico de IPC disponible", 404)
        return success(data)

    data = get_ipc()
    if not data:
        return error("No hay datos de IPC disponibles", 404)
    return success(data)
