import pytest
import logging
import json
from conftest import *
from config import *
from Switch.test_vlan import vlan_config
from Switch.bridge_funcs import bridge_config
from Switch.test_Bridge_group_conf import switch_config
from Switch.test_Bridge_Mstp_instance_conf import Bridge_Mstp_config
# from pytest-check import check


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

Port_Mstp_add = namedtuple('Port_Mstp_add', ['ifIndex', 'instanceIfIndex', 'result','shelfId', 'slotId', 'nodeId'])
Port_Mstp_add.__new__.__defaults__ = (None, None, "Pass", 1, 1, None)

Port_Mstp_POST = namedtuple('Port_Mstp_POST', ['ifIndex', 'instanceIfIndex','mstpInstanceIfPathCost', 
                       'mstpInstanceIfPriority', "id", 'result','shelfId', 'slotId', 'nodeId'])
Port_Mstp_POST.__new__.__defaults__ = (None, None, None, 0, 0, 0, "Pass", 1, 1, None)


def Port_Mstp_config(rest_interface_module, node_id, Port_Mstp_data=Port_Mstp_add(), method='POST'):
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
                    input_data["instanceIfIndex"] == data.instanceIfIndex),f'IN Everythig is ok Port_Mstp config(after {method}'
            logger.info(f'every thing ok after Port_Mstp config(after {method} ')

        elif method == 'POST':
            assert (input_data["ifIndex"]==data.ifIndex and
                    input_data["instanceIfIndex"] == data.instanceIfIndex and 
                    str(input_data["mstpInstanceIfPathCost"]) == str(data.mstpInstanceIfPathCost) and
                    str(input_data["mstpInstanceIfPriority"]) == str(data.mstpInstanceIfPriority)),f'IN Everythig is ok Port_Mstp config(after {method}'
            logger.info(f'every thing ok after Port_Mstp config(after {method} ')

        # else:  # method==DELETE
        #     assert (input_data["ifIndex"]==data.ifIndex and
        #             input_data["instanceIfIndex"] == data.instanceIfIndex and 
        #             str(input_data["mstpInstanceIfPathCost"]) == str(data.mstpInstanceIfPathCost) and
        #             str(input_data["mstpInstanceIfPriority"]) == str(data.mstpInstanceIfPriority)),f'GET ERROR in Port_Mstp config (after {method})'
    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in Port_Mstp config {data._asdict}'


def test_Port_Mstp_config(rest_interface_module, node_id):
    response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/bridgeconfig/getall?nodeId=11&shelfId=1&slotId=1")
    bridge_config(rest_interface_module, node_id, Bridge_conf(1, 'PROVIDER_MSTP_EDGE', 100, 30, maxAge=6, maxHops=1, priority=12288), method='POST')
    # *********************************************************************************************
    response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/vlan/getall?nodeId=11&shelfId=1&slotId=1")
    for vlan in VLAN_DATA_conf_service:
        vlan_config(rest_interface_module, node_id, vlan, method='POST')  
    for vlan in VLAN_DATA_conf_CUSTOM:
        vlan_config(rest_interface_module, node_id, vlan, method='POST')  
    # *****************************************************************************
    response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/bridgemstpinstanceconfig/getall?nodeId=11&shelfId=1&slotId=1")
    Bridge_Mstp_config(rest_interface_module, node_id, Bridge_Mstp_DATA_conf[0], method='add')
    # ************************************************************    
    for port in range(1,2):
        response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/bridgegroupconfig/getall?nodeId=11&shelfId=1&slotId=1")
        switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port,index=4), method='POST')
    # **************************************************
    for port in range(1,2):
        response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/portmstpconfig/getall?nodeId=11&shelfId=1&slotId=1")
        Port_Mstp_config(rest_interface_module, node_id, Port_Mstp_add(port, 5, "Pass"), method='add')
        # Port_Mstp_config(rest_interface_module, node_id, Port_Mstp_POST(port, 5, 1, 1, 5, "Pass"), method='POST')
        if port<24:
            Port_Mstp_config(rest_interface_module, node_id, Port_Mstp_add(port+1, 5, "Fail"), method='add')
        elif port==24:
              Port_Mstp_config(rest_interface_module, node_id, Port_Mstp_add(port-1, 5, "Fail"), method='add')  
        Port_Mstp_config(rest_interface_module, node_id, Port_Mstp_add(port, 5, "Pass"), method='DELETE')
    # *************************************************
    for port in range(1,2):
        switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port,index=9), method='DELETE')
    #************************************************************
    response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/bridgemstpinstanceconfig/getall?nodeId=11&shelfId=1&slotId=1")
    Bridge_Mstp_config(rest_interface_module, node_id, Bridge_Mstp_DATA_conf[1], method='DELETE')
    #*****************************************************************************  
    response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/vlan/getall?nodeId=11&shelfId=1&slotId=1")
    for vlan in VLAN_DATA_conf_CUSTOM:
        vlan_config(rest_interface_module, node_id, vlan, method='DELETE')  
    for vlan in VLAN_DATA_conf_service:
        vlan_config(rest_interface_module, node_id, vlan, method='DELETE')       
    #***********************************************************************************************    
    bridge_config(rest_interface_module, node_id, Bridge_conf(1, 'PROVIDER_MSTP_EDGE', 100, 30, maxAge=6, maxHops=1, priority=12288), method='DELETE')







