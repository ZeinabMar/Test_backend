import pytest
import logging
import json
from config import *
from conftest import *
from Pon.test_tcont_profile import Tcont_Management
from Pon.test_dba_profile import DBA_Profile


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)

gem_profile = namedtuple('gem_profile', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
gem_profile.__new__.__defaults__ = (None, {}, {},None, None)

gem_profile_Data = (
gem_profile(1, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"1","name": "gem1", "onuId": 1, "portId": 2, "tcontId": 8},
                                                           {
                                                            "gemid": [1, "gemId"],
                                                            "name": ["gem1", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [2, "portId"],
                                                            "tcontId": [8, "tcontId"]},result="Pass",method="ADD"),  
gem_profile(2, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"2","name": "gem2", "onuId": 1, "portId": 2, "tcontId": 6},
                                                           {
                                                            "gemid": [2, "gemId"],
                                                            "name": ["gem2", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [2, "portId"],
                                                            "tcontId": [6, "tcontId"]},result="Pass",method="ADD"),
# gem_profile(3, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"2","name": "gem2", "onuId": 2, "portId": 2, "tcontId": 6},
#                                                            {
#                                                             "gemid": [2, "gemId"],
#                                                             "name": ["gem2", "name"],
#                                                             "onuId": [2, "onuId"],
#                                                             "portId": [2, "portId"],
#                                                             "tcontId": [6, "tcontId"]},result="Pass",method="ADD"),
gem_profile(4, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"1","name": "gem1", "onuId": 1, "portId": 3, "tcontId": 8},
                                                           {
                                                            "gemid": [1, "gemId"],
                                                            "name": ["gem1", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [3, "portId"],
                                                            "tcontId": [8, "tcontId"]},result="Pass",method="ADD"),                                                            

gem_profile(5, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"5","name": "gem1", "onuId": 1, "portId": 2, "tcontId": 8},
                                                           {
                                                            "gemid": [5, "gemId"],
                                                            "name": ["gem1", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [2, "portId"],
                                                            "tcontId": [8, "tcontId"]},result="Pass",method="ADD"),  
gem_profile(6, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"6","name": "gem6", "onuId": 1, "portId": 5, "tcontId": 3},result="Fail",method="ADD"),  #unavailable tcont

gem_profile(7, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"1","name": "gem1", "onuId": 1, "portId": 2, "tcontId": 6},
                                                           {
                                                            "gemid": [1, "gemId"],
                                                            "name": ["gem1", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [2, "portId"],
                                                            "tcontId": [8, "tcontId"]},result="Fail",method="ADD"), 
gem_profile(8, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"1","name": "gem2", "onuId": 1, "portId": 2, "tcontId": 8},
                                                           {
                                                            "gemid": [1, "gemId"],
                                                            "name": ["gem1", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [2, "portId"],
                                                            "tcontId": [8, "tcontId"]},result="Fail",method="ADD"),
)
gem_profile_Data_Delete = (
    gem_profile(1, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"1","name": "gem1", "onuId": 1, "portId": 2, "tcontId": 8},result="Pass",method="DELETE"), 
    gem_profile(2, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"2","name": "gem2", "onuId": 1, "portId": 2, "tcontId": 6},result="Pass",method="DELETE"), 
    gem_profile(4, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"5","name": "gem1", "onuId": 1, "portId": 2, "tcontId": 8},result="Pass",method="DELETE"), 
    # gem_profile(4, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"5","name": "gem1", "onuId": 1, "portId": 2, "tcontId": 8},result="Pass",method="DELETE"), 
    gem_profile(5, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"1","name": "gem1", "onuId": 1, "portId": 3, "tcontId": 8},result="Pass",method="DELETE"), 

)

def Gem_Management(rest_interface_module, node_id, gem_data=gem_profile(), method='ADD'):
    method = gem_data.method
    logger.info(f'GEM MANAGEMENT TEST DATA ------- > {gem_data.index}')
    expected_set = gem_data.expected_result_Set
    expected_set["nodeId"]= int(node_id)
    expected_get = gem_data.expected_result_Get  

    logger.info(f"TRY TO {method} Gem_Management CONFIG ...")
    if method == 'ADD':
        url = "/api/gponconfig/gem/add"
        response = rest_interface_module.post_request(url, expected_set)    
    else:  # method==DELETE   
        url = f"/api/gponconfig/gem/delete/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["gemId"])
        response = rest_interface_module.delete_request(url)

    if gem_data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in Gem_Management config {expected_set}'
        if response.status_code != 200:
            logger.error(response.message)
        #**********************************************************************
        if len(expected_get.keys()) !=0:
            logger.info(f' GETTING Gem_Management (after {method} method) ... ')
            read_data = rest_interface_module.get_request(f"/api/gponconfig/gem/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["gemId"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"{method} IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
            logger.info(f'check is completed in {method} method')
    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in GEM MANAGE {gem_data._asdict}'
        if len(expected_get.keys()) !=0:
            read_data = rest_interface_module.get_request(f"/api/gponconfig/gem/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["gemId"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"set steeep IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)





def test_Gem_Management(rest_interface_module, node_id):

    for dba in dba_profile_Data_Config:
        DBA_Profile(rest_interface_module, node_id, dba, method='ADD')
 
    for tcont in tcont_Data_Config:
        Tcont_Management(rest_interface_module, node_id, tcont)
    
    for gem in gem_profile_Data:
        Gem_Management(rest_interface_module, node_id, gem)

    for gem in gem_profile_Data_Delete:
        Gem_Management(rest_interface_module, node_id, gem)

    for tcont in tcont_Data_Delete_Config:
        Tcont_Management(rest_interface_module, node_id, tcont)

    for dba in dba_profile_Data_Config_Delete:
        DBA_Profile(rest_interface_module, node_id, dba, method='DELETE')       