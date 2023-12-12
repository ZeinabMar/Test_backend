import pytest
import logging
import json
from config import *
from conftest import *
from Pon.test_tcont_profile import Tcont_Management
from Pon.test_dba_profile import DBA_Profile
from Pon.test_Service_Profile_Definition import Service_Profile_Definition
from Pon.test_Service_Profile_Tcont import Tcont_Service_Profile


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)

Gem_service_profile = namedtuple('Gem_service_profile', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
Gem_service_profile.__new__.__defaults__ = (None, {}, {},None, None)

Gem_service_profile_Data = (
Gem_service_profile(1, { "gemId": "1", "tcontId": 1,"tcontName": "", "nodeId": None, "shelfId": 1,
                         "slotId": 1,"onuId": 1, "name": "test_gem1",}, {"tcontId": [1, "tcontId"],
                                                                         "name": ["test_gem1", "name"],
                                                                         "onuId": [1, "onuId"],
                                                                         "gemId": [1, "gemId"]},result="Pass",method="ADD"),
Gem_service_profile(2, { "gemId": "1", "tcontId": 1,"tcontName": "", "nodeId": None, "shelfId": 1,
                         "slotId": 1,"onuId": 2, "name": "test_gem1",}, {"tcontId": [1, "tcontId"],
                                                                         "name": ["test_gem1", "name"],
                                                                         "onuId": [2, "onuId"],
                                                                         "gemId": [1, "gemId"]},result="Pass",method="ADD"),

)  

Gem_service_profile_Delete = (
    Gem_service_profile(1, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 1, "gemId": 1},result="Pass",method="DELETE"), 
    Gem_service_profile(2, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 2, "gemId": 1},result="Pass",method="DELETE"), 
)

def Gem_Service_Profile(rest_interface_module, node_id, gem_service_profile_data=Gem_service_profile(), method='ADD'):
    method = gem_service_profile_data.method
    logger.info(f'SERVICE GEM TEST DATA ------- > {gem_service_profile_data.index}')
    expected_set = gem_service_profile_data.expected_result_Set
    expected_set["nodeId"]= int(node_id)
    expected_get = gem_service_profile_data.expected_result_Get  

    logger.info(f"TRY TO {method} SERVICE GEM PROFILE CONFIG ...")
    if method == 'ADD':
        url = "/api/gponconfig/gemserviceprofile/add"
        response = rest_interface_module.post_request(url, expected_set)    
    else:  # method==DELETE   
        url = f"/api/gponconfig/gemserviceprofile/delete/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["gemId"])
        response = rest_interface_module.delete_request(url)

    if gem_service_profile_data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in SERVICE GEM PROFILE {expected_set}'
        if response.status_code != 200:
            logger.error(response.message)
        #**********************************************************************
        if len(expected_get.keys()) !=0:
            logger.info(f' GETTING SERVICE GEM (after {method} method) ... ')
            read_data = rest_interface_module.get_request(f"/api/gponconfig/gemserviceprofile/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["gemId"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"{method} IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
            logger.info(f'check is completed in {method} method')

    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in SERVICE GEM PROFILE {service_data._asdict}'
        if len(expected_get.keys()) !=0:
            read_data = rest_interface_module.get_request(f"/api/gponconfig/gemserviceprofile/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["gemId"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"set steeep IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)



def test_Gem_Service_Profile(rest_interface_module, node_id):
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/dbaProfile/getall?nodeId={node_id}&shelfId=1&slotId=1")
    for dba in dba_profile_Data_Config:
        DBA_Profile(rest_interface_module, node_id, dba, method='ADD')
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/onuserviceprofile/getall?nodeId={node_id}&shelfId=1&slotId=1")
    for service_def in Onu_Service_Profile_Data_Config:
        Service_Profile_Definition(rest_interface_module, node_id, service_def, method='ADD')
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/tcontserviceprofile/getall?nodeId={node_id}&shelfId=1&slotId=1&onuServiceProfileId=-1")    
    for service_tcont in Tcont_service_profile_Data_Config:
        Tcont_Service_Profile(rest_interface_module, node_id, service_tcont)
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/gemserviceprofile/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=undefined&onuServiceProfileId=-1")    
    for service_gem in Gem_service_profile_Data:
        Gem_Service_Profile(rest_interface_module, node_id, service_gem)
    for service_gem in Gem_service_profile_Delete:
        Gem_Service_Profile(rest_interface_module, node_id, service_gem)
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/tcontserviceprofile/getall?nodeId={node_id}&shelfId=1&slotId=1&onuServiceProfileId=-1")    
    for service_tcont in Tcont_service_profile_Delete_Config:
        Tcont_Service_Profile(rest_interface_module, node_id, service_tcont)
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/onuserviceprofile/getall?nodeId={node_id}&shelfId=1&slotId=1")
    for service_def in Onu_Service_Profile_Delete_Config:
        Service_Profile_Definition(rest_interface_module, node_id, service_def, method='DELETE')    
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/dbaProfile/getall?nodeId={node_id}&shelfId=1&slotId=1")
    for dba in dba_profile_Data_Config_Delete:
        DBA_Profile(rest_interface_module, node_id, dba, method='DELETE')       
