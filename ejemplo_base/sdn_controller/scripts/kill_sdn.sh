# Script para detener procesos de Ryu activos
#!/bin/bash

echo "🧼 Limpiando Mininet..."
sudo mn -c

echo "🛑 Terminando procesos de Ryu..."
pkill -f "ryu-manager"
