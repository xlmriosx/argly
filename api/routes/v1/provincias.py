# api/routes/v1/provincias.py
from flask import Blueprint
from api.services.data_loader import get_provincias
from api.utils.responses import success, error

provincias_v1_bp = Blueprint("provincias_v1", __name__, url_prefix="/v1/provincias")


@provincias_v1_bp.route("/", methods=["GET"])
def obtener_provincias():
    data = get_provincias()
    if not data:
        return error("No hay datos geográficos disponibles", 404)
    return success(data)
