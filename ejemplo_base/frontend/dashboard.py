import os
import sys

# Para que Streamlit encuentre el paquete backend
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import altair as alt
from backend.api import autenticar_tenant, obtener_dispositivos, obtener_telemetria_dispositivo

# ─── Configuración de la página ────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard UrbIA – Sensor único",
    layout="wide"
)
st.title("🌡️ Dashboard UrbIA – Últimas lecturas de un sensor")

# ─── Paso 1: Autenticación ─────────────────────────────────────────────────────
token = autenticar_tenant()
if not token:
    st.error("❌ No se pudo autenticar con ThingsBoard")
    st.stop()

# ─── Paso 2: Selección de dispositivo ──────────────────────────────────────────
devices = obtener_dispositivos(token)
if not devices:
    st.warning("⚠️ No hay dispositivos disponibles")
    st.stop()

device_map  = {d["name"]: d["id"]["id"] for d in devices}
device_name = st.selectbox("Selecciona un dispositivo", list(device_map.keys()))
device_id   = device_map[device_name]

# ─── Paso 3: Selección de sensor ───────────────────────────────────────────────
all_sensors = ["temperatura", "humedad", "co2", "presion", "luz", "ruido"]
sensor      = st.selectbox("Selecciona un sensor", all_sensors)

# ─── Paso 4: Número de lecturas ────────────────────────────────────────────────
n_points = st.selectbox("Últimas N lecturas", [10, 20, 30, 40, 50], index=0)

# ─── Paso 5: Obtener telemetría ────────────────────────────────────────────────
# Pedimos algo de margen de tiempo (180 min) y limitamos con `limit=n_points`
df = obtener_telemetria_dispositivo(
    device_id=device_id,
    token=token,
    variables=[sensor],
    minutos=180,
    limit=n_points
)

if not isinstance(df, pd.DataFrame) or df.empty:
    st.warning(f"⚠️ No hay datos para el sensor **{sensor}**")
    st.stop()

# ─── Paso 6: Filtrar y ordenar ─────────────────────────────────────────────────
df_sensor = (
    df[df["sensor"] == sensor]
      .sort_values("timestamp")
      .tail(n_points)
)

# ─── Paso 7: Gráfica ────────────────────────────────────────────────────────────
st.markdown(f"### 📈 {device_name} — Sensor **{sensor}** (últimas {n_points} lecturas)")
chart = (
    alt.Chart(df_sensor)
       .mark_line(point=True)
       .encode(
           x=alt.X("timestamp:T", title="Fecha y Hora"),
           y=alt.Y("valor:Q",    title="Valor"),
           tooltip=["timestamp:T", "valor:Q"]
       )
       .properties(height=400)
       .interactive()
)
st.altair_chart(chart, use_container_width=True)
