# fastapi_app.py

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from node_edge.processor import SensorDataProcessor
from node_edge.db import database


app = FastAPI()

class SensorData(BaseModel):
    co2: float
    temperatura: float
    humedad: float
    presion: float
    luz: float
    ruido: float

# Configurar un objeto de procesador de datos
processor = SensorDataProcessor()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/telemetry/{token}")
async def receive_telemetry(token: str, data: SensorData, request: Request):
    """
    Recibe los datos de los sensores, los valida,
    los guarda en PostgreSQL y los envía a ThingsBoard.
    """
    print(f"🚀 Recibiendo datos para el token {token}: {data.dict()}")

    # Convertir los datos a un diccionario
    sensor_data = data.dict()

    # Validar los datos sin normalizarlos
    print(f"🔧 Validando los datos sin normalizarlos...")
    processed_data = processor.validate_and_omit(sensor_data)
    print(f"✅ Datos procesados: {processed_data}")

    # Enviar a ThingsBoard
    print(f"🌐 Enviando datos a ThingsBoard...")
    success = processor.send_data_to_thingsboard(token, processed_data)

    if success:
        # Obtener IP de quien envía la telemetría
        client_ip = request.client.host

        # Guardar en PostgreSQL
        print(f"💾 Guardando datos en PostgreSQL desde IP: {client_ip}")
        await processor.save_to_postgres(processed_data, token, client_ip)

        print("✅ Datos enviados correctamente.")
        return {"message": "Datos procesados y enviados correctamente."}
    else:
        print("❌ Error al enviar los datos a ThingsBoard.")
        raise HTTPException(status_code=500, detail="Error al enviar datos a ThingsBoard")
