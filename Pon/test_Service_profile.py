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

service_profile = namedtuple('service_profile', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
service_profile.__new__.__defaults__ = (None, {}, {},None, None)

service_profile_Data = (
service_profile(1, {"nodeId":None, "slotId":1,"shelfId":1, "servicePortId": 3, "onuId": 1, "portId": 1, "gemId": 1, "userVlan": 10},
                                                           {
                                                            "gemId": [1, "gemId"],
                                                            "servicePortId": [3, "servicePortId"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [1, "portId"],
                                                            "userVlan": [10, "userVlan"],},result="Pass",method="ADD"),  
)                                                       
service_profile_Data_Delete = (
    service_profile(1, {"nodeId":None, "slotId":1,"shelfId":1, "servicePortId": 3, "onuId": 1, "portId": 1},result="Pass",method="DELETE"),  

)

def Service_Profile(rest_interface_module, node_id, service_data=service_profile(), method='ADD'):
    method = service_data.method
    logger.info(f'SERVICE PROFILE TEST DATA ------- > {service_data.index}')
    expected_set = service_data.expected_result_Set
    expected_set["nodeId"]= int(node_id)
    expected_get = service_data.expected_result_Get  

    logger.info(f"TRY TO {method} SERVICE PROFILE CONFIG ...")
    if method == 'ADD':
        url = "/api/gponconfig/service/add"
        response = rest_interface_module.post_request(url, expected_set)    
    else:  # method==DELETE   
        url = f"/api/gponconfig/service/delete/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["serviceId"])
        response = rest_interface_module.delete_request(url)

    if service_data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in PROFILE DBA config {expected_set}'
        if response.status_code != 200:
            logger.error(response.message)
        logger.info(f' GETTING Gem_Management (after {method} method) ... ')
        read_data = rest_interface_module.get_request(f"/api/gponconfig/service/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["serviceId"]))
        input_data = json.loads(read_data.text)
        #**********************************************************************
        if method == 'ADD' or 'DELETE': 
            for key in expected_get.keys():
                logger.info(f"{method} IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
            logger.info(f'check is completed in {method} method')

    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in SERVICE PROFILE {service_data._asdict}'
        if len(expected_get.keys()) !=0:
            read_data = rest_interface_module.get_request(f"/api/gponconfig/service/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["serviceId"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"set steeep IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)





def test_Service_Profile(rest_interface_module, node_id):
    bridge_config(rest_interface_module, node_id, Bridge_conf(), method='POST')
    # ****************************************************************************************************************************
    for vlan in VLAN_DATA_conf_CUSTOM:
        vlan_config(rest_interface_module, node_id, vlan, method='POST')  

    # for dba in dba_profile_Data_Config:
    #     DBA_Profile(rest_interface_module, node_id, dba, method='ADD')
 
    # for tcont in tcont_Data_Config:
    #     Tcont_Management(rest_interface_module, node_id, tcont)
    
    # for gem in gem_profile_Data_Config:
    #     Gem_Management(rest_interface_module, node_id, gem)

    for service in service_profile_Data:
        Service_Profile(rest_interface_module, node_id, service)

    for service in service_profile_Data_Delete:
        Service_Profile(rest_interface_module, node_id, service)
    # for gem in gem_profile_Data_Delete_Config:
    #     Gem_Management(rest_interface_module, node_id, gem)

    # for tcont in tcont_Data_Delete_Config:
    #     Tcont_Management(rest_interface_module, node_id, tcont)

    # for dba in dba_profile_Data_Delete_Config:
    #     DBA_Profil(rest_interface_module, node_id, dba, method='DELETE')  
    # 
    for port in range(1,3):
        switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port,index=9), method='POST')
 
    for vlan in VLAN_DATA_conf_CUSTOM:
        vlan_config(rest_interface_module, node_id, vlan, method='DELETE')
    #****************************************************************************************************************************
    bridge_config(rest_interface_module, node_id, Bridge_conf(), method='DELETE')    