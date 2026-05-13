# api/routes/v1/combustibles.py
from flask import Blueprint, request
from api.services.data_loader import (
    get_combustibles_by_provincia,
    get_combustibles_by_empresa,
    get_promedio_combustible,
)
from api.utils.responses import success, error

combustibles_v1_bp = Blueprint(
    "combustibles_v1", __name__, url_prefix="/v1/combustibles"
)


@combustibles_v1_bp.route("/", methods=["GET"])
def obtener_combustibles():
    provincia = request.args.get("provincia")
    empresa = request.args.get("empresa")

    if provincia and empresa:
        return error("Usar 'provincia' o 'empresa', no ambos a la vez", 400)

    if provincia:
        data = get_combustibles_by_provincia(provincia)
        if not data:
            return error("No se encontraron datos para esa provincia", 404)
        return success(data)

    if empresa:
        data = get_combustibles_by_empresa(empresa)
        if not data:
            return error("No se encontraron datos para esa empresa", 404)
        return success(data)

    return error("Debe proveer 'provincia' o 'empresa' como parámetro", 400)


@combustibles_v1_bp.route("/promedio", methods=["GET"])
def promedio_combustible():
    provincia = request.args.get("provincia")
    combustible = request.args.get("combustible")

    if not provincia or not combustible:
        return error("Parámetros 'provincia' y 'combustible' requeridos", 400)

    promedio = get_promedio_combustible(provincia, combustible)
    if promedio is None:
        return error("No hay datos suficientes para calcular el promedio", 404)

    return success(
        {
            "provincia": provincia.lower(),
            "combustible": combustible.replace("-", " ").title(),
            "precio_promedio": promedio,
        }
    )
