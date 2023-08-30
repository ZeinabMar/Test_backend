import pytest
import logging
import json
from config import *
from Switch.bridge_funcs import bridge_config
from Switch.test_Bridge_group_conf import switch_config
from collections import namedtuple
# from pytest-check import check


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

Port_Stp = namedtuple('Port_Stp', ['index','stpIndex', 'stpIfStpAutoEdge','stpIfStpBpduFilter', 'stpIfStpBpduGuard',
                      'stpIfStpEdgePort', 'stpIfStpPortFast', 'stpIfStpRootGuard', 'result','shelfId', 'slotId', 'nodeId'])
Port_Stp.__new__.__defaults__ = (None, None, -1, "NO", "NO", -1, -1, -1, "Pass", 1, 1, None)
Port_Stp_DATA = (
    Port_Stp(1, None, -1, "ENABLE", "NO", 1, -1, -1, "Pass"),
    Port_Stp(2, None, -1, "NO", "DISABLE", 1, 1, 1, "Pass"),
    Port_Stp(3, None, 1, "DEFAULT", "DEFAULT", 1, 1, 1, "Pass"),
    Port_Stp(4, None, 1, 4, "DEFAULT", 1, 1, 1, "Fail"),
    Port_Stp(5, None, 1, "DISABLE", 4, 1, 1, 1, "Fail"),
    Port_Stp(6)
)

def Port_Stp_config(rest_interface_module, node_id, Port_Stp_data=Port_Stp(), method='POST'):
    data = Port_Stp_data._replace(nodeId=node_id)
    logger.info(f"TRY TO {method} Port_Stp CONFIG ...")

    if method == 'POST' or method == 'DELETE':  
        url = "/api/gponconfig/sp5100/portstpconfig/update"
        response = rest_interface_module.post_request(url, data._asdict()) 

    if data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in Port_Stp config {data._asdict}'
        if response.status_code != 200:
            logger.error(response.message)
        logger.info(f' GETTING Port_Stp-config (after {method} method) ... ')

        read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/portstpconfig/get/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.stpIndex}")
        input_data = json.loads(read_data.text)
        logger.info(f'data after read input_data {input_data}')
        #*********************************************************
        if method == 'POST':
            assert (input_data["stpIndex"]==data.stpIndex and
                    input_data["stpIfStpAutoEdge"] == data.stpIfStpAutoEdge and 
                    str(input_data["stpIfStpBpduFilter"]) == str(data.stpIfStpBpduFilter) and
                    str(input_data["stpIfStpBpduGuard"]) == str(data.stpIfStpBpduGuard) and
                    input_data["stpIfStpEdgePort"] == data.stpIfStpEdgePort and
                    input_data["stpIfStpPortFast"] == data.stpIfStpPortFast and
                    input_data["stpIfStpRootGuard"] == data.stpIfStpRootGuard),f'IN Everythig is ok Port_Stp config(after {method}'
            logger.info(f'every thing ok after Qos_Class config(after {method} ')

        else:  # method==DELETE
            assert (input_data["stpIndex"]==data.stpIndex and
                    input_data["stpIfStpAutoEdge"] == -1 and 
                    str(input_data["stpIfStpBpduFilter"]) == "NO" and
                    str(input_data["stpIfStpBpduGuard"]) == "NO" and
                    input_data["stpIfStpEdgePort"] == -1 and
                    input_data["stpIfStpPortFast"] == -1 and
                    input_data["stpIfStpRootGuard"] == -1),f'GET ERROR in Port_Stp config (after {method})'
    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in Port_Stp config {data._asdict}'


def test_Port_Stp_config(rest_interface_module, node_id):

    bridge_config(rest_interface_module, node_id, Bridge_conf(), method='POST')
    for port in range(9,25):  
        for switch in Switch_conf_Data: 
            if switch.index==4:
                switch_config(rest_interface_module, node_id, switch._replace(ethIfIndex=port), method='POST')
    
    for port in range(9,25):
        for stp in Port_Stp_DATA:
            if stp.index == 6:
                Port_Stp_config(rest_interface_module, node_id, stp._replace(stpIndex=port), method='DELETE')
            else:
                Port_Stp_config(rest_interface_module, node_id, stp._replace(stpIndex=port), method='POST')

    for port in range(9,25):  
        for switch in Switch_conf_Data: 
            if switch.index==9:
                switch_config(rest_interface_module, node_id, switch._replace(index=9,ethIfIndex=port), method='DELETE')
    bridge_config(rest_interface_module, node_id, Bridge_conf(), method='DELETE')






