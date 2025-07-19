# backend/api.py

from fastapi import FastAPI, HTTPException, Query
import requests
import time
import pandas as pd
from typing import List, Optional
from requests.exceptions import RequestException, HTTPError, Timeout, ConnectionError

# ─── Configuración de ThingsBoard ──────────────────────────────────────────────
BASE_URL        = "https://inti-data.ngrok.io"
TENANT_USER     = "tenant@thingsboard.org"
TENANT_PASSWORD = "tenant"

app = FastAPI()

def autenticar_tenant() -> Optional[str]:
    url     = f"{BASE_URL}/api/auth/login"
    payload = {"username": TENANT_USER, "password": TENANT_PASSWORD}
    try:
        resp = requests.post(url, json=payload)
        resp.raise_for_status()
        return resp.json().get("token")
    except Exception as e:
        print("❌ Error autenticando:", e)
        return None

def obtener_dispositivos(token: str) -> List[dict]:
    url     = f"{BASE_URL}/api/tenant/devices?pageSize=100&page=0"
    headers = {"X-Authorization": f"Bearer {token}"}
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json().get("data", [])
    except Exception as e:
        print("❌ Error obteniendo dispositivos:", e)
        return []

def obtener_telemetria_dispositivo(
    device_id:  str,
    token:      str,
    variables:  List[str],
    minutos:    int = 60,
    limit:      int = 10
) -> pd.DataFrame:
    """
    Devuelve un DataFrame con las últimas `limit` lecturas de
    las claves en `variables` para el dispositivo `device_id`.
    """
    ts_actual = int(time.time() * 1000)
    ts_inicio = ts_actual - minutos * 60 * 1000
    url    = f"{BASE_URL}/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries"
    params = {
        "startTs": ts_inicio,
        "endTs":   ts_actual,
        "keys":    ",".join(variables),
        "agg":     "NONE",
        "limit":   limit
    }
    headers = {"X-Authorization": f"Bearer {token}"}
    try:
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        datos = resp.json()
        registros = []
        for key, lecturas in datos.items():
            for l in lecturas:
                registros.append({
                    "timestamp": pd.to_datetime(int(l["ts"]), unit="ms"),
                    "sensor":    key,
                    "valor":     float(l["value"])
                })
        return pd.DataFrame(registros)
    except Exception as e:
        print("❌ Error obteniendo telemetría:", e)
        return pd.DataFrame()

@app.get("/telemetria")
def api_telemetria(
    # puedes pasar: ?variables=co2&variables=temperatura&minutos=120&limit=20
    variables: List[str] = Query(
        default=["temperatura","humedad","co2","presion","luz","ruido"],
        description="Lista de telemetría a solicitar"
    ),
    minutos: int = Query(60, description="Intervalo en minutos atrás"),
    limit:   int = Query(10, description="Número de lecturas a devolver")
):
    token = autenticar_tenant()
    if not token:
        raise HTTPException(401, "No se pudo autenticar")
    devices = obtener_dispositivos(token)
    if not devices:
        raise HTTPException(404, "No se encontraron dispositivos")
    device_id = devices[0]["id"]["id"]
    df = obtener_telemetria_dispositivo(device_id, token, variables, minutos=minutos, limit=limit)
    if df.empty:
        return {"telemetria": []}
    return {"telemetria": df.to_dict(orient="records")}
