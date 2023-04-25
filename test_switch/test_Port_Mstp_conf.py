import pytest
import logging
import json
from config import *
from test_switch.test_vlan import vlan_config
from test_switch.bridge_funcs import bridge_config
from test_switch.test_Bridge_group_conf import switch_config
from test_switch.test_Bridge_Mstp_instance_conf import Bridge_Mstp_config
# from pytest-check import check


pytestmark = [pytest.mark.env_name("OLT_env"), pytest.mark.rest_dev("nms")]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

Port_Mstp = namedtuple('Port_Mstp', ['ifIndex', 'instanceIfIndex','mstpInstanceIfPathCost', 
                       'mstpInstanceIfPriority', 'result','shelfId', 'slotId', 'nodeId'])
Port_Mstp.__new__.__defaults__ = (None, None, None, 0, 0, "Pass", 1, 1, None)
# Port_Mstp_DATA = (
#     Port_Mstp(1, None, 5, "ENABLE", "NO", 1, -1, -1, "Pass"),
# )

def Port_Mstp_config(rest_interface_module, node_id, Port_Mstp_data=Port_Mstp(), method='POST'):
    data = Port_Mstp_data._replace(nodeId=node_id)
    logger.info(f"TRY TO {method} Port_Mstp CONFIG ...")

    if method == 'add':
        url = "/api/gponconfig/sp5100/portmstpconfig/add"
        response = rest_interface_module.post_request(url, data._asdict()) 
    elif method == 'POST':  
        url = "/api/gponconfig/sp5100/portmstpconfig/update"
        response = rest_interface_module.post_request(url, data._asdict()) 
    else:  # method==DELETE
        url = f"/api/gponconfig/sp5100/portmstpconfig/delete/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.ifIndex}/{data.instanceIfIndex}"
        response = rest_interface_module.delete_request(url)


    if data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in Port_Stp config {data._asdict}'
        if response.status_code != 200:
            logger.error(response.message)
        logger.info(f' GETTING Port_Stp-config (after {method} method) ... ')

        read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/portmstpconfig/get/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.ifIndex}/{data.instanceIfIndex}")
        input_data = json.loads(read_data.text)
        logger.info(f'data after read input_data {input_data}')
        #*********************************************************
        if method == 'add':
            assert (input_data["ifIndex"]==data.ifIndex and
                    input_data["instanceIfIndex"] == data.instanceIfIndex and 
                    str(input_data["mstpInstanceIfPathCost"]) == str(data.mstpInstanceIfPathCost) and
                    str(input_data["mstpInstanceIfPriority"]) == str(data.mstpInstanceIfPriority)),f'IN Everythig is ok Port_Mstp config(after {method}'
            logger.info(f'every thing ok after Port_Mstp config(after {method} ')

        elif method == 'POST':
            assert (input_data["ifIndex"]==data.ifIndex and
                    input_data["instanceIfIndex"] == data.instanceIfIndex and 
                    str(input_data["mstpInstanceIfPathCost"]) == str(data.mstpInstanceIfPathCost) and
                    str(input_data["mstpInstanceIfPriority"]) == str(data.mstpInstanceIfPriority)),f'IN Everythig is ok Port_Mstp config(after {method}'
            logger.info(f'every thing ok after Port_Mstp config(after {method} ')

        else:  # method==DELETE
            assert (input_data["ifIndex"]==data.ifIndex and
                    input_data["instanceIfIndex"] == data.instanceIfIndex and 
                    str(input_data["mstpInstanceIfPathCost"]) == str(data.mstpInstanceIfPathCost) and
                    str(input_data["mstpInstanceIfPriority"]) == str(data.mstpInstanceIfPriority)),f'GET ERROR in Port_Mstp config (after {method})'
    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in Port_Mstp config {data._asdict}'


def test_Port_Mstp_config(rest_interface_module, node_id):

    bridge_config(rest_interface_module, node_id, Bridge_conf(1, 'PROVIDER_MSTP_EDGE', 100, 30, maxAge=6, maxHops=1, priority=12288), method='POST')
    # *********************************************************************************************
    for vlan in VLAN_DATA_conf_service:
        vlan_config(rest_interface_module, node_id, vlan, method='POST')  
    for vlan in VLAN_DATA_conf_CUSTOM:
        vlan_config(rest_interface_module, node_id, vlan, method='POST')  
    # *****************************************************************************
    Bridge_Mstp_config(rest_interface_module, node_id, Bridge_Mstp_DATA_conf[0], method='add')
    # ************************************************************    
    for port in range(1,4):
        switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port,index=4), method='POST')
    # **************************************************
    for port in range(1,3):
        Port_Mstp_config(rest_interface_module, node_id, Port_Mstp(port, 5, 0, 0, "Pass"), method='POST')
        if port<24:
            Port_Mstp_config(rest_interface_module, node_id, Port_Mstp(port+1, 5, 0, 0, "Fail"), method='POST')
        elif port==24:
              Port_Mstp_config(rest_interface_module, node_id, Port_Mstp(port-1, 5, 0, 0, "Fail"), method='POST')  
        Port_Mstp_config(rest_interface_module, node_id, Port_Mstp(port, 5, 0, 0, "Pass"), method='DELETE')
    # *************************************************
    for port in range(1,25):
        switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port,index=9), method='POST')
    #************************************************************
    Bridge_Mstp_config(rest_interface_module, node_id, Bridge_Mstp_DATA_conf[1], method='DELETE')
    #*****************************************************************************  
    for vlan in VLAN_DATA_conf_CUSTOM:
        vlan_config(rest_interface_module, node_id, vlan, method='DELETE')  
    for vlan in VLAN_DATA_conf_service:
        vlan_config(rest_interface_module, node_id, vlan, method='DELETE')       
    #***********************************************************************************************    
    bridge_config(rest_interface_module, node_id, Bridge_conf(1, 'PROVIDER_MSTP_EDGE', 100, 30, maxAge=6, maxHops=1, priority=12288), method='DELETE')







