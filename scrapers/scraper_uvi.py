import requests
import urllib3
from utils import save_dataset_json, formatear_fecha_bcra

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

UVI_ID = "7914"


def obtener_uvi_actual():
    url = "https://www.bcra.gob.ar/api/endpoints/principales-variables-ultimas.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        serie = response.json().get("series", {}).get(UVI_ID)

        if not serie:
            print(f"⚠ No se encontró la serie {UVI_ID}")
            return None

        return {
            "fecha": formatear_fecha_bcra(serie["fecha"]),
            "valor": float(serie["valor"]),
            "descripcion": "Unidad de Vivienda (UVI)",
        }

    except Exception as e:
        print(f"Error scraping UVI: {e}")
        return None


def merge_uvi(historico, nuevo_dato):
    if not nuevo_dato:
        return historico

    for item in historico:
        if item["fecha"] == nuevo_dato["fecha"]:
            print(f"ℹ UVI {nuevo_dato['fecha']} ya existe")
            return historico

    historico.append(nuevo_dato)
    print(f"✔ UVI agregado: {nuevo_dato['fecha']}")
    return historico


if __name__ == "__main__":
    historico = []
    uvi_data = obtener_uvi_actual()
    historico = merge_uvi(historico, uvi_data)
    save_dataset_json(dataset="uvi", data=historico)
