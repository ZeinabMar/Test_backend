import pytest
import logging
import json
from config import *
from conftest import *


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)

Onu_Service_Profile = namedtuple('Onu_Service_Profile', ['index', 'expected_result_Set', 'expected_result_Get', "result"])                                       
Onu_Service_Profile.__new__.__defaults__ = (None, {}, {},None)

Onu_Service_Profile_Data = (

Onu_Service_Profile(1, {
    "nodeId": None,"shelfId": 1,"slotId": 1,"onuServiceProfileId": "1","onuServiceProfileName": None,"onuTypeProfileName": "Default"},
    {"onuserviceId": [1, "onuServiceProfileId"],"onuServiceProfileName": [None, "onuServiceProfileName"],"onuTypeProfileName": ["Default", "onuTypeProfileName"]},result="Pass"),  
Onu_Service_Profile(2, {
    "nodeId": None,"shelfId": 1,"slotId": 1,"onuServiceProfileId": "2","onuServiceProfileName": None,"onuTypeProfileName": "Default"},
    {"onuserviceId": [2, "onuServiceProfileId"], "onuServiceProfileName": [None, "onuServiceProfileName"], "onuTypeProfileName": ["Default", "onuTypeProfileName"]},result="Pass"),              
)


Onu_Service_Profile_Delete = (
    Onu_Service_Profile(1, {"nodeId":None, "slotId":1,"shelfId":1,"onuServiceProfileId":"1"}, result="Pass"),
    Onu_Service_Profile(2, {"nodeId":None, "slotId":1,"shelfId":1,"onuServiceProfileId":"2"}, result="Pass"),
)

def Service_Profile_Definition(rest_interface_module, node_id, Onu_Service=Onu_Service_Profile(), method='ADD'):
    logger.info(f'SERVICE PROFILE TEST DATA ------- > {Onu_Service.index}')
    expected_set = Onu_Service.expected_result_Set
    expected_set["nodeId"]= node_id
    expected_get = Onu_Service.expected_result_Get  

    logger.info(f"TRY TO {method} Qos_Policy CONFIG ...")
    if method == 'ADD': 
        url = "/api/gponconfig/onuserviceprofile/add"
        response = rest_interface_module.post_request(url, expected_set) 
    elif method == "DELETE":
        url = f"/api/gponconfig/onuserviceprofile/delete/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["onuServiceProfileId"])
        response = rest_interface_module.delete_request(url)

    if Onu_Service.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in  SERVICE Profile config {expected_set}'
        if response.status_code != 200:
            logger.error(response.message)
        if len(expected_get.keys()) !=0:
            logger.info(f' GETTING SERVICE PROFILE (after {method} method) ... ')
            read_data = rest_interface_module.get_request(f"/api/gponconfig/onuserviceprofile/getall?nodeId="+str(expected_set["nodeId"])+"&shelfId="+str(expected_set["shelfId"])+"&slotId="+str(expected_set["slotId"]))
            input_data_getall = json.loads(read_data.text)
            input_data = find_in_getall(input_data_getall, "onuServiceProfileId", expected_get["onuserviceId"][0])
            for key in expected_get.keys():
                logger.info(f"{method} IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
            logger.info(f'check is completed in {method} method')
    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in GEM MANAGE {expected_set}'
        if len(expected_get.keys()) !=0:
            logger.info(f' GETTING SERVICE PROFILE (after {method} method) ... ')
            read_data = rest_interface_module.get_request(f"/api/gponconfig/onuserviceprofile/getall?nodeId="+str(expected_set["nodeId"])+"&shelfId="+str(expected_set["shelfId"])+"&slotId="+str(expected_set["slotId"]))
            input_data_getall = json.loads(read_data.text)
            input_data = find_in_getall(input_data_getall, "onuServiceProfileId", expected_get["onuserviceId"][0])
            for key in expected_get.keys():
                logger.info(f"set steeep IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)



def test_Service_Profile_Definition(rest_interface_module, node_id):
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/onuserviceprofile/getall?nodeId={node_id}&shelfId=1&slotId=1")
    for service_def in Onu_Service_Profile_Data:
        Service_Profile_Definition(rest_interface_module, node_id, service_def, method='ADD')
    for service_def in Onu_Service_Profile_Delete:
        Service_Profile_Definition(rest_interface_module, node_id, service_def, method='DELETE')    
