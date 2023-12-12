import pytest
import logging
import json
from config import *
from conftest import *

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)

pon_init_info = namedtuple('pon_init_info', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
pon_init_info.__new__.__defaults__ = (None, {}, {},None, None)
  


pon_init_info_Data = (
pon_init_info(1, {"nodeId": None,"shelfId": 1,"slotId": 1,"portId": 2,"ifIndex": 2,"adminState": "DISABLE",
    "ponServiceEnable5100": "DISABLE","ponOnuAutoDiscovery": "ENABLE","ifModuleState5100": "DISABLED",
    "sfpModuleState5100": "DISABLED",   "ponMulticastState5100": 0,"operationalState": None,"scbPort": None,"modulePresent": 4,
    "scbMaxBw": None,"autoLearn": "ENABLE","operationalStateStr": "act_working","modulePresentStr": "Disabled"},{
                                                                                                            "portId": [2, "portId"],
                                                                                                            "ifIndex": [2, "ifIndex"],
                                                                                                            "adminState": ["DISABLE", "adminState"],
                                                                                                            "ponServiceEnable5100": ["DISABLE", "ponServiceEnable5100"],
                                                                                                            "ponOnuAutoDiscovery": ["ENABLE", "ponOnuAutoDiscovery"],
                                                                                                            "sfpModuleState5100": ["DISABLED", "sfpModuleState5100"],
                                                                                                            "ifModuleState5100": ["DISABLED", "ifModuleState5100"],
                                                                                                            "ponMulticastState5100": [0, "ponMulticastState5100"],
                                                                                                            "autoLearn": ["ENABLE", "autoLearn"],
                                                                                                            "operationalStateStr": ["inactive", "operationalStateStr"],
                                                                                                            "modulePresentStr": ["Disabled", "modulePresentStr"],},result="Pass",method="UPDATE"),                                                          
pon_init_info(2, {"nodeId": None,"shelfId": 1,"slotId": 1,"portId": 2,"ifIndex": 2,"adminState": "DISABLE",
    "ponServiceEnable5100": "ENABLE","ponOnuAutoDiscovery": "ENABLE","ifModuleState5100": "DISABLED",
    "sfpModuleState5100": "DISABLED", "ponMulticastState5100": 0,"operationalState": None,"scbPort": None,"modulePresent": 4,
    "scbMaxBw": None,"autoLearn": "ENABLE","operationalStateStr": "act_working","modulePresentStr": "Disabled"},{
                                                                                                            "portId": [2, "portId"],
                                                                                                            "ifIndex": [2, "ifIndex"],
                                                                                                            "adminState": ["DISABLE", "adminState"],
                                                                                                            "ponServiceEnable5100": ["ENABLE", "ponServiceEnable5100"],
                                                                                                            "ponOnuAutoDiscovery": ["ENABLE", "ponOnuAutoDiscovery"],
                                                                                                            "sfpModuleState5100": ["DISABLED", "sfpModuleState5100"],
                                                                                                            "ifModuleState5100": ["DISABLED", "ifModuleState5100"],
                                                                                                            "ponMulticastState5100": [0, "ponMulticastState5100"],
                                                                                                            "autoLearn": ["ENABLE", "autoLearn"],
                                                                                                            "operationalStateStr": ["act_working", "operationalStateStr"],
                                                                                                            "modulePresentStr": ["Disabled", "modulePresentStr"],},result="Pass",method="UPDATE"),                                                          
pon_init_info(3, {"nodeId": None,"shelfId": 1,"slotId": 1,"portId": 2,"ifIndex": 2,"adminState": "ENABLE",
    "ponServiceEnable5100": "ENABLE","ponOnuAutoDiscovery": "ENABLE","ifModuleState5100": "DISABLED",
    "sfpModuleState5100": "DISABLED", "ponMulticastState5100": 0,"operationalState": None,"scbPort": None,"modulePresent": 4,
    "scbMaxBw": None,"autoLearn": "ENABLE","operationalStateStr": "act_working","modulePresentStr": "Disabled"},{
                                                                                                            "portId": [2, "portId"],
                                                                                                            "ifIndex": [2, "ifIndex"],
                                                                                                            "adminState": ["ENABLE", "adminState"],
                                                                                                            "ponServiceEnable5100": ["ENABLE", "ponServiceEnable5100"],
                                                                                                            "ponOnuAutoDiscovery": ["ENABLE", "ponOnuAutoDiscovery"],
                                                                                                            "sfpModuleState5100": ["ENABLED", "sfpModuleState5100"],
                                                                                                            "ifModuleState5100": ["ENABLED", "ifModuleState5100"],
                                                                                                            "ponMulticastState5100": [0, "ponMulticastState5100"],
                                                                                                            "autoLearn": ["ENABLE", "autoLearn"],
                                                                                                            "operationalStateStr": ["act_working", "operationalStateStr"],
                                                                                                            "modulePresentStr": ["Enabled", "modulePresentStr"],},result="Pass",method="UPDATE"),                                                          

)


def Pon_Initial_Information(rest_interface_module, node_id, pon_init_info_data=pon_init_info(), method='UPDATE'):
    method = pon_init_info_data.method
    logger.info(f'PON INITIAL INFORMATION TEST DATA ------- > {pon_init_info_data.index}')
    expected_set = pon_init_info_data.expected_result_Set
    expected_set["nodeId"]= node_id
    expected_get = pon_init_info_data.expected_result_Get  

    logger.info(f"TRY TO {method} PON INITIAL INFORMATION ...")
    if method == "UPDATE":
        url = "/api/gponconfig/pon/saveprimaryinfo"
        response = rest_interface_module.post_request(url, expected_set)     
    
    if pon_init_info_data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in PON INITIAL INFORMATION config {expected_set}'
        if response.status_code != 200:
            logger.error(response.message)

        if len(expected_get.keys()) !=0: 
            logger.info(f' GETTING PON INITIAL INFORMATION (after {method} method) ... ')
            read_data = rest_interface_module.get_request(f"/api/gponconfig/pon/getprimaryinfo/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["ifIndex"]))
            input_data = json.loads(read_data.text)
            #**********************************************************************
            for key in expected_get.keys():
                logger.info(f"{method} IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
            logger.info(f'check is completed in {method} method')

    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in PON INITIAL INFORMATION {tcont_data._asdict}'
        if len(expected_get.keys()) !=0:
            read_data = rest_interface_module.get_request(f"c"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["ifIndex"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"set steeep IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)





def test_Pon_Initial_Information(rest_interface_module, node_id):
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/pon/getprimaryinfo/{node_id}/1/1/2/2")
    for pon_init in pon_init_info_Data:
        Pon_Initial_Information(rest_interface_module, node_id, pon_init)       