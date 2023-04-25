import pytest
import logging
import json
from config import *
from test_switch.bridge_funcs import bridge_config
from test_switch.test_Bridge_group_conf import switch_config
from test_switch.test_Bridge_Stp_conf import Bridge_Stp_config

# from pytest-check import check


pytestmark = [pytest.mark.env_name("OLT_env"), pytest.mark.rest_dev("nms")]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

Port_Mstp_report = namedtuple('Port_Stp_report', ['ifIndex', 'stpIndex', "specMstpInstanceInterfaceConfiguredCSTExternalPathCost", 'specMstpInstanceInterfaceConfiguredInternalPathCost',
                              'specMstpInstanceInterfaceCSTPriority', 'specMstpInstanceInterfaceDesignatedBridge', 'specMstpInstanceInterfaceDesignatedInternalPathCost',
                              'specMstpInstanceInterfaceDesignatedPortId', 'specMstpInstanceInterfaceDesignatedRoot', 'specMstpInstanceInterfaceForwardDelay',
                              'specMstpInstanceInterfaceForwardTimer', 'specMstpInstanceInterfaceHelloTime', 'specMstpInstanceInterfaceHelloTimer', 'specMstpInstanceInterfaceIfIndex',
                              'specMstpInstanceInterfaceMessageAge', 'specMstpInstanceInterfaceMessageAgeTimer', 'specMstpInstanceInterfacePortId', 'specMstpInstanceInterfacePortNumber',
                              'specMstpInstanceInterfaceRole', 'specMstpInstanceInterfaceState', 'specMstpInstanceInterfaceMSTIPriority','shelfId', 'slotId', 'nodeId'])
Bridge_Data = [
Bridge_conf(1, 'IEEE', 100, 30, 1, 6, priority=4096 ,result="Fail"),
Bridge_conf(1, 'IEEE_VLAN_BRIDGE', 1000, 29, 2, 7, priority=8192, result="Fail"),
Bridge_conf(1, 'MSTP', 100, 30, maxAge=6, maxHops=1, priority=12288),
Bridge_conf(1, 'MSTPRING', 1000, 29, maxAge=7, maxHops=20, priority=16384),
Bridge_conf(1, 'RPVSTP', 100, priority=20480, result="Fail"),
Bridge_conf(1, 'RSTP', 1000, 29, 2, 7, priority=24576, result="Fail"),
Bridge_conf(1, 'RSTP_RING', 100, 30, 1, 6, priority=28672, result="Fail"),
Bridge_conf(1, 'RSTP_VLAN_BRIDGE', 1000, 29, 2, 7, priority=32768, result="Fail"),
Bridge_conf(1, 'RSTP_VLAN_BRIDGE_RING', 100, 30, 1, 6, priority=36864, result="Fail"),
Bridge_conf(1, 'PROVIDER_MSTP', 1000, 29, maxAge=7, maxHops=35, priority=40960),
Bridge_conf(1, 'PROVIDER_MSTP_EDGE', 100, 30, maxAge=6, maxHops=39, priority=45056),
Bridge_conf(1, 'PROVIDER_RSTP', 1000, 29, 2, 7, priority=49152, result="Fail"),
Bridge_conf(1, 'PROVIDER_RSTP_EDGE', 1000, 29, 2, 7, priority=53248, result="Fail")]

def Port_Mstp_report(rest_interface_module, node_id, Port_Mstp_rp=Bridge_conf(),stpIndex=1, method='POST'):
    data = Port_Mstp_rp._replace(nodeId=node_id)
    logger.info(f"TRY TO {method} Port_Mstp_report CONFIG ...")

    if method == 'GET':  
        read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/interfacemstpstatereport/get/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.ifIndex}/{stpIndex}")
        input_data = json.loads(read_data.text)

        assert read_data.status_code == 200, f'{method} ERROR in Port_Mstp config {data._asdict}'
        if read_data.status_code != 200:
            logger.error(read_data.message)
        logger.info(f' GETTING Port_Mstp_report (after {method} method) ... ')

                #*********************************************************
        if method == 'GET':
            if data.bridgeProtocol == "MSTP" or "MSTP_RING" or "PROVIDER_MSTP" or "PROVIDER_MSTP_EDGE":
                assert (input_data["stpIndex"] == 1 and
                        # len(str(input_data["specStpBridgeId"])) != 0 and 
                        input_data["specMstpBridgePriority"] == data.priority and 
                        input_data["specMstpHelloTime"] == data.helloTime and
                        input_data["specMstpMaxAge"] == data.maxAge and
                        input_data["specMstpMaxHops"] == data.maxHops and
                        len(str(input_data["specMstpTopologyChangeCount"])) != 0 and
                        len(str(input_data["specMstpRootId"])) != 0 and
                        input_data["specMstpStpEnable"] == 1 and
                        input_data["stpBridgeStpErrDisableState"] == data.stpBridgeStpErrDisableState and
                        str(input_data["stpBridgeStpPathCost"]) == str(data.stpBridgeStpPathCost)),f'IN Everythig is ok Bridge_Mstp config(after {method}'
                logger.info(f'every thing ok after Bridge_Mstp config(after {method} ')

            else:
                assert (input_data["stpIndex"] == 1 and
                        # len(str(input_data["specStpBridgeId"])) != 0 and 
                        input_data["specMstpBridgePriority"] == data.priority and 
                        input_data["specMstpHelloTime"] == data.helloTime and
                        input_data["specMstpMaxAge"] == data.maxAge and
                        input_data["specMstpMaxHops"] == data.maxHops and
                        len(str(input_data["specMstpTopologyChangeCount"])) != 0 and
                        len(str(input_data["specMstpRootId"])) != 0 and
                        input_data["specMstpStpEnable"] == 1 and
                        input_data["stpBridgeStpErrDisableState"] == data.stpBridgeStpErrDisableState and
                        str(input_data["stpBridgeStpPathCost"]) == str(data.stpBridgeStpPathCost)),f'IN Everythig is ok Bridge_Mstp config(after {method}'
                logger.info(f'every thing ok after Bridge_Mstp config(after {method} ')


def test_Bridge_Stp_report(rest_interface_module, node_id):
    def mstp():
        for port in range(1,25):
            switch_config(rest_interface_module, node_id, Switch_conf._replace(ethIfIndex=port,index=4), method='POST')
        Bridge_Mstp_config(rest_interface_module, node_id, Bridge_Mstp_conf(2, 1, None, None, f"{vlan.vlanId}", "Pass", 1, 1, None))
        Bridge_Stp_report(rest_interface_module, node_id, bridge, 1, method='GET')
        Bridge_Mstp_config(rest_interface_module, node_id, Bridge_Mstp_conf(2, 1, f"{vlan.vlanId}", f"{vlan.vlanId}", "", "Pass", 1, 1, None))
        for port in range(1,25):
            switch_config(rest_interface_module, node_id, Switch_conf._replace(ethIfIndex=port,index=9), method='POST')    

    for bridge in Bridge_Data:
        bridge_config(rest_interface_module, node_id, bridge, method='POST')
        if bridge.bridgeProtocol == 'PROVIDER_MSTP'or 'PROVIDER_RSTP':
            for vlan in VLAN_DATA_conf_service:
                vlan_config(rest_interface_module, node_id, vlan, method='POST') 
                mstp()
                vlan_config(rest_interface_module, node_id, vlan, method='DELETE')
        else:
            for vlan in VLAN_DATA_conf_service:
                vlan_config(rest_interface_module, node_id, vlan, method='POST')  
                mstp()
                vlan_config(rest_interface_module, node_id, vlan, method='DELETE')

            for vlan in VLAN_DATA_conf_CUSTOM:
                vlan_config(rest_interface_module, node_id, vlan, method='POST')   
                mstp()
                vlan_config(rest_interface_module, node_id, vlan, method='DELETE')
       
        bridge_config(rest_interface_module, node_id, bridge, method='DELETE')





