import pytest
import logging
import json
from config import *
from conftest import *
from Pon.test_tcont_profile import Tcont_Management
from Pon.test_dba_profile import DBA_Profile
from Pon.test_Service_Profile_Definition import Service_Profile_Definition
from Switch.bridge_funcs import bridge_config
from Switch.test_vlan import vlan_config
from Pon.test_Service_Profile_Tcont import Tcont_Service_Profile
from Pon.test_Service_Profile_Gem import Gem_Service_Profile
from Pon.test_Service_Profile_OLT import Olt_Service_Profile

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)


remote_service_profile = namedtuple('remote_service_profile', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
remote_service_profile.__new__.__defaults__ = (None, {}, {},None, None)



remote_service_profile_Data = (
remote_service_profile(1, {"nodeId": None,"shelfId": 1, "slotId": 1,"onuId": 1, "rmServiceId": "1","onuPortType": "VEIP",
                           "onuPortId": 0,"vlanMode": "ACCESS","gemId": 1,"pvId": "10","priority": "1",}, {"rmServiceId": [1, "rmServiceId"],
                                                                                                           "onuPortType": ["VEIP", "onuPortType"],
                                                                                                           "vlanMode": ["ACCESS", "vlanMode"],
                                                                                                           "priority": [1, "priority"],
                                                                                                           "pvId": [10, "pvId"],
                                                                                                           "onuId": [1, "onuId"],
                                                                                                           "gemId": [1, "gemId"]},result="Pass",method="ADD"),

remote_service_profile(2, {"nodeId": None,"shelfId": 1, "slotId": 1,"onuId": 2, "rmServiceId": "1","onuPortType": "ETH_UNI",
                           "onuPortId": 0,"vlanMode": "TRUNK", "vlanList":"10", "gemId": 1,"pvId": None,"priority": "1",}, {"rmServiceId": [1, "rmServiceId"],
                                                                                                           "onuPortType": ["ETH_UNI", "onuPortType"],
                                                                                                           "vlanMode": ["TRUNK", "vlanMode"],
                                                                                                           "vlanList": [10, "vlanList"],
                                                                                                           "priority": [0, "priority"],
                                                                                                           "pvId": [0, "pvId"],
                                                                                                           "onuId": [2, "onuId"],
                                                                                                           "gemId": [1, "gemId"]},result="Pass",method="ADD"),
remote_service_profile(3, {"nodeId": None,"shelfId": 1, "slotId": 1,"onuId": 2, "rmServiceId": "2","onuPortType": "ETH_UNI",
                           "onuPortId": 0,"vlanMode": "TRUNK", "vlanList":"11", "gemId": 2,"pvId": None,"priority": "1",}, {"rmServiceId": [2, "rmServiceId"],
                                                                                                           "onuPortType": ["ETH_UNI", "onuPortType"],
                                                                                                           "vlanMode": ["TRUNK", "vlanMode"],
                                                                                                           "vlanList": [11, "vlanList"],
                                                                                                           "priority": [0, "priority"],
                                                                                                           "pvId": [0, "pvId"],
                                                                                                           "onuId": [2, "onuId"],
                                                                                                           "gemId": [2, "gemId"]},result="Pass",method="ADD"),
remote_service_profile(4, {"nodeId": None,"shelfId": 1, "slotId": 1,"onuId": 2, "rmServiceId": "2","onuPortType": "ETH_UNI",
                           "onuPortId": 0,"vlanMode": "ACCESS", "vlanList":"12", "gemId": 2,"pvId": None,"priority": "1",}, {"rmServiceId": [2, "rmServiceId"],
                                                                                                           "onuPortType": ["ETH_UNI", "onuPortType"],
                                                                                                           "vlanMode": ["TRUNK", "vlanMode"],
                                                                                                           "vlanList": [11, "vlanList"],
                                                                                                           "priority": [0, "priority"],
                                                                                                           "pvId": [0, "pvId"],
                                                                                                           "onuId": [2, "onuId"],
                                                                                                           "gemId": [2, "gemId"]},result="Fail",method="ADD"),

)  

remote_service_profile_Delete = (
    remote_service_profile(1, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 1, "rmServiceId": 1},result="Pass",method="DELETE"), 
    remote_service_profile(2, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 2, "rmServiceId": 2},result="Pass",method="DELETE"), 
    remote_service_profile(3, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 2, "rmServiceId": 1},result="Pass",method="DELETE"), 
)

def Remote_Service_Profile(rest_interface_module, node_id, remote_service_profile_data=remote_service_profile(), method='ADD'):
    method = remote_service_profile_data.method
    logger.info(f'SERVICE PROFILE REMOTE ONU TEST DATA ------- > {remote_service_profile_data.index}')
    expected_set = remote_service_profile_data.expected_result_Set
    expected_set["nodeId"]= int(node_id)
    expected_get = remote_service_profile_data.expected_result_Get  

    logger.info(f"TRY TO {method} SERVICE PROFILE REMOTE ONU CONFIG ...")
    if method == 'ADD':
        url = "/api/gponconfig/sp5100/rmserviceprofile/add"
        response = rest_interface_module.post_request(url, expected_set)    
    else:  # method==DELETE   
        url = f"/api/gponconfig/sp5100/rmserviceprofile/delete/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["rmServiceId"])
        response = rest_interface_module.delete_request(url)

    if remote_service_profile_data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in SERVICE PROFILE REMOTE ONU {expected_set}'
        if response.status_code != 200:
            logger.error(response.message)
        #**********************************************************************
        if len(expected_get.keys()) !=0:
            logger.info(f' GETTING SERVICE PROFILE REMOTE ONU (after {method} method) ... ')
            read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/rmserviceprofile/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["rmServiceId"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"{method} IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
            logger.info(f'check is completed in {method} method')

    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in SERVICE PROFILE REMOTE ONU {service_data._asdict}'
        if len(expected_get.keys()) !=0:
            read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/rmserviceprofile/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["rmServiceId"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"set steeep IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)





def test_Remote_Service_Profile(rest_interface_module, node_id):

    bridge_config(rest_interface_module, node_id, Bridge_conf(), method='POST')
    # ****************************************************************************************************************************
    for vlan in VLAN_DATA_conf_CUSTOM:
        vlan_config(rest_interface_module, node_id, vlan, method='POST')  

    for dba in dba_profile_Data_Config:
        DBA_Profile(rest_interface_module, node_id, dba, method='ADD')
    for service_def in Onu_Service_Profile_Data_Config:
        Service_Profile_Definition(rest_interface_module, node_id, service_def, method='ADD')
    for service_tcont in Tcont_service_profile_Data_Config:
        Tcont_Service_Profile(rest_interface_module, node_id, service_tcont)
    for service_gem in Gem_service_profile_Data_Config:
        Gem_Service_Profile(rest_interface_module, node_id, service_gem)
    for olt_service_p in olt_service_profile_Data_Config:
        Olt_Service_Profile(rest_interface_module, node_id, olt_service_p)

    for remote_p in remote_service_profile_Data:
        Remote_Service_Profile(rest_interface_module, node_id, remote_p)
    for remote_p in remote_service_profile_Delete:
        Remote_Service_Profile(rest_interface_module, node_id, remote_p)

    for olt_service_p in olt_service_profile_Delete_Config:
        Olt_Service_Profile(rest_interface_module, node_id, olt_service_p)    
    for service_gem in Gem_service_profile_Delete_Config:
        Gem_Service_Profile(rest_interface_module, node_id, service_gem)
    for service_tcont in Tcont_service_profile_Delete_Config:
        Tcont_Service_Profile(rest_interface_module, node_id, service_tcont)
    for service_def in Onu_Service_Profile_Delete_Config:
        Service_Profile_Definition(rest_interface_module, node_id, service_def, method='DELETE')    
    for dba in dba_profile_Data_Config_Delete:
        DBA_Profile(rest_interface_module, node_id, dba, method='DELETE')      

    for vlan in VLAN_DATA_conf_CUSTOM:
        vlan_config(rest_interface_module, node_id, vlan, method='DELETE')  
    #****************************************************************************************************************************
    bridge_config(rest_interface_module, node_id, Bridge_conf(), method='DELETE')    