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



pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)

service_olt = namedtuple('service_olt', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
service_olt.__new__.__defaults__ = (None, {}, {},None, None)

service_olt_Data = (
service_olt(1, {"nodeId":None, "slotId":1,"shelfId":1, "servicePortId": "1", "onuId": 1, "portId": 2, "gemId": 1, "userVlan": "10"},
                                                           {
                                                            "gemId": [1, "gemId"],
                                                            "servicePortId": [1, "servicePortId"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [2, "portId"],
                                                            "userVlan": [10, "userVlan"],},result="Pass",method="ADD"),  
service_olt(2, {"nodeId":None, "slotId":1,"shelfId":1, "servicePortId": "2", "onuId": 1, "portId": 2, "gemId": 1, "userVlan": "10"},
                                                           {
                                                            "gemId": [1, "gemId"],
                                                            "servicePortId": [2, "servicePortId"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [2, "portId"],
                                                            "userVlan": [10, "userVlan"],},result="Pass",method="ADD"),   
service_olt(3, {"nodeId":None, "slotId":1,"shelfId":1, "servicePortId": "1", "onuId": 1, "portId": 3, "gemId": 1, "userVlan": "10"},
                                                           {
                                                            "gemId": [1, "gemId"],
                                                            "servicePortId": [1, "servicePortId"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [3, "portId"],
                                                            "userVlan": [10, "userVlan"],},result="Pass",method="ADD"),                                                            
service_olt(4, {"nodeId":None, "slotId":1,"shelfId":1, "servicePortId": "2", "onuId": 1, "portId": 2, "gemId": 2, "userVlan": "10"},
                                                           {
                                                            "gemId": [1, "gemId"],
                                                            "servicePortId": [2, "servicePortId"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [2, "portId"],
                                                            "userVlan": [10, "userVlan"],},result="Fail",method="ADD"), 

service_olt(5, {"nodeId":None, "slotId":1,"shelfId":1, "servicePortId": "2", "onuId": 1, "portId": 2, "gemId": 1, "userVlan": "11"},
                                                           {
                                                            "gemId": [1, "gemId"],
                                                            "servicePortId": [2, "servicePortId"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [2, "portId"],
                                                            "userVlan": [10, "userVlan"],},result="Fail",method="ADD"),   
                                                            
service_olt(6, {"nodeId":None, "slotId":1,"shelfId":1, "servicePortId": "2", "onuId": 1, "portId": 2, "gemId": 1, "userVlan": 100},result="Fail",method="ADD"),                                                              
)   
  
service_olt_Data_Delete = (
    service_olt(1, {"nodeId":None, "slotId":1,"shelfId":1, "servicePortId": 1, "onuId": 1, "portId": 2},result="Pass",method="DELETE"),  
    service_olt(1, {"nodeId":None, "slotId":1,"shelfId":1, "servicePortId": 2, "onuId": 1, "portId": 2},result="Pass",method="DELETE"),  
    service_olt(1, {"nodeId":None, "slotId":1,"shelfId":1, "servicePortId": 1, "onuId": 1, "portId": 3},result="Pass",method="DELETE"),  
)

def OLT_Service(rest_interface_module, node_id, service_olt_data=service_olt(), method='ADD'):
    method = service_olt_data.method
    logger.info(f'SERVICE OLT TEST DATA ------- > {service_olt_data.index}')
    expected_set = service_olt_data.expected_result_Set
    expected_set["nodeId"]= node_id
    expected_get = service_olt_data.expected_result_Get  

    logger.info(f"TRY TO {method} SERVICE OLT CONFIG ...")
    if method == 'ADD':
        url = "/api/gponconfig/service/add"
        response = rest_interface_module.post_request(url, expected_set)    
    else:  # method==DELETE   
        url = f"/api/gponconfig/service/delete/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["servicePortId"])
        response = rest_interface_module.delete_request(url)

    if service_olt_data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in SERVICE OLT config {expected_set}'
        if response.status_code != 200:
            logger.error(response.message)
        #**********************************************************************
        if len(expected_get.keys()) !=0:
            logger.info(f' GETTING SERVICE OLT (after {method} method) ... ')
            read_data = rest_interface_module.get_request(f"/api/gponconfig/service/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["servicePortId"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"{method} IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
            logger.info(f'check is completed in {method} method')

    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in SERVICE OLT {service_data._asdict}'
        if len(expected_get.keys()) !=0:
            read_data = rest_interface_module.get_request(f"/api/gponconfig/service/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["servicePortId"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"set steeep IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)





def test_OLT_Service(rest_interface_module, node_id):
    bridge_config(rest_interface_module, node_id, Bridge_conf(), method='POST')
    # ****************************************************************************************************************************
    for vlan in VLAN_DATA_conf_CUSTOM:
        vlan_config(rest_interface_module, node_id, vlan, method='POST')  

    for dba in dba_profile_Data_Config:
        DBA_Profile(rest_interface_module, node_id, dba, method='ADD')
 
    for tcont in tcont_Data_Config:
        Tcont_Management(rest_interface_module, node_id, tcont)
    
    for gem in gem_profile_Data_Config:
        Gem_Management(rest_interface_module, node_id, gem)

    for serviceolt in service_olt_Data:
        OLT_Service_Profile(rest_interface_module, node_id, serviceolt)

    for serviceolt in service_olt_Data_Delete:
        OLT_Service_Profile(rest_interface_module, node_id, serviceolt)

    for gem in gem_profile_Data_Delete_Config:
        Gem_Management(rest_interface_module, node_id, gem)

    for tcont in tcont_Data_Delete_Config:
        Tcont_Management(rest_interface_module, node_id, tcont)

    for dba in dba_profile_Data_Config_Delete:
        DBA_Profile(rest_interface_module, node_id, dba, method='DELETE')       

    for vlan in VLAN_DATA_conf_CUSTOM:
        vlan_config(rest_interface_module, node_id, vlan, method='DELETE')  
    #****************************************************************************************************************************
    bridge_config(rest_interface_module, node_id, Bridge_conf(), method='DELETE')    