#!/bin/bash

# Script para lanzar el laboratorio SDN de UrbIA
# Autor: Daniel C. / Proyecto Doctoral UrbIA

echo "🧹 Limpiando entorno Mininet..."
sudo mn -c

echo "🟢 Activando entorno virtual..."
source .venv/bin/activate

echo "🚀 Lanzando controlador Ryu con 3 apps..."
cd sdn_controller
PYTHONPATH=. ryu-manager controllers/controlador_flujo.py \
                   controllers/encaminamiento_sdn.py \
                   controllers/sdn_monitor.py &
RYU_PID=$!

sleep 4
echo "🌐 API de monitoreo disponible en http://localhost:8028"

echo "🧠 Abriendo nueva terminal para lanzar topología SDN personalizada..."
gnome-terminal -- bash -c "cd ~/UrbIA/ejemplo_base/sdn_controller/topologias && sudo python3 topologia_sdn.py; exec bash"

echo ""
echo "✅ Todo listo. Controlador SDN y topología activos."
echo "📊 Monitoreo en tiempo real desde tu navegador en http://localhost:8028"
echo "🛑 Para cerrar, finaliza el proceso Ryu con: kill $RYU_PID"
