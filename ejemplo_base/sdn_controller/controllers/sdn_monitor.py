# controllers/sdn_monitor.py

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER, DEAD_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.topology import event
from ryu.lib import hub

from threading import Thread
import monitor_api  # ✅ Import necesario para exponer la API externa

class SDNMonitor(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SDNMonitor, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.stats_switches = {}  # Dict para estadísticas de flujo por switch
        self.stats_puertos = {}   # Dict para estadísticas de puertos por switch

        # Lanzar hilo de monitoreo continuo
        self.monitor_thread = hub.spawn(self._monitor)

        # 👇 Lanzar hilo adicional para exponer la API externa (FastAPI)
        self.logger.info("🌐 Lanzando API de monitoreo en http://0.0.0.0:8028 ...")
        Thread(target=monitor_api.lanzar_api, args=(self,), daemon=True).start()

    @set_ev_cls(event.EventSwitchEnter)
    def switch_enter_handler(self, ev):
        dp = ev.switch.dp
        self.logger.info("✅ Switch conectado con DPID %s", dp.id)

    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.info("Registrando datapath: %016x", datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.info("Eliminando datapath: %016x", datapath.id)
                del self.datapaths[datapath.id]

    def _monitor(self):
        while True:
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(10)

    def _request_stats(self, datapath):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        req_flow = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req_flow)

        req_port = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req_port)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):
        body = ev.msg.body
        dpid = ev.msg.datapath.id
        self.logger.info("📊 Estadísticas de flujo para switch %s", dpid)

        flow_stats = []
        for stat in sorted(body, key=lambda x: x.priority):
            stat_data = {
                "tabla": stat.table_id,
                "prioridad": stat.priority,
                "in_port": stat.match.get('in_port'),
                "eth_type": stat.match.get('eth_type'),
                "ipv4_src": stat.match.get('ipv4_src'),
                "ipv4_dst": stat.match.get('ipv4_dst'),
                "paquetes": stat.packet_count,
                "bytes": stat.byte_count
            }
            flow_stats.append(stat_data)

            self.logger.info(
                "Tabla %s  Prioridad %s  In_Port %s  Eth_Type %s  IPv4_src %s  IPv4_dst %s → Paquetes: %d  Bytes: %d",
                stat_data["tabla"], stat_data["prioridad"], stat_data["in_port"],
                stat_data["eth_type"], stat_data["ipv4_src"], stat_data["ipv4_dst"],
                stat_data["paquetes"], stat_data["bytes"]
            )

        self.stats_switches[dpid] = flow_stats

    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def _port_stats_reply_handler(self, ev):
        body = ev.msg.body
        dpid = ev.msg.datapath.id
        self.logger.info("📊 Estadísticas de puertos para switch %s", dpid)

        port_stats = []
        for stat in body:
            stat_data = {
                "puerto": stat.port_no,
                "rx_bytes": stat.rx_bytes,
                "rx_paquetes": stat.rx_packets,
                "tx_bytes": stat.tx_bytes,
                "tx_paquetes": stat.tx_packets,
                "errores_tx": stat.tx_errors
            }
            port_stats.append(stat_data)

            self.logger.info(
                "Puerto %d: RX %d bytes (%d paquetes), TX %d bytes (%d paquetes), errores TX %d",
                stat.port_no,
                stat.rx_bytes, stat.rx_packets,
                stat.tx_bytes, stat.tx_packets,
                stat.tx_errors
            )

        self.stats_puertos[dpid] = port_stats
