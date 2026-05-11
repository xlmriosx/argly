import requests
import urllib3
from utils import save_dataset_json, formatear_fecha_bcra

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

UVA_ID = "7913"


def obtener_uva_actual():
    url = "https://www.bcra.gob.ar/api/endpoints/principales-variables-ultimas.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        serie = response.json().get("series", {}).get(UVA_ID)

        if not serie:
            print(f"⚠ No se encontró la serie {UVA_ID}")
            return None

        return {
            "fecha": formatear_fecha_bcra(serie["fecha"]),
            "valor": float(serie["valor"]),
            "descripcion": "Unidad de Valor Adquisitivo (UVA)",
        }

    except Exception as e:
        print(f"Error scraping UVA: {e}")
        return None


def merge_uva(historico, nuevo):
    if not nuevo:
        return historico

    for item in historico:
        if item["fecha"] == nuevo["fecha"]:
            print(f"ℹ UVA {nuevo['fecha']} ya existe")
            return historico

    historico.append(nuevo)
    print(f"✔ UVA agregado: {nuevo['fecha']}")
    return historico


if __name__ == "__main__":
    historico = []
    uva_data = obtener_uva_actual()
    historico = merge_uva(historico, uva_data)
    save_dataset_json(dataset="uva", data=historico)
