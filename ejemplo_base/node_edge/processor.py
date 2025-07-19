import json
import requests
from node_edge.db import database  # Importa la conexión a PostgreSQL

class SensorDataProcessor:
    def __init__(self, threshold: float = 1000.0):
        """
        Inicializa el procesador de datos de sensores con un umbral específico.
        :param threshold: El valor máximo permitido para los datos de los sensores.
        """
        self.threshold = threshold  # Definimos un umbral para los valores fuera de rango
        print(f"🚀 Inicializando SensorDataProcessor con threshold = {self.threshold}")

    def validate_and_omit(self, sensor_data: dict) -> dict:
        """
        Valida los datos de los sensores y omite aquellos que están fuera del rango.
        Si un valor está fuera del rango, simplemente lo elimina.
        :param sensor_data: Diccionario con los datos de los sensores.
        :return: Diccionario con los datos validados (sin valores fuera de rango).
        """
        print(f"🔧 Validando datos: {sensor_data}")

        for sensor, value in list(sensor_data.items()):
            if value > self.threshold or value < 0:
                print(f"❌ Valor fuera de rango detectado: {value} para el sensor {sensor}")
                del sensor_data[sensor]

        print(f"✅ Datos validados y fuera de rango omitidos: {sensor_data}")
        return sensor_data

    def send_data_to_thingsboard(self, token: str, payload: dict) -> bool:
        """
        Envía los datos procesados a ThingsBoard.
        :param token: El token de autenticación para ThingsBoard.
        :param payload: Los datos del sensor a enviar.
        :return: True si los datos fueron enviados correctamente, False en caso contrario.
        """
        url = f"https://inti-data.ngrok.io/api/v1/{token}/telemetry"
        headers = {"Content-Type": "application/json"}

        print(f"🌐 Enviando datos a: {url} con el payload: {json.dumps(payload)}")

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            print(f"📡 Respuesta de ThingsBoard: {response.status_code} - {response.text}")
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de red: {e}")
            return False

    async def save_to_postgres(self, payload: dict, token: str, fuente_ip: str):
        """
        Guarda las lecturas validadas en la base de datos PostgreSQL.
        :param payload: Diccionario con las lecturas válidas.
        :param token: Token de autenticación del dispositivo.
        :param fuente_ip: Dirección IP de la fuente que envía la telemetría.
        """
        for sensor, valor in payload.items():
            query = """
                INSERT INTO lectura_sensor(sensor, valor, fuente_ip, token)
                VALUES (:sensor, :valor, :fuente_ip, :token)
            """
            values = {
                "sensor": sensor,
                "valor": valor,
                "fuente_ip": fuente_ip,
                "token": token
            }
            await database.execute(query=query, values=values)

        print("💾 Datos almacenados en PostgreSQL.")
