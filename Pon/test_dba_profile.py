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


dba_profile(1, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":1,"name": "dba_test12", "dbaType": 1, "fixedBwValue": 32000, "assureBwValue": None, "maxBwValue": None},
                                                           {
                                                            "namedba": ["dba_test12", "name"],
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


dba_profile(3, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":3,"name": "dba_test3", "dbaType": 3, "fixedBwValue": None, "assureBwValue": 128000, "maxBwValue": None,}, 
                                                          {
                                                            "name": ["dba_test3", "name"],
                                                            "dbaType": [3, "dbaType"],
                                                            "fixedBwValue": [None, "fixedBwValue"],
                                                            "assureBwValue": [128000, "assureBwValue"],
                                                            "maxBwValue": [None, "maxBwValue"]},result="Pass"),

dba_profile(4, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":4,"name": "dba_test3", "dbaType": 4, "fixedBwValue": None, "assureBwValue": 128000, "maxBwValue": None,}, 
                                                          {
                                                            "name": ["dba_test3", "name"],
                                                            "dbaType": [3, "dbaType"],
                                                            "fixedBwValue": [None, "fixedBwValue"],
                                                            "assureBwValue": [128000, "assureBwValue"],
                                                            "maxBwValue": [None, "maxBwValue"]},result="Fail"),
# dba_profile(4, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":3,"name": "dba_test3", "dbaType": 2, "fixedBwValue": None, "assureBwValue": 256000, "maxBwValue": 512000}, 
#                                                          {
#                                                             "name": ["dba_test3", "name"],
#                                                             "dbaType": [2, "dbaType"],
#                                                             "fixedBwValue": [None, "fixedBwValue"],
#                                                             "assureBwValue": [256000, "assureBwValue"],
#                                                             "maxBwValue": [512000, "maxBwValue"]},result="Pass"), 

# dba_profile(5, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":5,"name": "dba_test5-1", "dbaType": 5, "fixedBwValue": 250, "assureBwValue": 500, "maxBwValue": 1000,}, 
#                                                             {"dbaId": [5, "dbaId"],
#                                                             "name": ["dba_test5", "name"],
#                                                             "dbaType": [5, "dbaType"],
#                                                             "fixedBwValue": [250, "fixedBwValue"],
#                                                             "assureBwValue": [500, "assureBwValue"],
#                                                             "maxBwValue": [1000, "maxBwValue"]},result="Pass"),  

# dba_profile(6, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":6,"name": "dba_test5-2", "dbaType": 5, "fixedBwValue": 6000, "assureBwValue": 14000, "maxBwValue": 22000,}, 
#                                                             {"dbaId": [5, "dbaId"],
#                                                             "name": ["dba_test1", "name"],
#                                                             "dbaType": [5, "dbaType"],
#                                                             "fixedBwValue": [6000, "fixedBwValue"],
#                                                             "assureBwValue": [14000, "assureBwValue"],
#                                                             "maxBwValue": [22000, "maxBwValue"]},result="Pass"),  

# dba_profile(7, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":7,"name": "dba_test5-3", "dbaType": 5, "fixedBwValue": 750000, "assureBwValue": 1000000, "maxBwValue": 1200000,}, 
#                                                           {"dbaId": [7, "dbaId"],
#                                                             "name": ["dba_test5-3", "name"],
#                                                             "dbaType": [5, "dbaType"],
#                                                             "fixedBwValue": [750000, "fixedBwValue"],
#                                                             "assureBwValue": [1000000, "assureBwValue"],
#                                                             "maxBwValue": [1200000, "maxBwValue"]},result="Pass"),  

# dba_profile(8, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":8,"name": "dba_test5-4", "dbaType": 5, "fixedBwValue": 750000, "assureBwValue": 500000, "maxBwValue": 1200000,}, 
#                                                           {"dbaId": [8, "dbaId"],
#                                                             "name": ["dba_test5-4", "name"],
#                                                             "dbaType": [5, "dbaType"],
#                                                             "fixedBwValue": [750000, "fixedBwValue"],
#                                                             "assureBwValue": [500000, "assureBwValue"],
#                                                             "maxBwValue": [1200000, "maxBwValue"]},result="Fail"),  
# dba_profile(9, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":9,"name": "dba_test5-5", "dbaType": 5, "fixedBwValue": 900000, "assureBwValue": 1000000, "maxBwValue": 1200000,}, 
#                                                          {"dbaId": [9, "dbaId"],
#                                                             "name": ["dba_test5-5", "name"],
#                                                             "dbaType": [5, "dbaType"],
#                                                             "fixedBwValue": [900000, "fixedBwValue"],
#                                                             "assureBwValue": [1000000, "assureBwValue"],
#                                                             "maxBwValue": [1200000, "maxBwValue"]},result="Fail"),                  
)


def DBA_Profile(rest_interface_module, node_id, dba_profile_data=dba_profile(), method='ADD'):
    logger.info(f'PROFILE DBA TEST DATA ------- > {dba_profile_data.index}')
    expected_set = dba_profile_data.expected_result_Set
    expected_set["nodeId"]= int(node_id)
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

        read_data = rest_interface_module.get_request(f"/api/gponconfig/dbaProfile/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["dbaId"]))
        input_data = json.loads(read_data.text)
        #**********************************************************************
        if method == 'ADD' or 'DELETE': 
            for key in expected_get.keys():
                logger.info(f"{method} IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
            logger.info(f'check is completed in {method} method')
    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in GEM MANAGE {gem_data._asdict}'
        if len(expected_get.keys()) !=0:
            read_data = rest_interface_module.get_request(f"/api/gponconfig/dbaProfile/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["dbaId"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"set steeep IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)



def test_DBA_Profile(rest_interface_module, node_id):

    for dba in dba_profile_Data:
        DBA_Profile(rest_interface_module, node_id, dba, method='ADD')
    # for dba in dba_profile_Data:
    #     DBA_Profil(rest_interface_module, node_id, dba, method='DELETE')    
