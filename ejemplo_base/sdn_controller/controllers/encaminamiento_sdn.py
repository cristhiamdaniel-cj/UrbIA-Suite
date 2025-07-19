# controllers/encaminamiento_sdn.py

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ipv4
from ryu.lib.packet import ether_types


class EncaminamientoSDN(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(EncaminamientoSDN, self).__init__(*args, **kwargs)
        self.ip_to_port = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        """
        Regla por defecto para enviar paquetes desconocidos al controlador.
        """
        datapath = ev.msg.datapath
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto

        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

        self.logger.info("Switch conectado con DPID %s", datapath.id)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        """
        Instala una nueva regla en la tabla de flujo del switch.
        """
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]

        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        """
        Aprende direcciones IP de origen y decide a qué puerto reenviar.
        """
        msg = ev.msg
        datapath = msg.datapath
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth_pkt = pkt.get_protocol(ethernet.ethernet)

        if eth_pkt.ethertype != ether_types.ETH_TYPE_IP:
            return  # Ignora tramas no IP

        ip_pkt = pkt.get_protocol(ipv4.ipv4)
        src_ip = ip_pkt.src
        dst_ip = ip_pkt.dst

        dpid = datapath.id
        self.ip_to_port.setdefault(dpid, {})

        self.logger.info("Switch %s recibió paquete: %s ➜ %s (in_port=%s)", dpid, src_ip, dst_ip, in_port)

        # Aprende la IP de origen
        self.ip_to_port[dpid][src_ip] = in_port

        # Decide puerto de salida
        if dst_ip in self.ip_to_port[dpid]:
            out_port = self.ip_to_port[dpid][dst_ip]
        else:
            out_port = ofproto.OFPP_FLOOD  # Si no conoce la IP de destino, hace flooding

        actions = [parser.OFPActionOutput(out_port)]

        # Instala flujo si no hay flooding
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_IP,
                                    ipv4_src=src_ip,
                                    ipv4_dst=dst_ip,
                                    in_port=in_port)
            self.add_flow(datapath, 10, match, actions)

        # Envía el paquete manualmente
        out = parser.OFPPacketOut(datapath=datapath,
                                  buffer_id=ofproto.OFP_NO_BUFFER,
                                  in_port=in_port,
                                  actions=actions,
                                  data=msg.data)
        datapath.send_msg(out)
