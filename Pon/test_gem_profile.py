import pytest
import logging
import json
from config import *
from conftest import *

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)

gem_profile = namedtuple('gem_profile', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
gem_profile.__new__.__defaults__ = (None, {}, {},None)


gem_profile_Data = [


    {"gemId": "6","name": "gem6","onuId": 1,"portId": 1,"tcontId": 6,"tcontName": "tcont_valid6","result": "Pass"},
    {"gemId": "28","name": "gem28","onuId": 1,"portId": 1,"tcontId": 4,"tcontName": "tcont_valid4","result": "Pass"},
    {"gemId": "29","name": "gem29","onuId": 1,"portId": 1,"tcontId": 2,"tcontName": "tcont_valid2","result": "Pass"},
    {"gemId": "30","name": "gem30","onuId": 1,"portId": 1,"tcontId": 8,"tcontName": "tcont_valid8","result": "Pass"},
    {"gemId": "15","name": "gem_invalid_tcont","onuId": 1,"portId": 1,"tcontId": 3,"tcontName": "tcont_invalid","result": "Fail"},
    ]

gem_profile_Data = (
gem_profile(1, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"1","name": "gem1", "onuId": 1, "portId": 1, "tcontId": 8, "tcontName": "tcont_valid8"},
                                                           {
                                                            "gemid": ["1", "gemId"],
                                                            "name": ["gem1", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [1, "portId"],
                                                            "tcontId": [8, "tcontId"],                                                            
                                                            "tcontname": ["tcont_valid8", "tcontName"],},result="Pass",method="ADD"),  
gem_profile(2, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"2","name": "gem2", "onuId": 1, "portId": 1, "tcontId": 6, "tcontName": "tcont_valid6"},
                                                           {
                                                            "gemid": ["2", "gemId"],
                                                            "name": ["gem2", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [1, "portId"],
                                                            "tcontId": [6, "tcontId"],                                                            
                                                            "tcontname": ["tcont_valid6", "tcontName"],},result="Pass",method="ADD"),  
gem_profile(3, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"3","name": "gem3", "onuId": 1, "portId": 1, "tcontId": 4, "tcontName": "tcont_valid4"},
                                                           {
                                                            "gemid": ["3", "gemId"],
                                                            "name": ["gem4", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [1, "portId"],
                                                            "tcontId": [4, "tcontId"],                                                            
                                                            "tcontname": ["tcont_valid4", "tcontName"],},result="Pass",method="ADD"),  
gem_profile(4, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"4","name": "gem4", "onuId": 1, "portId": 1, "tcontId": 2, "tcontName": "tcont_valid2"},
                                                           {
                                                            "gemid": ["4", "gemId"],
                                                            "name": ["gem4", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [1, "portId"],
                                                            "tcontId": [2, "tcontId"],                                                            
                                                            "tcontname": ["tcont_valid2", "tcontName"],},result="Pass",method="ADD"),  

gem_profile(5, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"5","name": "gem5", "onuId": 1, "portId": 1, "tcontId": 8, "tcontName": "tcont_valid8"},
                                                           {
                                                            "gemid": ["5", "gemId"],
                                                            "name": ["gem5", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [1, "portId"],
                                                            "tcontId": [8, "tcontId"],                                                            
                                                            "tcontname": ["tcont_valid8", "tcontName"],},result="Pass",method="ADD"),  
gem_profile(6, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"6","name": "gem6", "onuId": 1, "portId": 1, "tcontId": 3, "tcontName": "tcont_valid8"},
                                                           {
                                                            "gemid": ["5", "gemId"],
                                                            "name": ["gem5", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [1, "portId"],
                                                            "tcontId": [8, "tcontId"],                                                            
                                                            "tcontname": ["tcont_valid8", "tcontName"],},result="Fail",method="ADD"),  

gem_profile(7, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"1","name": "gem1", "onuId": 1, "portId": 1, "tcontId": 6, "tcontName": "tcont_valid6"},
                                                           {
                                                            "gemid": ["1", "gemId"],
                                                            "name": ["gem1", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [1, "portId"],
                                                            "tcontId": [6, "tcontId"],                                                            
                                                            "tcontname": ["tcont_valid6", "tcontName"],},result="Pass",method="ADD"), 

)


def Gem_Management(rest_interface_module, node_id, gem_data=gem_profile(), method='ADD'):
    method = gem_data.method
    logger.info(f'TCONT MANAGEMENT TEST DATA ------- > {gem_data.index}')
    expected_set = gem_data.expected_result_Set
    expected_set["nodeId"]= int(node_id)
    expected_get = gem_data.expected_result_Get  

    logger.info(f"TRY TO {method} Qos_Policy CONFIG ...")
    if method == 'ADD':
        url = "/api/gponconfig/tcont/add"
        response = rest_interface_module.post_request(url, expected_set) 
    elif method == "UPDATE":
        url = "/api/gponconfig/sp5100/tcont/update"
        response = rest_interface_module.post_request(url, expected_set)     
    else:  # method==DELETE   
        url = f"/api/gponconfig/tcont/delete/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["tcontId"])
        response = rest_interface_module.delete_request(url)

    if tcont_data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in PROFILE DBA config {expected_set}'
        if response.status_code != 200:
            logger.error(response.message)
        logger.info(f' GETTING Qos_Policy-config (after {method} method) ... ')
        read_data = rest_interface_module.get_request(f"/api/gponconfig/tcont/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["tcontId"]))
        input_data = json.loads(read_data.text)
        #**********************************************************************
        if method == 'ADD' or 'DELETE' or "UPDATE": 
            for key in expected_get.keys():
                logger.info(f"{method} IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
            logger.info(f'check is completed in {method} method')

    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in TCONT MANAGE {data._asdict}'
        if len(expected_get.keys()) !=0:
            read_data = rest_interface_module.get_request(f"/api/gponconfig/tcont/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["tcontId"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"set steeep IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)





def test_Tcont_Management(rest_interface_module, node_id):

    for dba in dba_profile_Data_Config:
        DBA_Profile(rest_interface_module, node_id, dba, method='ADD')
 
    for tcont in tcont_Data:
        Tcont_Management(rest_interface_module, node_id, tcont)
    for tcont in tcont_Data_Delete:
        Tcont_Management(rest_interface_module, node_id, tcont)

    for dba in dba_profile_Data_Config_Delete:
        DBA_Profil(rest_interface_module, node_id, dba, method='DELETE')       