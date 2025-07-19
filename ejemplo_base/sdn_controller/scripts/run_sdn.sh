# Script para iniciar controladores SDN con Ryu
#!/bin/bash

echo "🚀 Iniciando Ryu con los controladores..."
ryu-manager controllers/controlador_flujo.py controllers/encaminamiento_sdn.py controllers/sdn_monitor.py &
RYU_PID=$!

echo "🕒 Esperando que el controlador se estabilice..."
sleep 3

echo "🧠 Lanzando topología Mininet..."
sudo python3 topologias/topologia_sdn.py

echo "🛑 Deteniendo Ryu (PID=$RYU_PID)..."
kill $RYU_PID
