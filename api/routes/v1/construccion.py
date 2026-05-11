# api/routes/v1/construccion.py
from flask import Blueprint
from api.services.data_loader import get_construccion
from api.utils.responses import success, error

construccion_v1_bp = Blueprint(
    "construccion_v1", __name__, url_prefix="/v1/construccion"
)


@construccion_v1_bp.route("/", methods=["GET"])
def obtener_construccion():
    data = get_construccion()
    if not data:
        return error("No hay datos de construcción disponibles", 404)
    return success(data)
