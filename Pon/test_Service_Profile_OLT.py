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

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)


olt_service_profile = namedtuple('olt_service_profile', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
olt_service_profile.__new__.__defaults__ = (None, {}, {},None, None)

olt_service_profile_Data = (
olt_service_profile(1, {"servicePortId": "1","nodeId": None,"shelfId": 1, "slotId": 1, "portShowName": "PON ",
                        "onuId": 1,"gemId": 1,"vlan": 0,"svlan": 0,"userVlan": "10","innerVlan": 0,
                        "vlanPriority": 0,"svlanPriority": 0,"vlanPriorityAction": "1","svlanPriorityAction": "1",
                        "cosQueueProfileId": 0,"queue": 0,"queueSelectMode": 0,"upLinkC2CId": 0,"downLinkC2CId": 0,}, {"servicePortId": [1, "servicePortId"],
                                                                                                                       "userVlan": [10, "userVlan"],
                                                                                                                       "onuId": [1, "onuId"],
                                                                                                                       "gemId": [1, "gemId"]},result="Pass",method="ADD"),
olt_service_profile(2, {"servicePortId": "2","nodeId": None,"shelfId": 1, "slotId": 1, "portShowName": "PON ",
                        "onuId": 1,"gemId": 2,"vlan": 0,"svlan": 0,"userVlan": "11","innerVlan": 0,
                        "vlanPriority": 0,"svlanPriority": 0,"vlanPriorityAction": "1","svlanPriorityAction": "1",
                        "cosQueueProfileId": 0,"queue": 0,"queueSelectMode": 0,"upLinkC2CId": 0,"downLinkC2CId": 0,},result="Fail",method="ADD"),

olt_service_profile(3, {"servicePortId": "1","nodeId": None,"shelfId": 1, "slotId": 1, "portShowName": "PON ",
                        "onuId": 2,"gemId": 1,"vlan": 0,"svlan": 0,"userVlan": "10","innerVlan": 0,
                        "vlanPriority": 0,"svlanPriority": 0,"vlanPriorityAction": "1","svlanPriorityAction": "1",
                        "cosQueueProfileId": 0,"queue": 0,"queueSelectMode": 0,"upLinkC2CId": 0,"downLinkC2CId": 0,}, {"servicePortId": [1, "servicePortId"],
                                                                                                                       "userVlan": [10, "userVlan"],
                                                                                                                       "onuId": [2, "onuId"],
                                                                                                                       "gemId": [1, "gemId"]},result="Pass",method="ADD"),
olt_service_profile(4, {"servicePortId": "2","nodeId": None,"shelfId": 1, "slotId": 1, "portShowName": "PON ",
                        "onuId": 2,"gemId": 2,"vlan": 0,"svlan": 0,"userVlan": "11","innerVlan": 0,
                        "vlanPriority": 0,"svlanPriority": 0,"vlanPriorityAction": "1","svlanPriorityAction": "1",
                        "cosQueueProfileId": 0,"queue": 0,"queueSelectMode": 0,"upLinkC2CId": 0,"downLinkC2CId": 0,}, {"servicePortId": [2, "servicePortId"],
                                                                                                                       "userVlan": [11, "userVlan"],
                                                                                                                       "onuId": [2, "onuId"],
                                                                                                                       "gemId": [2, "gemId"]},result="Pass",method="ADD"),

)  

olt_service_profile_Delete = (
    olt_service_profile(1, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 1, "servicePortId": 1},result="Pass",method="DELETE"), 
    olt_service_profile(1, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 2, "servicePortId": 2},result="Pass",method="DELETE"), 
    olt_service_profile(2, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 2, "servicePortId": 1},result="Pass",method="DELETE"), 
)

def Olt_Service_Profile(rest_interface_module, node_id, olt_service_profile_data=olt_service_profile(), method='ADD'):
    method = olt_service_profile_data.method
    logger.info(f'SERVICE PROFILE OLT TEST DATA ------- > {olt_service_profile_data.index}')
    expected_set = olt_service_profile_data.expected_result_Set
    expected_set["nodeId"]= int(node_id)
    expected_get = olt_service_profile_data.expected_result_Get  

    logger.info(f"TRY TO {method} SERVICE PROFILE OLT CONFIG ...")
    if method == 'ADD':
        url = "/api/gponconfig/serviceprofile/add"
        response = rest_interface_module.post_request(url, expected_set)    
    else:  # method==DELETE   
        url = f"/api/gponconfig/serviceprofile/delete/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["servicePortId"])
        response = rest_interface_module.delete_request(url)

    if olt_service_profile_data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in SERVICE PROFILE OLT {expected_set}'
        if response.status_code != 200:
            logger.error(response.message)
        #**********************************************************************
        if len(expected_get.keys()) !=0:
            logger.info(f' GETTING SERVICE PROFILE OLT (after {method} method) ... ')
            read_data = rest_interface_module.get_request(f"/api/gponconfig/serviceprofile/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["servicePortId"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"{method} IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
            logger.info(f'check is completed in {method} method')

    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in SERVICE PROFILE OLT {service_data._asdict}'
        if len(expected_get.keys()) !=0:
            read_data = rest_interface_module.get_request(f"/api/gponconfig/serviceprofile/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["servicePortId"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"set steeep IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)





def test_Olt_Service_Profile(rest_interface_module, node_id):

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

    for olt_service_p in olt_service_profile_Data:
        Olt_Service_Profile(rest_interface_module, node_id, olt_service_p)
    for olt_service_p in olt_service_profile_Delete:
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