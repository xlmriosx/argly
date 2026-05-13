import requests
from datetime import datetime

AMBITO_BASE = "https://mercados.ambito.com/riesgopais"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; argly/1.0)",
    "Accept": "application/json",
    "Referer": "https://www.ambito.com/",
}

TIMEOUT = 8  # segundos


def get_actual() -> dict:
    """
    Consulta el endpoint /variacion-ultimo de Ámbito.
    Representa el valor actual del riesgo país.

    Respuesta cruda de Ámbito:
      {
        "ultimo":           "557",
        "fecha":            "24-04-2026",
        "variacion":        "1,46%",
        "class-variacion":  "up-red"
      }

    Retorna:
      {
        "ultimo":     557,
        "fecha":      "2026-04-24",
        "variacion":  1.46,
        "tendencia":  "sube",       →  "sube" | "baja" | "neutro"
        "fuente":     "ambito.com"
      }
    """
    resp = requests.get(
        f"{AMBITO_BASE}/variacion-ultimo", headers=HEADERS, timeout=TIMEOUT
    )
    resp.raise_for_status()
    raw = resp.json()

    return {
        "ultimo": _parse_int(raw.get("ultimo")),
        "fecha": _normalizar_fecha(raw.get("fecha", "")),
        "variacion": _parse_porcentaje(raw.get("variacion")),
        "tendencia": _parse_tendencia(raw.get("class-variacion")),
        "fuente": "ambito.com",
    }


def get_anterior() -> dict:
    """
    Consulta el endpoint /jornada de Ámbito.
    Representa el cierre de la jornada anterior.

    Respuesta cruda de Ámbito:
      {
        "ultimo":             "510",
        "fecha":              "11-05-2026 19:30:02",
        "valor":              "510",
        "varpesos":           "-14",
        "variacion-nombre":   "Var. puntos"
      }

    Retorna:
      {
        "ultimo":             510,
        "fecha":              "2026-05-11",
        "variacion_puntos":   -14,
        "fuente":             "ambito.com"
      }
    """
    resp = requests.get(f"{AMBITO_BASE}/jornada", headers=HEADERS, timeout=TIMEOUT)
    resp.raise_for_status()
    raw = resp.json()

    fecha_hora = raw.get("fecha", "")
    fecha, _ = _split_fecha_hora(fecha_hora)

    return {
        "ultimo": _parse_int(raw.get("ultimo")),
        "fecha": fecha,
        "variacion_puntos": _parse_int(raw.get("varpesos")),
        "fuente": "ambito.com",
    }


def get_historico(desde: str, hasta: str) -> list[dict]:
    """
    Consulta el endpoint /historico-general/{desde}/{hasta} de Ámbito.

    Parámetros:
      desde / hasta: YYYY-MM-DD

    Respuesta cruda de Ámbito (array, primer elemento es el header):
      [
        ["Fecha", "Puntos"],
        ["08-05-2026", "510,00"],
        ["07-05-2026", "522,00"],
        ...
      ]

    Retorna:
      [
        { "fecha": "2026-05-08", "valor": 510 },
        { "fecha": "2026-05-07", "valor": 522 },
        ...
      ]
    """
    _validar_fecha(desde, "desde")
    _validar_fecha(hasta, "hasta")

    url = f"{AMBITO_BASE}/historico-general/{desde}/{hasta}"
    resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    resp.raise_for_status()
    raw = resp.json()

    # El primer elemento es el header ["Fecha", "Puntos"], lo salteamos
    filas = raw[1:] if raw else []

    return [
        {
            "fecha": _normalizar_fecha(fila[0]),  # "08-05-2026" → "2026-05-08"
            "valor": _parse_float(fila[1]),  # "510,00"     → 510
        }
        for fila in filas
        if len(fila) == 2
    ]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _split_fecha_hora(fecha_hora: str) -> tuple[str, str]:
    """
    "11-05-2026 19:30:02" → ("2026-05-11", "19:30:02")
    """
    try:
        partes = fecha_hora.strip().split(" ")
        fecha = _normalizar_fecha(partes[0])
        hora = partes[1] if len(partes) > 1 else ""
        return fecha, hora
    except Exception:
        return "", ""


def _normalizar_fecha(fecha_str: str) -> str:
    """
    "08-05-2026" (DD-MM-YYYY) → "2026-05-08" (YYYY-MM-DD)
    Si ya viene en YYYY-MM-DD la devuelve igual.
    """
    if not fecha_str:
        return ""
    try:
        return datetime.strptime(fecha_str.strip(), "%d-%m-%Y").strftime("%Y-%m-%d")
    except ValueError:
        return fecha_str.strip()


def _validar_fecha(fecha_str: str, nombre: str) -> None:
    """Lanza ValueError si la fecha no tiene formato YYYY-MM-DD."""
    try:
        datetime.strptime(fecha_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"El parámetro '{nombre}' debe tener formato YYYY-MM-DD")


def _parse_int(valor) -> int | None:
    try:
        return int(str(valor).replace(",", "").strip())
    except (ValueError, TypeError):
        return None


def _parse_float(valor) -> int | None:
    """
    "510,00" → 510
    El EMBI son puntos básicos enteros, el decimal de Ámbito no aporta info.
    """
    try:
        return int(float(str(valor).replace(",", ".").strip()))
    except (ValueError, TypeError):
        return None


def _parse_porcentaje(valor: str) -> float | None:
    """
    "1,46%" → 1.46
    "-0,83%" → -0.83
    """
    try:
        return float(str(valor).replace("%", "").replace(",", ".").strip())
    except (ValueError, TypeError):
        return None


def _parse_tendencia(class_variacion: str) -> str:
    """
    "up-red"    → "sube"
    "down-green"→ "baja"
    cualquier otro → "neutro"

    Nota: en riesgo país "up" es rojo (malo) y "down" es verde (bueno),
    al revés de una acción. Ámbito refleja eso en los nombres de clase.
    """
    if not class_variacion:
        return "neutro"
    val = class_variacion.lower()
    if "up" in val:
        return "sube"
    if "down" in val:
        return "baja"
    return "neutro"
