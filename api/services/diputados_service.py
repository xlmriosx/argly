import json
import os

DATA_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "diputados", "diputados.json"
)


def get_diputados(distrito=None, bloque=None):
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError("No hay datos de diputados disponibles.")

    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)

    diputados = data["datos"]

    if distrito:
        distrito_normalizado = distrito.replace("-", " ")
        diputados = [
            d
            for d in diputados
            if d["distrito"].lower() == distrito_normalizado.lower()
        ]

    if bloque:
        bloque_normalizado = bloque.replace("-", " ")
        diputados = [
            d for d in diputados if bloque_normalizado.lower() in d["bloque"].lower()
        ]

    return {"total": len(diputados), "fuente": data["fuente"], "datos": diputados}
