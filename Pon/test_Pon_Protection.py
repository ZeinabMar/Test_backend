import pytest
import logging
import json
from config import *
from conftest import *
from config import pon_init_info_no_shutdown
from Pon.test_Pon_Initial_Information import Pon_Initial_Information
from Pon.test_onu_auto_learn import read_only_Onu_State

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)


pon_protection = namedtuple('pon_protection', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
pon_protection.__new__.__defaults__ = (None, {}, {},None, None)

Pon_Protection_Data = (
pon_protection(1, {"nodeId": 11,"shelfId": 1,"slotId": 1,"groupIndex": 1,"groupName": "group1","workingPort": 2,
                        "protectionPort": 3,"activePort": 2,"groupState": 1,"groupSwitchOver": "W2P"}, {"groupIndex": [1, "groupIndex"],
                                                                                                        "groupName": ["group1", "groupName"],
                                                                                                        "workingPort": [2, "workingPort"],
                                                                                                        "protectionPort" :[3,"protectionPort"],
                                                                                                        "activePort" :[2,"activePort"],
                                                                                                        "groupState" :[1,"groupState"],
                                                                                                        "groupSwitchOver" :["W2P","groupSwitchOver"]},result="Pass",method="ADD"),
pon_protection(2, {"nodeId": 11,"shelfId": 1,"slotId": 1,"groupIndex": 1,"groupName": "group2","workingPort": 2,
                        "protectionPort": 3,"activePort": 2,"groupState": 1,"groupSwitchOver": "W2P"}, {"groupIndex": [1, "groupIndex"],
                                                                                                        "groupName": ["group2", "groupName"],
                                                                                                        "workingPort": [2, "workingPort"],
                                                                                                        "protectionPort" :[3,"protectionPort"],
                                                                                                        "activePort" :[2,"activePort"],
                                                                                                        "groupState" :[1,"groupState"],
                                                                                                        "groupSwitchOver" :["W2P","groupSwitchOver"]},result="Pass",method="UPDATE"),                                                                                                        
)  

Pon_Protection_Delete = (
    pon_protection(1, {"nodeId": 11,"shelfId": 1,"slotId": 1,"groupIndex": 1},result="Pass",method="DELETE"),
)

def Pon_Protection(rest_interface_module, node_id, pon_protection_data=pon_protection(), method='ADD'):
    method = pon_protection_data.method
    logger.info(f'PON PROTECTION TEST DATA ------- > {pon_protection_data.index}')
    expected_set = pon_protection_data.expected_result_Set
    expected_set["nodeId"]= int(node_id)
    expected_get = pon_protection_data.expected_result_Get  

    logger.info(f"TRY TO {method} PON PROTECTION CONFIG ...")
    if method == 'ADD':
        url = "/api/gponconfig/sp5100/ponprotection/add"
        response = rest_interface_module.post_request(url, expected_set) 
    elif method == 'UPDATE':
        url = "/api/gponconfig/sp5100/ponprotection/update"
        response = rest_interface_module.post_request(url, expected_set)        
    else:  # method==DELETE   
        url = f"/api/gponconfig/sp5100/ponprotection/delete/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["groupIndex"])
        response = rest_interface_module.delete_request(url)

    if pon_protection_data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in PON PROTECTION OLT {expected_set}'
        if response.status_code != 200:
            logger.error(response.message)
        #**********************************************************************
        if len(expected_get.keys()) !=0:
            logger.info(f' GETTING PON PROTECTION OLT (after {method} method) ... ')
            read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/ponprotection/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["groupIndex"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"{method} IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
            logger.info(f'check is completed in {method} method')

    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in PON PROTECTION OLT {pon_protection_data._asdict}'
        if len(expected_get.keys()) !=0:
            read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/ponprotection/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["groupIndex"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"set steeep IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)





def test_Pon_Protection(rest_interface_module, node_id):

    pon_init = replace_dictionary(pon_init_info_no_shutdown, "set", {"portId":2,"ifIndex":2})
    pon_init = replace_dictionary(pon_init,"get", {"portId":[2,"portId"],"ifIndex":[2,"ifIndex"]})
    Pon_Initial_Information(rest_interface_module, node_id, pon_init, method='UPDATE') 

    # pon_init = replace_dictionary(pon_init_info_shutdown, "set", {"portId":3,"ifIndex":3})
    # pon_init = replace_dictionary(pon_init,"get", {"portId":[3,"portId"],"ifIndex":[3,"ifIndex"]})   
    # Pon_Initial_Information(rest_interface_module, node_id, pon_init, method='UPDATE')       
    active = "ADDED"
    while("OPERATION_STATE"!=active):
        active = read_only_Onu_State(rest_interface_module, node_id ,1,1,2)       
    # ****************************************************************************************************************************
    for pon_protection in Pon_Protection_Data:
        Pon_Protection(rest_interface_module, node_id, pon_protection)  
    for pon_protection in Pon_Protection_Delete:
        Pon_Protection(rest_interface_module, node_id, pon_protection)      

    