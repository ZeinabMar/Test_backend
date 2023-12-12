import pytest
import logging
import json
from config import *
from conftest import *
from Pon.test_tcont_profile import Tcont_Management
from Pon.test_dba_profile import DBA_Profile
from Pon.test_gem_profile import Gem_Management
from Switch.bridge_funcs import bridge_config
from Switch.test_vlan import vlan_config
from Switch.test_Bridge_group_conf import switch_config
from Switch.test_uplink_port_Vlan_conf import uplink_vlan_config
from Pon.test_OLT_Service import OLT_Service


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)

remote_service_profile = namedtuple('remote_service_profile', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
remote_service_profile.__new__.__defaults__ = (None, {}, {},None, None)

#     {"portId": 1, "onuId": 1, "rmServiceId": 1, "onuPortType": "VEIP", "onuPortId": 1, "vlanMode": "ACCESS", "gemId": 1, "pvId": 50, "vlanList": None, "priority": 3, "result": 'Pass'},

#    {"portId": 1, "onuId": 1, "rmServiceId": 2, "onuPortType": "VEIP", "onuPortId": 1, "vlanMode": "TRUNK", "gemId": 2, "pvId": None, "vlanList": "60", "priority": 2, "result": 'Pass'},
#     {"portId": 1, "onuId": 1, "rmServiceId": 3, "onuPortType": "VEIP", "onuPortId": 1, "vlanMode": "HYBRID", "gemId": 1, "pvId": 10, "vlanList": "20", "priority": 1, "result": 'Pass'},
#     {"portId": 1, "onuId": 1, "rmServiceId": 4, "onuPortType": "ETH_UNI", "onuPortId": 1, "vlanMode": "XLATE", "gemId": 2, "pvId": "60", "vlanList": "70", "priority": 1, "result": 'Pass'},
#     {"portId": 1, "onuId": 1, "rmServiceId": 5, "onuPortType": "ETH_UNI", "onuPortId": 1, "vlanMode": "TRANSPARENT", "gemId": 1, "pvId": None, "vlanList": None, "priority": 1, "result": 'Pass'},
#     {"portId": 1, "onuId": 1, "rmServiceId": 1, "onuPortType": "ETH_UNI", "onuPortId": 1, "vlanMode": None, "gemId": 1, "pvId": 750, "vlanList": "500", "priority": 1, "result": 'Fail'},



remote_service_profile_Data = (
remote_service_profile(1, {
    "nodeId": None,"shelfId": 1,"slotId": 1,"portId": 2,"onuId": 1, "rmServiceId": "1",
    "onuPortType": "VEIP","onuPortId": 0,"vlanMode": "ACCESS","gemId": 1,"pvId": "10","priority": "3",}, {"rmServiceId": [1, "rmServiceId"],
                                                                                                "onuPortType": ["VEIP", "onuPortType"],
                                                                                                "onuPortId": [0, "onuPortId"],
                                                                                                "onuId": [1, "onuId"],
                                                                                                "portId": [2, "portId"],
                                                                                                "gemId": [1, "gemId"],
                                                                                                "vlanMode": ["ACCESS", "vlanMode"],
                                                                                                "pvId": [10, "pvId"],
                                                                                                "priority": [3, "priority"],},result="Pass",method="ADD"),
remote_service_profile(2, {
    "nodeId": None,"shelfId": 1,"slotId": 1,"portId": 2,"onuId": 1,"rmServiceId": "2","onuPortType": "VEIP",
    "onuPortId": 0,"vlanMode": "TRUNK", "gemId": 1,"vlanList": "10", "pvId": None,"priority": None,}, {"rmServiceId": [2, "rmServiceId"],
                                                                                                "onuPortType": ["VEIP", "onuPortType"],
                                                                                                "onuPortId": [0, "onuPortId"],
                                                                                                "onuId": [1, "onuId"],
                                                                                                "portId": [2, "portId"],
                                                                                                "gemId": [1, "gemId"],
                                                                                                "vlanMode": ["TRUNK", "vlanMode"],
                                                                                                "vlanList": [10, "vlanList"],
                                                                                                "priority": [0, "priority"],},result="Pass",method="ADD"),

remote_service_profile(3, {
    "nodeId": None,"shelfId": 1,"slotId": 1,"portId": 3,"onuId": 1,"rmServiceId": "1","onuPortType": "VEIP",
    "onuPortId": 0,"vlanMode": "TRUNK", "gemId": 1,"vlanList": "10", "pvId": None,"priority": None,}, {"rmServiceId": [1, "rmServiceId"],
                                                                                                "onuPortType": ["VEIP", "onuPortType"],
                                                                                                "onuPortId": [0, "onuPortId"],
                                                                                                "onuId": [1, "onuId"],
                                                                                                "portId": [3, "portId"],
                                                                                                "gemId": [1, "gemId"],
                                                                                                "vlanMode": ["TRUNK", "vlanMode"],
                                                                                                "vlanList": [10, "vlanList"],
                                                                                                "priority": [0, "priority"],},result="Pass",method="ADD"),
)                                                       
remote_service_profile_Data_Delete = (
    remote_service_profile(1, {"nodeId":None, "slotId":1,"shelfId":1, "rmServiceId": 1, "onuId": 1, "portId": 2},result="Pass",method="DELETE"), 
    remote_service_profile(2, {"nodeId":None, "slotId":1,"shelfId":1, "rmServiceId": 2, "onuId": 1, "portId": 2},result="Pass",method="DELETE"),  
    remote_service_profile(3, {"nodeId":None, "slotId":1,"shelfId":1, "rmServiceId": 1, "onuId": 1, "portId": 3},result="Pass",method="DELETE"),  
)

def ONU_remote_Service(rest_interface_module, node_id, remote_service_data=remote_service_profile(), method='ADD'):
    method = remote_service_data.method
    logger.info(f'REMOTE SERVICE TEST DATA ------- > {remote_service_data.index}')
    expected_set = remote_service_data.expected_result_Set
    expected_set["nodeId"]= int(node_id)
    expected_get = remote_service_data.expected_result_Get  

    logger.info(f"TRY TO {method} REMOTE SERVICE PROFILE CONFIG ...")
    if method == 'ADD':
        url = "/api/gponconfig/sp5100/rmonu/service/add"
        response = rest_interface_module.post_request(url, expected_set)    
    else:  # method==DELETE   
        url = f"/api/gponconfig/sp5100/rmonu/service/delete/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["rmServiceId"])
        response = rest_interface_module.delete_request(url)

    if remote_service_data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in PROFILE DBA config {expected_set}'
        if response.status_code != 200:
            logger.error(response.message)
        #**********************************************************************
        if len(expected_get.keys()) !=0:
            logger.info(f' GETTING Remote Service (after {method} method) ... ')
            read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/rmonu/service/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["rmServiceId"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"{method} IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
            logger.info(f'check is completed in {method} method')

    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in REMOTE SERVICE PROFILE {service_data._asdict}'
        if len(expected_get.keys()) !=0:
            read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/rmonu/service/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["rmServiceId"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"set steeep IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)





def test_ONU_remote_Service(rest_interface_module, node_id):
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgeconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
    bridge_config(rest_interface_module, node_id, Bridge_conf(), method='POST')
    # ****************************************************************************************************************************
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/vlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
    for vlan in VLAN_DATA_conf_CUSTOM:
        vlan_config(rest_interface_module, node_id, vlan, method='POST')  
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgegroupconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
    for port in range(1,4):
        switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port, index=4), method='POST')
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/portvlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
    for uplink in uplink_vlan_conf_DATA:    
        uplink_vlan_config(rest_interface_module, node_id, uplink, method='POST') 
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/dbaProfile/getall?nodeId={node_id}&shelfId=1&slotId=1")
    for dba in dba_profile_Data_Config:
        DBA_Profile(rest_interface_module, node_id, dba, method='ADD')
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/tcont/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=2&onuId=-1")
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/tcont/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=3&onuId=-1")
    for tcont in tcont_Data_Config:
        Tcont_Management(rest_interface_module, node_id, tcont)
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/gem/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=2&onuId=1")
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/gem/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=3&onuId=1")
    for gem in gem_profile_Data_Config:
        Gem_Management(rest_interface_module, node_id, gem)
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/service/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=2&onuId=1")
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/service/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=3&onuId=1")
    for service in service_profile_Data_Config:
        OLT_Service(rest_interface_module, node_id, service)
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/rmonu/service/getall?nodeId={node_id}&shelfId=1&slotId=1&onuId=1&portId=2")
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/rmonu/service/getall?nodeId={node_id}&shelfId=1&slotId=1&onuId=1&portId=3")
    for remote in remote_service_profile_Data:
        ONU_remote_Service(rest_interface_module, node_id, remote)

    for remote in remote_service_profile_Data_Delete:
        ONU_remote_Service(rest_interface_module, node_id, remote)

    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/service/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=2&onuId=1")
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/service/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=3&onuId=1")
    for service in service_profile_Data_Delete_Config:
        OLT_Service(rest_interface_module, node_id, service)
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/gem/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=2&onuId=1")
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/gem/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=3&onuId=1")
    for gem in gem_profile_Data_Delete_Config:
        Gem_Management(rest_interface_module, node_id, gem)
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/tcont/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=2&onuId=-1")
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/tcont/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=3&onuId=-1")
    for tcont in tcont_Data_Delete_Config:
        Tcont_Management(rest_interface_module, node_id, tcont)
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/dbaProfile/getall?nodeId={node_id}&shelfId=1&slotId=1")
    for dba in dba_profile_Data_Config_Delete:
        DBA_Profile(rest_interface_module, node_id, dba, method='DELETE')       
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/portvlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
    for uplink in uplink_vlan_conf_DATA:    
        uplink_vlan_config(rest_interface_module, node_id, uplink, method='DELETE') 
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgegroupconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
    for port in range(1,4):
        switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port,index=9), method='DELETE')
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/vlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
    for vlan in VLAN_DATA_conf_CUSTOM:
        vlan_config(rest_interface_module, node_id, vlan, method='DELETE')
    #****************************************************************************************************************************
    bridge_config(rest_interface_module, node_id, Bridge_conf(), method='DELETE')          