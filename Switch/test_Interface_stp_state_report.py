import pytest
import logging
import json
from conftest import *
from config import *
from Switch.bridge_funcs import bridge_config
from Switch.test_Bridge_group_conf import switch_config
from Switch.test_Bridge_Stp_conf import Bridge_Stp_config
from Switch.test_Port_Stp_conf import Port_Stp_config

# from pytest-check import check


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

interface_Stp = namedtuple('interface_Stp', ["ifIndex", "specStpInterfaceIfIndex", "specStpInterfacePortNumber", 
                               'specStpInterfaceDesignatedPortId', 'shelfId', 'slotId', 'nodeId'])
interface_Stp.__new__.__defaults__ = (0, 0, 0, "", 1, 1, 17)
Bridge_Data = [
Bridge_conf(1, 'IEEE', 100, 30, 1, 6, priority=4096),
Bridge_conf(1, 'IEEE_VLAN_BRIDGE', 1000, 29, 2, 7, priority=8192),
# Bridge_conf(1, 'MSTP', 100, 30, maxAge=6, maxHops=1, priority=12288),
# Bridge_conf(1, 'MSTPRING', 1000, 29, maxAge=7, maxHops=20, priority=16384),
Bridge_conf(1, 'RPVSTP', 100, priority=20480),
Bridge_conf(1, 'RSTP', 1000, 29, 2, 7, priority=24576),
Bridge_conf(1, 'RSTP_RING', 100, 30, 1, 6, priority=28672),
Bridge_conf(1, 'RSTP_VLAN_BRIDGE', 1000, 29, 2, 7, priority=32768),
Bridge_conf(1, 'RSTP_VLAN_BRIDGE_RING', 100, 30, 1, 6, priority=36864),
# Bridge_conf(1, 'PROVIDER_MSTP', 1000, 29, maxAge=7, maxHops=35, priority=40960),
# Bridge_conf(1, 'PROVIDER_MSTP_EDGE', 100, 30, maxAge=6, maxHops=39, priority=45056),
Bridge_conf(1, 'PROVIDER_RSTP', 1000, 29, 2, 7, priority=49152),
Bridge_conf(1, 'PROVIDER_RSTP_EDGE', 1000, 29, 2, 7, priority=53248)]

def interface_Stp_report(rest_interface_module, node_id, interface_Stp=interface_Stp(), port=None, method='POST', result="Pass"):
    data = interface_Stp._replace(ifIndex=port, nodeId=node_id)
    logger.info(f"TRY TO {method} interface_Stp_report CONFIG ...")

    if method == 'GET':  
        read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/interfacestpstatereport/get/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.ifIndex}")
        input_data = json.loads(read_data.text)
        assert read_data.status_code == 200, f'{method} ERROR in interface_Stp config {data._asdict}'
        if read_data.status_code != 200:
            logger.error(read_data.message)
        logger.info(f' GETTING interface_Stp_report (after {method} method) ... ')
        #*********************************************************
        if result == "Pass":
            assert read_data.status_code == 200, f'{method} ERROR in interface_Stp config {data._asdict}'
            if read_data.status_code != 200:
                logger.error(read_data.message)
            logger.info(f' GETTING interface_Stp_report (after {method} method) ... ')
            
            assert (input_data["ifIndex"] == data.ifIndex and
                    input_data["specStpInterfaceIfIndex"] != 0 and
                    len(str(input_data["specStpInterfaceDesignatedPortId"])) != 0 and 
                    input_data['specStpInterfacePortNumber'] != 0),f'IN Everythig is ok interface_Stp config(after {method}'
            logger.info(f'every thing ok after nterfaace_Stp config(after {method} ')

        elif result == "Fail":
            assert read_data.status_code in range(400, 505), f'{method} SET INCORRECT DATA in interface_Stp_report config {data._asdict}'


def test_interface_Stp_report(rest_interface_module, node_id):

    for bridge in Bridge_Data:
        response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgeconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
        bridge_config(rest_interface_module, node_id, bridge, method='POST')

        for port in range(1,2):
            response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgegroupconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
            switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port, index=4), method='POST')
        
        for port in range(1,2):
            response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/portstpconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
            Port_Stp_config(rest_interface_module, node_id, Port_Stp_conf(port,1,"ENABLE","ENABLE",-1,1,-1), method='POST')
            interface_Stp_report(rest_interface_module, node_id, interface_Stp(), port=port, method='GET')
            Port_Stp_config(rest_interface_module, node_id, Port_Stp_conf(port), method='DELETE')

        for port in range(1,2):  
            response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgegroupconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
            switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port, index=9), method='DELETE')

        response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgeconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
        bridge_config(rest_interface_module, node_id, bridge, method='DELETE')
        
                



        






