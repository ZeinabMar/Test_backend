import pytest
import logging
import json
from config import *
from conftest import *
from Pon.test_tcont_profile import Tcont_Management
from Pon.test_dba_profile import DBA_Profile
from Pon.test_Service_Profile_Definition import Service_Profile_Definition


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)

Tcont_service_profile = namedtuple('Tcont_service_profile', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
Tcont_service_profile.__new__.__defaults__ = (None, {}, {},None, None)

Tcont_service_profile_Data = (
Tcont_service_profile(1, {
    "id": None,"tcontId": "1","nodeId": None,"shelfId": 1,"slotId": 1,"onuId": 1,"name": "test_tcont1",
    "bwProfileName": "dba_type1","bwProfileId": 1,"bwProfileShow": "dba_type1(1)",}, {"name": ["test_tcont1", "name"],
                                                                                                "bwProfileName": ["dba_type1", "bwProfileName"],
                                                                                                "bwProfileId": [1, "bwProfileId"],
                                                                                                "onuId": [1, "onuId"]},result="Pass",method="ADD"),
Tcont_service_profile(2, {
    "id": None,"tcontId": "1","nodeId": None,"shelfId": 1,"slotId": 1,"onuId": 2,"name": "test_tcont1",
    "bwProfileName": "dba_type1","bwProfileId": 1,"bwProfileShow": "dba_type1(1)",}, {"name": ["test_tcont1", "name"],
                                                                                                "bwProfileName": ["dba_type1", "bwProfileName"],
                                                                                                "bwProfileId": [1, "bwProfileId"],
                                                                                                "onuId": [2, "onuId"]},result="Pass",method="ADD"),

)  

Tcont_service_profile_Delete = (
    Tcont_service_profile(1, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 1, "tcontId": 1},result="Pass",method="DELETE"), 
    Tcont_service_profile(1, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 2, "tcontId": 1},result="Pass",method="DELETE"), 
)

def Tcont_Service_Profile(rest_interface_module, node_id, tcont_service_profile_data=Tcont_service_profile(), method='ADD'):
    method = tcont_service_profile_data.method
    logger.info(f'SERVICE TCONT TEST DATA ------- > {tcont_service_profile_data.index}')
    expected_set = tcont_service_profile_data.expected_result_Set
    expected_set["nodeId"]= int(node_id)
    expected_get = tcont_service_profile_data.expected_result_Get  

    logger.info(f"TRY TO {method} SERVICE TCONT PROFILE CONFIG ...")
    if method == 'ADD':
        url = "/api/gponconfig/tcontserviceprofile/add"
        response = rest_interface_module.post_request(url, expected_set)    
    else:  # method==DELETE   
        url = f"/api/gponconfig/tcontserviceprofile/delete/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["tcontId"])
        response = rest_interface_module.delete_request(url)

    if tcont_service_profile_data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in SERVICE TCONT PROFILE {expected_set}'
        if response.status_code != 200:
            logger.error(response.message)
        #**********************************************************************
        if len(expected_get.keys()) !=0:
            logger.info(f' GETTING SERVICE TCONT (after {method} method) ... ')
            read_data = rest_interface_module.get_request(f"/api/gponconfig/tcontserviceprofile/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["tcontId"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"{method} IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
            logger.info(f'check is completed in {method} method')

    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in SERVICE TCONT PROFILE {service_data._asdict}'
        if len(expected_get.keys()) !=0:
            read_data = rest_interface_module.get_request(f"/api/gponconfig/tcontserviceprofile/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["tcontId"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"set steeep IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)





def test_Tcont_Service_Profile(rest_interface_module, node_id):

    for dba in dba_profile_Data_Config:
        DBA_Profile(rest_interface_module, node_id, dba, method='ADD')
    for service_def in Onu_Service_Profile_Data_Config:
        Service_Profile_Definition(rest_interface_module, node_id, service_def, method='ADD')

    for service_tcont in Tcont_service_profile_Data:
        Tcont_Service_Profile(rest_interface_module, node_id, service_tcont)

    for service_tcont in Tcont_service_profile_Delete:
        Tcont_Service_Profile(rest_interface_module, node_id, service_tcont)

    for service_def in Onu_Service_Profile_Delete_Config:
        Service_Profile_Definition(rest_interface_module, node_id, service_def, method='DELETE')    

    for dba in dba_profile_Data_Config_Delete:
        DBA_Profile(rest_interface_module, node_id, dba, method='DELETE')       
