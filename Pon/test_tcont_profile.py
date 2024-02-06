import pytest
import logging
import json
from config import *
from conftest import *
from Pon.test_dba_profile import DBA_Profile

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)

tcont = namedtuple('tcont', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
tcont.__new__.__defaults__ = (None, {}, {},None, None)

tcont_Data = (
tcont(1, {"nodeId":None, "slotId":1,"shelfId":1,"bwProfileId":1,"bwProfileName": "dba_type1", "name": "tcont_valid1", "onuId": 1, "portId": 2, "tcontId": 8},
                                                           {
                                                            "bwProfileId": [1, "bwProfileId"],
                                                            "bwProfileName": ["dba_type1", "bwProfileName"],
                                                            "name": ["tcont_valid1", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [2, "portId"],
                                                            "tcontId": [8, "tcontId"]},result="Pass",method="ADD"),  

tcont(2, {"nodeId":None, "slotId":1,"shelfId":1,"bwProfileId":2,"bwProfileName": "dba_type2", "name": "tcont_valid2", "onuId": 1, "portId": 2, "tcontId": 4},
                                                           {
                                                            "bwProfileId": [2, "bwProfileId"],
                                                            "bwProfileName": ["dba_type2", "bwProfileName"],
                                                            "name": ["tcont_valid2", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [2, "portId"],
                                                            "tcontId": [4, "tcontId"]},result="Pass", method="ADD"),   

tcont(3, {"nodeId":None, "slotId":1,"shelfId":1,"bwProfileId":3,"bwProfileName": "dba_type3", "name": "tcont_valid2", "onuId": 1, "portId": 2, "tcontId": 4},
                                                           {
                                                            "bwProfileId": [2, "bwProfileId"],
                                                            "bwProfileName": ["dba_type2", "bwProfileName"],
                                                            "name": ["tcont_valid2", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [2, "portId"],
                                                            "tcontId": [4, "tcontId"]},result="Fail", method="UPDATE"),  

tcont(4, {"nodeId":None, "slotId":1,"shelfId":1,"bwProfileId":2,"bwProfileName": "dba_type2", "name": "tcont_valid2", "onuId": 1, "portId": 2, "tcontId": 6},
                                                           {
                                                            "bwProfileId": [2, "bwProfileId"],
                                                            "bwProfileName": ["dba_type2", "bwProfileName"],
                                                            "name": ["tcont_valid2", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [2, "portId"],
                                                            "tcontId": [6, "tcontId"]},result="Pass", method="ADD"), 
# tcont(5, {"nodeId":None, "slotId":1,"shelfId":1,"bwProfileId":2,"bwProfileName": "dba_type2", "name": "tcont_valid2", "onuId": 2, "portId": 2, "tcontId": 6},
#                                                            {
#                                                             "bwProfileId": [2, "bwProfileId"],
#                                                             "bwProfileName": ["dba_type2", "bwProfileName"],
#                                                             "name": ["tcont_valid2", "name"],
#                                                             "onuId": [2, "onuId"],
#                                                             "portId": [2, "portId"],
#                                                             "tcontId": [6, "tcontId"]},result="Pass", method="ADD"),  
tcont(6, {"nodeId":None, "slotId":1,"shelfId":1,"bwProfileId":1,"bwProfileName": "dba_type1", "name": "tcont_valid1", "onuId": 1, "portId": 3, "tcontId": 8},
                                                           {
                                                            "bwProfileId": [1, "bwProfileId"],
                                                            "bwProfileName": ["dba_type1", "bwProfileName"],
                                                            "name": ["tcont_valid1", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [3, "portId"],
                                                            "tcontId": [8, "tcontId"]},result="Pass",method="ADD"), 
tcont(7, {"nodeId":None, "slotId":1,"shelfId":1,"bwProfileId":1,"bwProfileName": "dba_type1", "name": "tcont_disable_pon", "onuId": 1, "portId": 5, "tcontId": 6},result="Fail", method="UPDATE"), 
)

tcont_Data_Delete = (
   tcont(1, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 1, "portId": 2, "tcontId": 4},result="Pass", method="DELETE"), 
   tcont(2, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 1, "portId": 2, "tcontId": 6},result="Pass", method="DELETE"), 
   tcont(3, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 1, "portId": 2, "tcontId": 8},result="Pass", method="DELETE"), 
#    tcont(4, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 2, "portId": 2, "tcontId": 6},result="Pass", method="DELETE"), 
   tcont(5, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 1, "portId": 3, "tcontId": 8},result="Pass", method="DELETE"), 
)

def Tcont_Management(rest_interface_module, node_id, tcont_data=tcont(), method='ADD'):
    method = tcont_data.method
    logger.info(f'TCONT MANAGEMENT TEST DATA ------- > {tcont_data.index}')
    expected_set = tcont_data.expected_result_Set
    expected_set["nodeId"]= node_id
    expected_get = tcont_data.expected_result_Get  

    logger.info(f"TRY TO {method} TCONT MANAGEMENT CONFIG ...")
    if method == 'ADD':
        url = "/api/gponconfig/tcont/add"
        response = rest_interface_module.post_request(url, expected_set) 
    elif method == "UPDATE":
        url = "/api/gponconfig/tcont/update"
        response = rest_interface_module.post_request(url, expected_set)     
    elif method=="DELETE":   
        url = f"/api/gponconfig/tcont/delete/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["tcontId"])
        response = rest_interface_module.delete_request(url)

    if tcont_data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in TCONT MANAGEMENT config {expected_set}'
        if response.status_code != 200:
            logger.error(response.message)

        if len(expected_get.keys()) !=0: 
            logger.info(f' GETTING TCONT MANAGEMENT (after {method} method) ... ')
            read_data = rest_interface_module.get_request(f"/api/gponconfig/tcont/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["tcontId"]))
            input_data = json.loads(read_data.text)
            #**********************************************************************
            for key in expected_get.keys():
                logger.info(f"{method} IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
            logger.info(f'check is completed in {method} method')

    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in TCONT MANAGE {tcont_data._asdict}'
        if len(expected_get.keys()) !=0:
            read_data = rest_interface_module.get_request(f"/api/gponconfig/tcont/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["tcontId"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"set steeep IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)





def test_Tcont_Management(rest_interface_module, node_id):
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/dbaProfile/getall?nodeId={node_id}&shelfId=1&slotId=1")
    for dba in dba_profile_Data_Config:
        DBA_Profile(rest_interface_module, node_id, dba, method='ADD')
    for tcont in tcont_Data:
        response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/tcont/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=2&onuId=-1")
        response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/tcont/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=3&onuId=-1")
        Tcont_Management(rest_interface_module, node_id, tcont)
    for tcont in tcont_Data_Delete:
        response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/tcont/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=2&onuId=-1")
        response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/tcont/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=3&onuId=-1")    
        Tcont_Management(rest_interface_module, node_id, tcont)
    for dba in dba_profile_Data_Config_Delete:
        DBA_Profile(rest_interface_module, node_id, dba, method='DELETE')       