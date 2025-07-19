#!/bin/bash
echo "🌐 Iniciando API de monitoreo en el puerto 8028..."
nohup PYTHONPATH=. python3 controllers/monitor_api.py > logs/api.log 2>&1 &
echo "✅ API corriendo en segundo plano. Verifica en http://<IP>:8028"
