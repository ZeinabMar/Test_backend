import pytest
import logging
import json
from config import *
from conftest import *
from Pon.test_tcont_profile import Tcont_Management
from Pon.test_dba_profile import DBA_Profile


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)

add_edit_onu = namedtuple('add_edit_onu', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
add_edit_onu.__new__.__defaults__ = (None, {}, {},None, None)

Add_Edit_Onus_Data = (
add_edit_onu(1, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"1","name": "gem1", "onuId": 1, "portId": 2, "tcontId": 8},
                                                           {
                                                            "gemid": [1, "gemId"],
                                                            "name": ["gem1", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [2, "portId"],
                                                            "tcontId": [8, "tcontId"]},result="Pass",method="ADD"),  
)
add_edit_onu_Delete = (
)

def Add_Edit_Onus(rest_interface_module, node_id, add_edit_onu_data=add_edit_onu(), method='ADD'):
    method = add_edit_onu_data.method
    logger.info(f'ADD/EDIT ONUS TEST DATA ------- > {add_edit_onu_data.index}')
    expected_set = add_edit_onu_data.expected_result_Set
    expected_set["nodeId"]= int(node_id)
    expected_get = add_edit_onu_data.expected_result_Get  

    logger.info(f"TRY TO {method} ADD/EDIT ONUS CONFIG ...")
    if method == 'ADD':
        url = "/api/gponconfig/onu/add"
        response = rest_interface_module.post_request(url, expected_set)    
    else:  # method==DELETE   
        url = f"/api/gponconfig/onu/delete/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"])
        response = rest_interface_module.delete_request(url)

    if dba_profile_data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in DBA_Profile config {expected_set}'
        if response.status_code != 200:
            logger.error(response.message)
        if len(expected_get.keys()) !=0:
            logger.info(f' GETTING ADD/EDIT ONUS (after {method} method) ... ')
            read_data = rest_interface_module.get_request(f"/api/gponconfig/onu/getallauthenticated?nodeId="+str(expected_set["nodeId"])+"&shelfId="+str(expected_set["shelfId"])+"&slotId="+str(expected_set["slotId"])+"&portId="+str(expected_set["slotId"]))
            input_data_getall = json.loads(read_data.text)
            input_data = find_in_getall(input_data_getall, "onuId", expected_get["onuId"][0])
            for key in expected_get.keys():
                logger.info(f"{method} IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
            logger.info(f'check is completed in {method} method')
    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in ADD/EDIT ONUS {expected_set}'
        if len(expected_get.keys()) !=0:
            logger.info(f' GETTING ADD/EDIT ONUS (after {method} method) ... ')
            read_data = rest_interface_module.get_request(f"/api/gponconfig/onu/getallauthenticated?nodeId="+str(expected_set["nodeId"])+"&shelfId="+str(expected_set["shelfId"])+"&slotId="+str(expected_set["slotId"]))
            input_data_getall = json.loads(read_data.text)
            input_data = find_in_getall(input_data_getall, "onuId", expected_get["onuId"][0])
            for key in expected_get.keys():
                logger.info(f"set steeep IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)



def test_Add_Edit_Onus(rest_interface_module, node_id):
    pass    
