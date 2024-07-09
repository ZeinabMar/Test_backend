import pytest
import logging
import json
from conftest import *
from config import *
from Switch.bridge_funcs import bridge_config
from Switch.test_Bridge_group_conf import switch_config
from Switch.test_Bridge_Stp_conf import Bridge_Stp_config
from colorama import Fore
# from pytest-check import check


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

Bridge_Mstp_report = namedtuple('Bridge_Stp_report', ['stpIndex', "specMstpBridgeId", 'specMstpBridgePriority','specMstpBridgeUp', 'specMstpForwardDelay',
                      'specMstpHelloTime', 'specMstpLastTopologyChange', 'specMstpMaxAge', 'specMstpMaxHops', 'specMstpRegRootId', 'specMstpRootId',
                      'specMstpRootPathCost', 'specMstpRootPort', 'specMstpStpEnable', 'specMstpTopologyChangeCount', 'specMstpTransmitHoldCount','shelfId', 'slotId', 'nodeId'])
Bridge_Data = [
# Bridge_conf(1, 1, 'IEEE', 100, 30, 1, 6, priority=4096, result='Fail'),
# Bridge_conf(2, 1, 'IEEE_VLAN_BRIDGE', 1000, 29, 2, 7, priority=8192, result='Fail'),
Bridge_conf(3, 1, 'MSTP', 100, 30, maxAge=6, maxHops=1, priority=12288),
Bridge_conf(4, 1, 'MSTPRING', 1000, 29, maxAge=7, maxHops=20, priority=16384),
# Bridge_conf(5, 1, 'RPVSTP', 100, priority=20480),
# Bridge_conf(6, 1, 'RSTP', 1000, 29, 2, 7, priority=24576, result='Fail'),
# Bridge_conf(7, 1, 'RSTP_RING', 100, 30, 1, 6, priority=28672, result='Fail'),
# Bridge_conf(8, 1, 'RSTP_VLAN_BRIDGE', 1000, 29, 2, 7, priority=32768, result='Fail'),
# Bridge_conf(9, 1, 'RSTP_VLAN_BRIDGE_RING', 100, 30, 1, 6, priority=36864, result='Fail'),
Bridge_conf(10, 1, 'PROVIDER_MSTP', 1000, 29, maxAge=7, maxHops=35, priority=40960),
Bridge_conf(11, 1, 'PROVIDER_MSTP_EDGE', 100, 30, maxAge=6, maxHops=39, priority=45056),
# Bridge_conf(12, 1, 'PROVIDER_RSTP', 1000, 29, 2, 7, priority=49152, result='Fail'),
# Bridge_conf(13, 1, 'PROVIDER_RSTP_EDGE', 1000, 29, 2, 7, priority=53248 , result='Fail')
]

def Bridge_Mstp_report(rest_interface_module, node_id, Bridge_Mstp_rp=Bridge_conf(),stpIndex=1, method='POST', result="Pass"):
    data = Bridge_Mstp_rp._replace(nodeId=node_id)
    logger.info(f"{Fore.LIGHTGREEN_EX} ******** TRY TO {method} Bridge_Mstp_report CONFIG --> {data.index}...")

    if method == 'GET':  
        read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/bridgemstpstatereport/get/{data.nodeId}/{data.shelfId}/{data.slotId}/{stpIndex}")
        input_data = json.loads(read_data.text)
#*********************************************************
    if result == "Pass":
        assert read_data.status_code == 200, f'{method} ERROR in Bridge_Mstp config {data._asdict}'
        if read_data.status_code != 200:
            logger.error(read_data.message)
        logger.info(f'{Fore.LIGHTBLUE_EX}******* GETTING Bridge_Mstp_report (after {method} method) --> {data.index} ... ')
        assert (input_data["stpIndex"] == 1 and
                len(str(input_data["specMstpBridgeId"])) != 0 and 
                input_data["specMstpBridgePriority"] == data.priority and 
                input_data["specMstpHelloTime"] == data.helloTime and
                input_data["specMstpMaxAge"] == data.maxAge and
                input_data["specMstpMaxHops"] == data.maxHops and
                len(str(input_data["specMstpTopologyChangeCount"])) != 0 and
                len(str(input_data["specMstpRootId"])) != 0 and
                input_data["specMstpStpEnable"] == 1 and
                input_data["specMstpTransmitHoldCount"] != 0),f'IN Everythig is ok Bridge_Mstp config(after {method}'
        logger.info(f'every thing ok after Bridge_Mstp config(after {method} ')

    else:
        assert read_data.status_code in range(400, 505), f'{method} SET INCORRECT DATA in Bridge_Mstp config {data._asdict}'
        # assert (input_data["stpIndex"] == 1 and
        #         # len(str(input_data["specStpBridgeId"])) != 0 and 
        #         input_data["specMstpBridgePriority"] == data.priority and 
        #         input_data["specMstpHelloTime"] == data.helloTime and
        #         input_data["specMstpMaxAge"] == data.maxAge and
        #         input_data["specMstpMaxHops"] == data.maxHops and
        #         len(str(input_data["specMstpTopologyChangeCount"])) != 0 and
        #         len(str(input_data["specMstpRootId"])) != 0 and
        #         input_data["specMstpStpEnable"] == 1 and
        #         input_data["stpBridgeStpErrDisableState"] == data.stpBridgeStpErrDisableState and
        #         str(input_data["stpBridgeStpPathCost"]) == str(data.stpBridgeStpPathCost)),f'IN Everythig is ok Bridge_Mstp config(after {method}'
        # logger.info(f'every thing ok after Bridge_Mstp config(after {method} ')


def test_Bridge_Mstp_report(rest_interface_module, node_id):
    for bridge in Bridge_Data:
        response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgeconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
        bridge_config(rest_interface_module, node_id, bridge, method='POST')
        # if bridge.bridgeProtocol == ("RPVSTP" or "RSTP" or "IEEE_VLAN_BRIDGE" or "IEEE" or "RSTP_RING" or "RSTP_VLAN_BRIDGE" or "RSTP_VLAN_BRIDGE_RING" or "PROVIDER_RSTP" or "PROVIDER_RSTP_EDGE"):
        #     Bridge_Mstp_report(rest_interface_module, node_id, bridge, 1, method='GET', result="Fail")
        # else:
        Bridge_Mstp_report(rest_interface_module, node_id, bridge, 1, method='GET', result="Pass")
        bridge_config(rest_interface_module, node_id, bridge, method='DELETE')





