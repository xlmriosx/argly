import requests
import urllib3
from utils import save_dataset_json, formatear_fecha_bcra

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ICL_ID = "7988"


def obtener_icl_actual():
    url = "https://www.bcra.gob.ar/api/endpoints/principales-variables-ultimas.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        data = response.json()

        serie = data.get("series", {}).get(ICL_ID)
        if not serie:
            print(f"⚠ No se encontró la serie {ICL_ID}")
            return None

        return {
            "fecha": formatear_fecha_bcra(serie["fecha"]),
            "valor": float(serie["valor"]),
            "descripcion": "ICL - Ley 27.551",
        }

    except Exception as e:
        print(f"Error: {e}")
        return None


def merge_icl(historico, nuevo_dato):
    if not nuevo_dato:
        return historico

    for item in historico:
        if item["fecha"] == nuevo_dato["fecha"]:
            print(f"ℹ ICL {nuevo_dato['fecha']} ya existe")
            return historico

    historico.append(nuevo_dato)
    print(f"✔ ICL agregado: {nuevo_dato['fecha']}")
    return historico


if __name__ == "__main__":
    historico = []
    icl_data = obtener_icl_actual()
    historico = merge_icl(historico, icl_data)
    save_dataset_json(dataset="icl", data=historico)
