import pytest
import logging
import json
from config import *
from conftest import *


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)

dba_profile = namedtuple('dba_profile', ['index', 'expected_result_Set', 'expected_result_Get', "result"])                                       
dba_profile.__new__.__defaults__ = (None, {}, {},None)

dba_profile_Data = (


dba_profile(1, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":1,"name": "dba_test1", "dbaType": 1, "fixedBwValue": 32000, "assureBwValue": None, "maxBwValue": None},
                                                           {
                                                            "name": ["dba_test1", "name"],
                                                            "dbatype": [1, "dbaType"],
                                                            "fixedbwvalue": [32000, "fixedBwValue"],
                                                            "assurebwvalue": [32250, "assureBwValue"],
                                                            "maxbwvalue": [32500, "maxBwValue"]},result="Pass"),  

dba_profile(2, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":2,"name": "dba_test2", "dbaType": 1, "fixedBwValue": 32000, "assureBwValue": None, "maxBwValue": None,}, 
                                                          {
                                                            "name": ["dba_test2", "name"],
                                                            "dbaType": [1, "dbaType"],
                                                            "fixedBwValue": [32000, "fixedBwValue"],
                                                            "assureBwValue": [32250, "assureBwValue"],
                                                            "maxBwValue": [32500, "maxBwValue"]},result="Pass"), 

dba_profile(3, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":3,"name": "dba_test3", "dbaType": 3, "fixedBwValue": None, "assureBwValue": 500, "maxBwValue": None,},result="Fail"),

dba_profile(4, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":3,"name": "dba_test3", "dbaType": 3, "fixedBwValue": 250, "assureBwValue": 500, "maxBwValue": 750,}, 
                                                          {
                                                            "name": ["dba_test3", "name"],
                                                            "dbaType": [3, "dbaType"],
                                                            "fixedBwValue": [0, "fixedBwValue"],
                                                            "assureBwValue": [500, "assureBwValue"],
                                                            "maxBwValue": [750, "maxBwValue"]},result="Pass"),

dba_profile(5, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":4,"name": "dba_test4", "dbaType": 4, "fixedBwValue": None, "assureBwValue": 128000, "maxBwValue": None,}, result="Fail"),
dba_profile(6, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":4,"name": "dba_test4", "dbaType": 4, "fixedBwValue": None, "assureBwValue": None, "maxBwValue": 50000}, 
                                                         {
                                                            "name": ["dba_test4", "name"],
                                                            "dbaType": [4, "dbaType"],
                                                            "fixedBwValue": [0, "fixedBwValue"],
                                                            "assureBwValue": [250, "assureBwValue"],
                                                            "maxBwValue": [50000, "maxBwValue"]},result="Pass"), 

dba_profile(7, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":5,"name": "dba_test5", "dbaType": 5, "fixedBwValue": None, "assureBwValue": 25000, "maxBwValue": None,}, result="Fail"),
dba_profile(8, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":5,"name": "dba_test5", "dbaType": 5, "fixedBwValue": None, "assureBwValue": None, "maxBwValue": 25000,}, result="Fail"),
dba_profile(9, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":5,"name": "dba_test5_1", "dbaType": 5, "fixedBwValue": 250, "assureBwValue": 500, "maxBwValue": 1000,}, 
                                                            {"dbaId": [5, "dbaId"],
                                                            "name": ["dba_test5_1", "name"],
                                                            "dbaType": [5, "dbaType"],
                                                            "fixedBwValue": [250, "fixedBwValue"],
                                                            "assureBwValue": [500, "assureBwValue"],
                                                            "maxBwValue": [1000, "maxBwValue"]},result="Pass"),  

dba_profile(10, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":5,"name": "dba_test5_2", "dbaType": 5, "fixedBwValue": 250, "assureBwValue": 500, "maxBwValue": 1000,}, 
                                                            {
                                                            "dbaId": [6, "dbaId"],
                                                            "name": ["dba_test5_2", "name"],
                                                            "dbaType": [5, "dbaType"],
                                                            "fixedBwValue": [250, "fixedBwValue"],
                                                            "assureBwValue": [500, "assureBwValue"],
                                                            "maxBwValue": [1000, "maxBwValue"]},result="Pass"), 

dba_profile(11, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":7,"name": "dba_test5_2", "dbaType": 5, "fixedBwValue": 250, "assureBwValue": 500, "maxBwValue": 25000,}, result="Fail"),
dba_profile(12, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":6,"name": "dba_test5_2", "dbaType": 5, "fixedBwValue": 250, "assureBwValue": 1000, "maxBwValue": 1250,}, 
                                                            {"dbaId": [6, "dbaId"],
                                                            "name": ["dba_test5_2", "name"],
                                                            "dbaType": [5, "dbaType"],
                                                            "fixedBwValue": [250, "fixedBwValue"],
                                                            "assureBwValue": [500, "assureBwValue"],
                                                            "maxBwValue": [1000, "maxBwValue"]},result="Fail"), 
               
)


def DBA_Profile(rest_interface_module, node_id, dba_profile_data=dba_profile(), method='ADD'):
    logger.info(f'PROFILE DBA TEST DATA ------- > {dba_profile_data.index}')
    expected_set = dba_profile_data.expected_result_Set
    expected_set["nodeId"]= node_id
    expected_get = dba_profile_data.expected_result_Get  

    logger.info(f"TRY TO {method} Qos_Policy CONFIG ...")
    if method == 'ADD':
        url = "/api/gponconfig/dbaProfile/add"
        response = rest_interface_module.post_request(url, expected_set) 
    else:  # method==DELETE
        url = f"/api/gponconfig/dbaProfile/delete/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["dbaId"])
        response = rest_interface_module.delete_request(url)


    if dba_profile_data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in DBA_Profile config {expected_set}'
        if response.status_code != 200:
            logger.error(response.message)
        logger.info(f' GETTING Gem_Management (after {method} method) ... ')

        read_data = rest_interface_module.get_request(f"/api/gponconfig/dbaProfile/getall?nodeId="+str(expected_set["nodeId"])+"&shelfId="+str(expected_set["shelfId"])+"&slotId="+str(expected_set["slotId"]))
        input_data_getall = json.loads(read_data.text)
        input_data = find_in_getall(input_data_getall, "name", expected_get["name"][0])
        if method == 'ADD' or 'DELETE': 
            for key in expected_get.keys():
                logger.info(f"{method} IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
            logger.info(f'check is completed in {method} method')
    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in GEM MANAGE {expected_set}'
        if len(expected_get.keys()) !=0:
            read_data = rest_interface_module.get_request(f"/api/gponconfig/dbaProfile/getall?nodeId="+str(expected_set["nodeId"])+"&shelfId="+str(expected_set["shelfId"])+"&slotId="+str(expected_set["slotId"]))
            input_data_getall = json.loads(read_data.text)
            input_data = find_in_getall(input_data_getall, "name")
            for key in expected_get.keys():
                logger.info(f"set steeep IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)



def test_DBA_Profile(rest_interface_module, node_id):
    for dba in dba_profile_Data:
        DBA_Profile(rest_interface_module, node_id, dba, method='ADD')
    # for dba in dba_profile_Data:
    #     DBA_Profil(rest_interface_module, node_id, dba, method='DELETE')    
