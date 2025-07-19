#!/usr/bin/env python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

# ✅ Clase personalizada para forzar OpenFlow 1.3
class OVSSwitch13(OVSSwitch):
    def __init__(self, *args, **kwargs):
        kwargs['protocols'] = 'OpenFlow13'
        super(OVSSwitch13, self).__init__(*args, **kwargs)

# 🧠 Topología extendida con nodo 'edge'
class TopologiaSDNUrbIA(Topo):
    def build(self):
        # Crear switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # Crear hosts
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')
        edge = self.addHost('edge', ip='10.0.0.100/24')

        # Conectar sensores y nodo edge
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(edge, s2)

        # Enlace entre switches
        self.addLink(s1, s2)

# 🚀 Función principal para lanzar la topología
def ejecutar_topologia():
    print("🧠 Iniciando topología SDN con nodo Edge simulado...")
    net = Mininet(
        topo=TopologiaSDNUrbIA(),
        controller=lambda name: RemoteController(name, ip='127.0.0.1', port=6633),
        switch=OVSSwitch13,
        autoSetMacs=True,
        autoStaticArp=True
    )

    net.start()
    print("✅ Topología iniciada. Puedes enviar datos desde h1 hacia edge.")
    CLI(net)
    net.stop()
    print("🛑 Topología detenida.")

if __name__ == '__main__':
    setLogLevel('info')
    ejecutar_topologia()
