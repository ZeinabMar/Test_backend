import pytest
import logging
import json
from config import *
from Switch.bridge_funcs import bridge_config
from Switch.test_Bridge_group_conf import switch_config
from Switch.test_Bridge_Stp_conf import Bridge_Stp_config

# from pytest-check import check


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

Bridge_Stp_report = namedtuple('Bridge_Stp_report', ['stpIndex', "specStpBridgeId", 'specStpBridgePriority','specStpBridgeUp', 'specStpForwardDelay',
                      'specStpHelloTime', 'specStpLastTopologyChange', 'specStpMaxAge', 'specStpRootId', 'specStpRootPathCost',
                      'specStpRootPort', 'specStpStpEnable', 'specStpTopologyChangeCount', 'specStpTransmitHoldCount','shelfId', 'slotId', 'nodeId'])
Bridge_Data_report = [
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
Bridge_conf(1, 'PROVIDER_RSTP_EDGE', 1000, 29, 2, 7, priority=53248)
]

def Bridge_Stp_report(rest_interface_module, node_id, Bridge_Stp_rp=Bridge_conf(),stpIndex=1, method='POST', result="Pass"):
    data = Bridge_Stp_rp._replace(nodeId=node_id)
    logger.info(f"TRY TO {method} Bridge_Stp_report CONFIG ...")

    if method == 'GET':  
        read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/bridgestpstatereport/get/{data.nodeId}/{data.shelfId}/{data.slotId}/{stpIndex}")
        input_data = json.loads(read_data.text)
    #*********************************************************
    if result == "Pass":
        assert read_data.status_code == 200, f'{method} ERROR in Bridge_Stp config {data._asdict}'
        if read_data.status_code != 200:
            logger.error(read_data.message)
        logger.info(f' GETTING Bridge_Stp_report (after {method} method) ... ')
        
        assert (input_data["stpIndex"] == 1 and
                len(str(input_data["specStpBridgeId"])) != 0 and 
                # input_data["specStpBridgePriority"] == data.priority and
                input_data['specStpForwardDelay'] == data.forwardTime and
                input_data["specStpHelloTime"] == data.helloTime and
                input_data["specStpMaxAge"] == data.maxAge and
                len(str(input_data["specStpLastTopologyChange"])) != 0 and
                len(str(input_data["specStpRootId"])) != 0 and
                input_data["specStpStpEnable"] == 1 ),f'IN Everythig is ok Bridge_Stp config(after {method}'
        logger.info(f'every thing ok after Bridge_Stp config(after {method} ')

    elif result == "Fail":
        assert read_data.status_code in range(400, 505), f'{method} SET INCORRECT DATA in Bridge_Stp_report config {data._asdict}'
        # assert (len(str(input_data["specStpBridgeId"])) == 0 and 
        #         input_data["specStpBridgePriority"] == 0 and
        #         input_data["specStpBridgeUp"] == 0 and
        #         input_data["specStpForwardDelay"] == 0 and
        #         input_data["specStpHelloTime"] == 0 and
        #         len(str(input_data["specStpLastTopologyChange"])) == 0 and
        #         input_data["specStpMaxAge"] == 0 and 
        #         len(str(input_data["specStpRootId"])) == 0 and 
        #         input_data["specStpRootPathCost"] == 0 and 
        #         len(str(input_data["specStpRootPort"])) == 0 and 
        #         input_data["specStpStpEnable"] == 0 and
        #         input_data["specStpTopologyChangeCount"] == 0 and
        #         input_data["specStpTransmitHoldCount"] == 0),f'IN Everythig is ok Bridge_Stp config(after {method}'                        
        # logger.info(f'every thing ok after Bridge_Stp config(after {method} ')


def test_Bridge_Stp_report(rest_interface_module, node_id):
    for bridge in Bridge_Data_report:
        bridge_config(rest_interface_module, node_id, bridge, method='POST')
        logger.info(f"bridgeee {bridge.bridgeProtocol}")
        # if bridge.bridgeProtocol == "MSTPRING" or "MSTP" or "PROVIDER_MSTP" or "PROVIDER_MSTP_EDGE":
        #     Bridge_Stp_report(rest_interface_module, node_id, bridge, 1, method='GET', result="Fail")
        # if bridge.bridgeProtocol == "IEEE" or "IEEE_VLAN_BRIDGE" or "RPVSTP" or "RSTP_RING" or "RSTP" or "RSTP_VLAN_BRIDGE" or "RSTP_VLAN_BRIDGE_RING" or "PROVIDER_RSTP" or "PROVIDER_RSTP_EDGE":    
        Bridge_Stp_report(rest_interface_module, node_id, bridge, 1, method='GET', result="Pass")
        bridge_config(rest_interface_module, node_id, bridge, method='DELETE')







