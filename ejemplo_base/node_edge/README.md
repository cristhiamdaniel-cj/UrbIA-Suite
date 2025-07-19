#  🧠 Módulo `node_edge` – UrbIA Suite

Este módulo actúa como **nodo de borde (edge node)** en la arquitectura distribuida de UrbIA. Se encarga de:

- ✅ Recibir la telemetría enviada desde sensores (simulados o reales)
- 🧪 Validar y filtrar los datos fuera de rango
- 🌐 Reenviar datos válidos a la plataforma ThingsBoard
- 💾 Almacenar los datos en una base de datos PostgreSQL

---

## 📁 Estructura de archivos

```

node\_edge/
├── db.py              # Conexión a la base de datos PostgreSQL
├── fastapi\_app.py     # API FastAPI que recibe los datos
├── processor.py       # Lógica de validación, reenvío y almacenamiento
├── **init**.py
└── **pycache**/

````

---

## 🚀 Flujo de procesamiento

1. El sensor (por ejemplo, un script en C++) envía datos en formato JSON a este módulo.
2. `fastapi_app.py` recibe la petición POST vía `/telemetry/{token}`.
3. `processor.py`:
   - Filtra valores fuera del rango definido.
   - Reenvía los datos válidos a ThingsBoard.
   - Guarda los datos válidos en PostgreSQL.

---

## 🧪 Validación de datos

- Cada sensor tiene un **umbral máximo configurable** (por defecto: 1000.0).
- Si un valor es negativo o supera el umbral, se **omite del payload** antes del reenvío.
- Esto protege a la plataforma de valores erróneos o fuera de especificación.

---

## 🔐 Requisitos

- Base de datos PostgreSQL operativa con tabla `lectura_sensor`.
- Dispositivo previamente creado en ThingsBoard con su **token**.
- Variables de conexión correctamente configuradas en `db.py`.

---

## 🔧 Variables importantes

### `db.py`

```python
DATABASE_URL = "postgresql://postgres:Alejito10.@localhost/urbia"
````

> Cambiar si la base de datos se aloja fuera del contenedor o si el usuario cambia.

### URL de ThingsBoard en `processor.py`

```python
url = f"https://inti-data.ngrok.io/api/v1/{token}/telemetry"
```

> Esta URL debe apuntar al dominio donde esté expuesta tu instancia de ThingsBoard (puede ser un túnel Ngrok o dominio público).

---

## 🐳 Ejecución en Docker

Este módulo se ejecuta como un servicio Docker en el entorno de UrbIA. Para iniciar toda la infraestructura de la Fase 0 (incluyendo el nodo Edge), usa:

```bash
cd ejemplo_base
docker-compose up -d
```

Esto levantará:

* `simulador_cpp`: módulo de simulación que envía telemetría
* `node_edge`: este módulo que procesa y reenvía la telemetría
* `thingsboard`: servidor de monitoreo IoT

### Logs del servicio

```bash
docker-compose logs -f node_edge
```

---

## 📬 Ejemplo de solicitud

```bash
curl -X POST http://localhost:8028/telemetry/52uy6acbp55ydzkq98nw \
  -H "Content-Type: application/json" \
  -d '{
    "co2": 412.5,
    "temperatura": 23.1,
    "humedad": 58.2,
    "presion": 1012.8,
    "luz": 720.0,
    "ruido": 36.4
  }'
```
