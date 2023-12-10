import pytest
import logging
import json
from config import *
from conftest import *
from Switch.bridge_funcs import bridge_config
from Switch.test_vlan import vlan_config
from Switch.test_Bridge_group_conf import switch_config

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)

mapping = namedtuple('mapping', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
mapping.__new__.__defaults__ = (None, {}, {},None, None)

Mapping_Data = (


mapping(1, {"nodeId": None,"shelfId": 1,"slotId": 1, "ifIndex": 1, "vlanId": 10,"vlanTranslatedId": 11},{"ifIndex": [1, "ifIndex"],
                                                                                                         "vlanId": [10, "vlanId"],
                                                                                                         "vlanTranslatedId": [11, "vlanTranslatedId"]},result="Pass", method="ADD"),  
mapping(2, {"nodeId": None,"shelfId": 1,"slotId": 1, "ifIndex": 1, "vlanId": 10,"vlanTranslatedId": 12},{"ifIndex": [1, "ifIndex"],
                                                                                                         "vlanId": [10, "vlanId"],
                                                                                                         "vlanTranslatedId": [12, "vlanTranslatedId"]},result="Pass", method="ADD"),  
mapping(3, {"nodeId": None,"shelfId": 1,"slotId": 1, "ifIndex": 2, "vlanId": 10,"vlanTranslatedId": 11},{"ifIndex": [2, "ifIndex"],
                                                                                                         "vlanId": [10, "vlanId"],
                                                                                                         "vlanTranslatedId": [11, "vlanTranslatedId"]},result="Pass", method="ADD"),  

)


Mapping_Delete = (
    mapping(1, {"nodeId": None,"shelfId": 1,"slotId": 1, "ifIndex": 1, "vlanId": 10,"vlanTranslatedId": 11},result="Pass", method="DELETE"),
    mapping(2, {"nodeId": None,"shelfId": 1,"slotId": 1, "ifIndex": 1, "vlanId": 10,"vlanTranslatedId": 12},result="Pass", method="DELETE"),  
    mapping(3, {"nodeId": None,"shelfId": 1,"slotId": 1, "ifIndex": 2, "vlanId": 10,"vlanTranslatedId": 11},result="Pass", method="DELETE"),  
  
)

def Mapping(rest_interface_module, node_id, mapping_data=mapping(), method='ADD'):
    logger.info(f'MAPPING TEST DATA ------- > {mapping_data.index}')
    expected_set = mapping_data.expected_result_Set
    expected_set["nodeId"]= node_id
    expected_get = mapping_data.expected_result_Get  

    logger.info(f"TRY TO {method} MAPPING CONFIG ...")
    if method == 'ADD':
        url = "/api/gponconfig/sp5100/vlan/mapping/add"
        response = rest_interface_module.post_request(url, expected_set) 
    elif method == "DELETE":
        url = f"/api/gponconfig/sp5100/vlan/mapping/delete/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["ifIndex"])+"/"+str(expected_set["vlanId"])+"/"+str(expected_set["vlanTranslatedId"])
        response = rest_interface_module.delete_request(url)

    if mapping_data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in DBA_Profile config {expected_set}'
        if response.status_code != 200:
            logger.error(response.message)
        if len(expected_get.keys()) !=0:
            logger.info(f' GETTING MAPPING (after {method} method) ... ')
            read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/vlan/mapping/getall?nodeId="+str(expected_set["nodeId"])+"&shelfId="+str(expected_set["shelfId"])+"&slotId="+str(expected_set["slotId"]))
            input_data_getall = json.loads(read_data.text)
            input_data = find_in_getall(input_data_getall, "ifIndex", expected_get["ifIndex"][0])
            for key in expected_get.keys():
                logger.info(f"{method} IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
            logger.info(f'check is completed in {method} method')
    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in MAPPING {expected_set}'
        if len(expected_get.keys()) !=0:
            logger.info(f' GETTING MAPPING (after {method} method) ... ')
            read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/vlan/mapping/getall?nodeId="+str(expected_set["nodeId"])+"&shelfId="+str(expected_set["shelfId"])+"&slotId="+str(expected_set["slotId"]))
            input_data_getall = json.loads(read_data.text)
            input_data = find_in_getall(input_data_getall, "ifIndex", expected_get["ifIndex"][0])
            for key in expected_get.keys():
                logger.info(f"set steeep IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)



def test_Mapping(rest_interface_module, node_id):
    response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/bridgeconfig/getall?nodeId=11&shelfId=1&slotId=1")
    bridge_config(rest_interface_module, node_id, Bridge_conf(), method='POST')
    # ****************************************************************************************************************************
    response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/vlan/getall?nodeId=11&shelfId=1&slotId=1")
    for vlan in VLAN_DATA_conf_CUSTOM:
        vlan_config(rest_interface_module, node_id, vlan, method='POST')  
    for port in range(1,3):
        response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/bridgegroupconfig/getall?nodeId=11&shelfId=1&slotId=1")
        switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port, index=4), method='POST')
    response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/vlan/mapping/getall?nodeId=11&shelfId=1&slotId=1")
    for map in Mapping_Data:
        Mapping(rest_interface_module, node_id, map, method='ADD')
    response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/vlan/mapping/getall?nodeId=11&shelfId=1&slotId=1")
    for map in Mapping_Delete:
        Mapping(rest_interface_module, node_id, map, method='DELETE')  


    for port in range(1,3):   
        response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/bridgegroupconfig/getall?nodeId=11&shelfId=1&slotId=1")
        switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port, index=9), method='DELETE')
    #*********************************************************************************************************************  
    response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/vlan/getall?nodeId=11&shelfId=1&slotId=1")
    for vlan in VLAN_DATA_conf_CUSTOM:
        vlan_config(rest_interface_module, node_id, vlan, method='DELETE')
    #****************************************************************************************************************************
    bridge_config(rest_interface_module, node_id, Bridge_conf(), method='DELETE')      
