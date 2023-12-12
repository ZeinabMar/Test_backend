import pytest
import logging
import json
from config import *
from conftest import *
from Switch.bridge_funcs import bridge_config
from Switch.test_vlan import vlan_config
from Switch.test_Bridge_group_conf import switch_config
from Switch.test_uplink_port_Vlan_conf import uplink_vlan_config

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)

IGMP = namedtuple('IGMP', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
IGMP.__new__.__defaults__ = (None, {}, {},None, None)


IGMP_DATA = (
IGMP(1, {
  "nodeId": None,
  "shelfId": 1,
  "slotId": 1,
  "vlanId": 10,
  "fastLeave": 1,
  "querier": 1,
  "staticGroup": "",
  "staticInt": 0,
  "staticSrc": "",
  "workMode": "PROXY",
  "mrouter": 1},{
                                                            "fastLeave": [1, "fastLeave"],
                                                            "querier": [1, "querier"],
                                                            "workMode": ["PROXCY", "workMode"],
                                                            "mrouter": [2, "mrouter"],
                                                            "vlanId": [10, "vlanId"]},result="Pass",method="ADD"),  
)
IGMP_Delete = (
    IGMP(1, {"nodeId":None, "slotId":1,"shelfId":1, "vlanId": 10},result="Pass",method="DELETE"), 
    IGMP(2, {"nodeId":None, "slotId":1,"shelfId":1, "vlanId": 11},result="Pass",method="DELETE"), 
)

def IGMP_Configuration(rest_interface_module, node_id, IGMP_data=IGMP(), method='ADD'):
    method = IGMP_data.method
    logger.info(f'IGMP CONFIGURATION TEST DATA ------- > {IGMP_data.index}')
    expected_set = IGMP_data.expected_result_Set
    expected_set["nodeId"]= int(node_id)
    expected_get = IGMP_data.expected_result_Get  

    logger.info(f"TRY TO {method} IGMP CONFIGURATION ...")
    if method == 'ADD':
        url = "/api/gponconfig/sp5100/igmp/add"
        response = rest_interface_module.post_request(url, expected_set)  
    elif method == 'UPDATE':  
        url = "/api/gponconfig/sp5100/igmp/update"
        response = rest_interface_module.post_request(url, data._asdict())       
    else:  # method==DELETE   
        url = f"/api/gponconfig/sp5100/igmp/delete/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["vlanId"])
        response = rest_interface_module.delete_request(url)

    if IGMP_data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in IGMP CONFIGURATION  {expected_set}'
        if response.status_code != 200:
            logger.error(response.message)
        #**********************************************************************
        if len(expected_get.keys()) !=0:
            logger.info(f' GETTING IGMP CONFIGURATION (after {method} method) ... ')
            read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/igmp/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["vlanId"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"{method} IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
            logger.info(f'check is completed in {method} method')
    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in IGMP CONFIGURATION {gem_data._asdict}'
        if len(expected_get.keys()) !=0:
            read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/igmp/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["vlanId"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"set steeep IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)





def test_IGMP_Configuration(rest_interface_module, node_id):
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgeconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
    bridge_config(rest_interface_module, node_id, Bridge_conf(), method='POST')
    # ****************************************************************************************************************************
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/vlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
    for vlan in VLAN_DATA_conf_CUSTOM:
        vlan_config(rest_interface_module, node_id, vlan, method='POST')  
    for port in range(1,3):
        response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgegroupconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
        switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port, index=4), method='POST')
        response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/portvlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
        uplink_vlan_config(rest_interface_module, node_id, uplink_vlan_conf_DATA[1]._replace(ethIfIndex=port), method='POST')  


    for igmp in IGMP_DATA:
        IGMP_Configuration(rest_interface_module, node_id, igmp)
    for igmp in IGMP_Delete:
        IGMP_Configuration(rest_interface_module, node_id, igmp)

    for port in range(1,3):  
        response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/portvlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
        uplink_vlan_config(rest_interface_module, node_id, uplink_vlan_conf_DATA[1]._replace(ethIfIndex=port), method='DELETE')   
        response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgegroupconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
        switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port, index=9), method='DELETE')
    
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/vlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
    for vlan in VLAN_DATA_conf_CUSTOM:
        vlan_config(rest_interface_module, node_id, vlan, method='DELETE')
    #****************************************************************************************************************************
    bridge_config(rest_interface_module, node_id, Bridge_conf(), method='DELETE')