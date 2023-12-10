import pytest
import logging
import json
from conftest import *
from config import *
from Switch.bridge_funcs import bridge_config
from Switch.test_Bridge_group_conf import switch_config
from collections import namedtuple
# from pytest-check import check


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

Port_L2 = namedtuple('Port_L2', ['index', "ethIfIndex", 'ethIfTxStatus','phyIfState', 'phyIfSpeed',
                                 'phyIfMtu', 'phyIfFlowControl', 'phyIfLoopback', 'phyIfDuplex', 
                                 'phyIfDesc', 'result', 'shelfId', 'slotId', 'nodeId'])
Port_L2.__new__.__defaults__ = (None, None, 1, -1, "10G", 1500, "NO", -1, "FULL", "", "Pass", 1, 1, None)
Port_L2_DATA = (
    Port_L2(1, None, 1, -1, "100G", 1500, "NO", None, "FULL", "", "Fail", 1, 1, None),#S100G is over
    Port_L2(2, None, 1, -1, "1G", 1500, "BOTH", None, "FULL", "", "Pass", 1, 1, None),
    Port_L2(3, None, 1, -1, "10G", 3000, "RX", None, "FULL", "", "Pass", 1, 1, None),
    Port_L2(4, None, 1, 1, "1G", 3000, "TX", None, "FULL", "", "Pass", 1, 1, None),
    Port_L2(5, None, 1, 1, None, 3000, "NO", None, "FULL", "", "Fail", 1, 1, None),
    Port_L2(6, None, 1, 1, "1G", None, "NO", None, "FULL", "", "Fail", 1, 1, None),
    Port_L2(7,None)
)

def Port_L2_config(rest_interface_module, node_id, Port_L2_data=Port_L2(), method='POST'):
    data = Port_L2_data._replace(nodeId=node_id)
    logger.info(f"TRY TO {method} Port_L2 CONFIG ...")

    if method == 'POST' or method == 'DELETE':  
        url = "/api/gponconfig/sp5100/portl2/update"
        response = rest_interface_module.post_request(url, data._asdict()) 

    if data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in Port_L2 config {data._asdict}'
        if response.status_code != 200:
            logger.error(response.message)
        logger.info(f' GETTING Port_L2-config (after {method} method) ... ')
        read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/portl2/get/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.ethIfIndex}")
        input_data = json.loads(read_data.text)
        logger.info(f'data after read input_data {input_data}')
        #*********************************************************
        if method == 'POST':
            assert (input_data["ethIfIndex"] == data.ethIfIndex and 
                    input_data["ethIfTxStatus"] == 1 and
                    input_data["phyIfState"] == data.phyIfState and
                    str(input_data["phyIfSpeed"]) == str(data.phyIfSpeed) and
                    input_data["phyIfMtu"] == data.phyIfMtu and
                    str(input_data["phyIfFlowControl"]) == str(data.phyIfFlowControl) and
                    input_data["phyIfLoopback"] == data.phyIfLoopback and
                    input_data["phyIfDuplex"] == data.phyIfDuplex),f'IN Everythig is ok Port_L2 config(after {method}'
            logger.info(f'every thing ok after Port_L2 config(after {method}')
        else:  # method==DELETE
            assert (input_data["ethIfIndex"] == data.ethIfIndex and 
                    input_data["ethIfTxStatus"] == 1 and
                    input_data["phyIfState"] == -1 and
                    str(input_data["phyIfSpeed"]) == "10G" and
                    input_data["phyIfMtu"] == 1500 and
                    input_data["phyIfFlowControl"] == "NO" and
                    input_data["phyIfLoopback"] == None and
                    str(input_data["phyIfDuplex"]) == "FULL"),f'GET ERROR in Port_L2 config (after {method})'
    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in Port_L2 config {data._asdict}'


def test_Port_L2_config(rest_interface_module, node_id):
    for port in range(1,3):
        for l2 in Port_L2_DATA:
            response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/portl2/getall?nodeId=31&shelfId=1&slotId=1")
            if l2.index != 7:
                Port_L2_config(rest_interface_module, node_id, l2._replace(ethIfIndex=port), method='POST')
    response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/portl2/getall?nodeId=31&shelfId=1&slotId=1")
    for port in range(1,3):
            Port_L2_config(rest_interface_module, node_id, Port_L2_DATA[6]._replace(ethIfIndex=port), method='DELETE')







