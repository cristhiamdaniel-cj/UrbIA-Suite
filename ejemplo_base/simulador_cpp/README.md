# 🛰️ Simulador C++ para Sensores Urbanos — UrbIA · Fase 0

Este módulo simula múltiples sensores ambientales en C++ y envía lecturas en tiempo real a un servidor ThingsBoard usando su API HTTP.

---

## 📚 Descripción

El propósito es replicar un entorno urbano sensorizado con datos artificiales para pruebas de dashboards y plataformas de visualización en **UrbIA**.

Cada sensor es una clase que hereda de `SensorBase`. Se generan valores aleatorios dentro de rangos realistas y se envían cada 5 segundos.

---

## 🌐 Requisitos

- C++17 (`g++`)
- `libcurl` instalado (`sudo apt install libcurl4-openssl-dev`)
- Sistema Linux/Unix
- Servidor ThingsBoard local o remoto corriendo en `http://localhost:8080`
- 📦 **Librería `nlohmann/json.hpp` (no incluida en el repositorio)**

---

## ⚠️ Dependencia Externa: `nlohmann/json.hpp`

Este archivo no se incluye en el repositorio (está en `.gitignore`).  
Antes de compilar, debes instalarlo manualmente así:

```bash
# Crear la carpeta si no existe
mkdir -p include/nlohmann

# Descargar el archivo desde el repositorio oficial
curl -o include/nlohmann/json.hpp https://raw.githubusercontent.com/nlohmann/json/develop/single_include/nlohmann/json.hpp
````

---

## 📁 Estructura del Proyecto

```
simulador_cpp/
├── include/         # Headers de sensores, cliente HTTP, logger, loader .env
│   ├── Sensor*.hpp
│   ├── HttpClient.hpp
│   ├── EnvLoader.hpp
│   ├── Logger.hpp
│   └── nlohmann/     # <--- DEBES CREAR ESTA CARPETA Y AÑADIR json.hpp
│       └── json.hpp
├── src/             # Implementaciones
│   ├── Sensor*.cpp
│   ├── HttpClient.cpp
│   ├── EnvLoader.cpp
│   └── Logger.cpp
├── logs/            # Log del simulador
│   └── simulador.log
├── build/           # Objetos compilados
├── sensor_simulator # Ejecutable
├── Makefile         # Script de compilación
└── .env             # Token del dispositivo
```

---

## 📦 Sensores Simulados

| Sensor      | Rango          | Unidad |
| ----------- | -------------- | ------ |
| CO₂         | 400 – 600      | ppm    |
| Temperatura | 20.0 – 35.0    | °C     |
| Humedad     | 40.0 – 80.0    | %      |
| Presión     | 990.0 – 1025.0 | hPa    |
| Luz         | 0 – 1000       | Lux    |
| Ruido       | 30.0 – 120.0   | dB     |

---

## 🛠️ Configuración

### 1. Crear `.env`

En la raíz del módulo (`simulador_cpp/`):

```env
THINGSBOARD_TOKEN=<<TU_TOKEN_AQUI>>
```

Este token debe corresponder al dispositivo registrado en ThingsBoard.

---

## 🚀 Compilar y Ejecutar

```bash
make clean && make run
```

Esto:

* Compila todo el código fuente
* Genera el binario `sensor_simulator`
* Inicia el envío de datos

---

## 🧾 Ejemplo de Payload JSON

```json
{
  "co2": 477.0,
  "temperatura": 34.33,
  "humedad": 65.97,
  "presion": 995.53,
  "luz": 675.29,
  "ruido": 50.27
}
```

Se envía vía `POST` a:

```
http://localhost:8080/api/v1/<TOKEN>/telemetry
```

---

## 🧩 Componentes Internos

* `SensorBase.hpp`: Clase abstracta base
* `Sensor*.hpp/cpp`: Implementaciones individuales
* `HttpClient`: Usa libcurl para enviar los datos
* `EnvLoader`: Carga variables de entorno desde `.env`
* `Logger`: Registra todos los eventos en `logs/simulador.log`

---

## 📈 Output

```bash
📡 Sensor: co2, Valor: 477.000000
📡 Sensor: temperatura, Valor: 34.330000
...
✅ Datos enviados correctamente.
```

```

---
