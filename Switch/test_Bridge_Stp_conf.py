import pytest
import logging
import json
from config import *
from Switch.bridge_funcs import bridge_config
from Switch.test_Bridge_group_conf import switch_config

# from pytest-check import check


pytestmark = [pytest.mark.env_name("OLT_env"), pytest.mark.rest_dev("nms")]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

Bridge_Stp = namedtuple('Bridge_Stp', ['index', "bridgeId", 'stpBridgeStp','stpBridgeStpBpduFilter', 'stpBridgeStpBpduGuard',
                      'stpBridgeStpErrDisableInterval', 'stpBridgeStpErrDisableState', 'stpBridgeStpPathCost', 'result','shelfId', 'slotId', 'nodeId'])
Bridge_Stp.__new__.__defaults__ = (None, 1, -1, -1, -1, -1, -1,"NO", "Pass", 1, 1, None)
Bridge_Stp_DATA = (
    Bridge_Stp(1, 1, 1, 1, 1, 1000, -1,"SHORT", "Pass"),
    Bridge_Stp(2, 1, 1, 1, -1, 1000, 1,"LONG", "Pass"),
    Bridge_Stp(3, 1, -1, -1, 1, 1000, -1,"SHORT", "Pass"),
    Bridge_Stp(4, 1, 1, 1, 1, 1000, -1,"SHORT", "Pass"),
    Bridge_Stp(5, 1, 1, 1, 1, 2, -1,"SHORT", "Fail"),
    Bridge_Stp(6, 1, 1, 1, 1, 1000, "NO", "SHORT", "Fail"),
    Bridge_Stp(7, 1, -1, -1, -1, -1, -1,"NO", "Pass")
)

def Bridge_Stp_config(rest_interface_module, node_id, Bridge_Stp_data=Bridge_Stp(), method='POST'):
    data = Bridge_Stp_data._replace(nodeId=node_id)
    logger.info(f"TRY TO {method} Bridge_Stp CONFIG ...")

    if method == 'POST' or method == 'DELETE':  
        url = "/api/gponconfig/sp5100/bridgestpconfig/update"
        response = rest_interface_module.post_request(url, data._asdict()) 

    if data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in Bridge_Stp config {data._asdict}'
        if response.status_code != 200:
            logger.error(response.message)
        logger.info(f' GETTING Bridge_Stp-config (after {method} method) ... ')

        read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/bridgestpconfig/get/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.bridgeId}")
        input_data = json.loads(read_data.text)
        logger.info(f'data after read input_data {input_data}')
        #*********************************************************
        if method == 'POST':
            assert (input_data["stpBridgeStp"] == data.stpBridgeStp and 
                    input_data["stpBridgeStpBpduFilter"] == data.stpBridgeStpBpduFilter and
                    input_data["stpBridgeStpBpduGuard"] == data.stpBridgeStpBpduGuard and
                    input_data["stpBridgeStpErrDisableInterval"] == data.stpBridgeStpErrDisableInterval and
                    input_data["stpBridgeStpErrDisableState"] == data.stpBridgeStpErrDisableState and
                    str(input_data["stpBridgeStpPathCost"]) == str(data.stpBridgeStpPathCost)),f'IN Everythig is ok Bridge_Stp config(after {method}'
            logger.info(f'every thing ok after Bridge_Stp config(after {method} ')

        else:  # method==DELETE
            assert (input_data["stpBridgeStp"] == -1 and 
                    input_data["stpBridgeStpBpduFilter"] == -1 and
                    input_data["stpBridgeStpBpduGuard"] == -1 and
                    input_data["stpBridgeStpErrDisableInterval"] == -1 and
                    input_data["stpBridgeStpErrDisableState"] == -1 and
                    str(input_data["stpBridgeStpPathCost"]) == "NO"),f'GET ERROR in Bridge_Stp config (after {method})'
    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in Bridge_Stp config {data._asdict}'


def test_Bridge_Stp_config(rest_interface_module, node_id):

    # bridge_config(rest_interface_module, node_id, Bridge_conf(), method='POST')

    for b_stp in Bridge_Stp_DATA:
        if b_stp.index == 7:
            Bridge_Stp_config(rest_interface_module, node_id, b_stp, method='DELETE')
        else:
            Bridge_Stp_config(rest_interface_module, node_id, b_stp, method='POST')

    # bridge_config(rest_interface_module, node_id, Bridge_conf(), method='DELETE')






