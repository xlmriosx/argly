import requests
import urllib3
from utils import save_dataset_json, formatear_fecha_bcra

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CER_ID = "3540"


def obtener_cer_actual():
    url = "https://www.bcra.gob.ar/api/endpoints/principales-variables-ultimas.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        serie = response.json().get("series", {}).get(CER_ID)

        if not serie:
            print(f"⚠ No se encontró la serie {CER_ID}")
            return None

        return {
            "fecha": formatear_fecha_bcra(serie["fecha"]),
            "valor": float(serie["valor"]),
            "descripcion": "Coeficiente de Estabilización de Referencia (CER)",
        }

    except Exception as e:
        print(f"Error scraping CER: {e}")
        return None


def merge_cer(historico, nuevo):
    if not nuevo:
        return historico

    for item in historico:
        if item["fecha"] == nuevo["fecha"]:
            print(f"ℹ CER {nuevo['fecha']} ya existe")
            return historico

    historico.append(nuevo)
    print(f"✔ CER agregado: {nuevo['fecha']}")
    return historico


if __name__ == "__main__":
    historico = []
    cer_data = obtener_cer_actual()
    historico = merge_cer(historico, cer_data)
    save_dataset_json(dataset="cer", data=historico)
