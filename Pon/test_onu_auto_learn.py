import pytest
import logging
import json
from config import *
from conftest import *

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)

onu_general = namedtuple('onu_general', ['index', 'expected_result_Set', 'expected_result_Get', "result"])                                       
onu_general.__new__.__defaults__ = (None, {}, {},None)

#*************************************    PON SECTION   ******************************************************    

# gpon-onu1/2:1
onu_general_Data = (
    onu_general(1,{
    "nodeId": 11,
    "shelfId": 1,
    "slotId": 1,
    "portId": 2,
    "ifIndex": 2,
    "adminState": "ENABLE",
    "ponServiceEnable5100": "ENABLE",
    "ponOnuAutoDiscovery": "ENABLE",
    "ifModuleState5100": "ENABLED",
    "sfpModuleState5100": "ENABLED",
    "operationalState": None,
    "scbPort": None,
    "modulePresent": 1,
    "scbMaxBw": None,
    "autoLearn": "ENABLE",
    "operationalStateStr": "act_working",
    "modulePresentStr": "Enabled",
    "deviceType": None,
    "errorCode": 0
},{"portId": [2, "portId"], 
                                                                                               "ifIndex": [2, "ifIndex"],
                                                                                               "adminState": ["ENABLE", "adminState"],
                                                                                               "ponServiceEnable5100": ["ENABLE", "ponServiceEnable5100"],
                                                                                               "ponOnuAutoDiscovery": ["ENABLE", "ponOnuAutoDiscovery"],
                                                                                               "ifModuleState5100": ["ENABLED", "ifModuleState5100"], 
                                                                                               "sfpModuleState5100": ["ENABLED", "sfpModuleState5100"], 
                                                                                               "autoLearn": ["ENABLE", "autoLearn"],
                                                                                               "operationalStateStr": ["act_working", "operationalStateStr"],
                                                                                               "modulePresentStr": ["Enabled", "modulePresentStr"]} , result = "Pass"),

onu_general(2,{
    "nodeId": 11,
    "shelfId": 1,
    "slotId": 1,
    "portId": 2,
    "ifIndex": 2,
    "adminState": "DISABLE",
    "ponServiceEnable5100": "ENABLE",
    "ponOnuAutoDiscovery": "ENABLE",
    "ifModuleState5100": "ENABLED",
    "sfpModuleState5100": "ENABLED",
    "operationalState": None,
    "scbPort": None,
    "modulePresent": 1,
    "scbMaxBw": None,
    "autoLearn": "ENABLE",
    "operationalStateStr": "act_working",
    "modulePresentStr": "Enabled",
    "deviceType": None,
    "errorCode": 0
},{"portId": [2, "portId"], 
                                                                                               "ifIndex": [2, "ifIndex"],
                                                                                               "adminState": ["DISABLE", "adminState"],
                                                                                               "ponServiceEnable5100": ["ENABLE", "ponServiceEnable5100"],
                                                                                               "ponOnuAutoDiscovery": ["ENABLE", "ponOnuAutoDiscovery"],
                                                                                               "ifModuleState5100": ["ENABLED", "ifModuleState5100"], 
                                                                                               "sfpModuleState5100": ["ENABLED", "sfpModuleState5100"], 
                                                                                               "autoLearn": ["ENABLE", "autoLearn"],
                                                                                               "operationalStateStr": ["act_working", "operationalStateStr"],
                                                                                               "modulePresentStr": ["Enabled", "modulePresentStr"]} , result = "Pass")                                                                                       
                                                                                               
                                                                                               )

def onu_auto_learn(rest_interface_module, node_id, ONU_data=onu_general(), method ="ADD"):
    logger.info(f"ONU TEST-DATA --> {ONU_data}")
    data_set = ONU_data.expected_result_Set
    data_set["nodeId"] = node_id
    data_get = ONU_data.expected_result_Get

    
    response = rest_interface_module.post_request("/api/gponconfig/pon/saveprimaryinfo", data_set)
    if ONU_data.result == "Pass":
        logger.info("first")
        assert 200 == response.status_code
        logger.info("second")

        # if len(data_get.keys()) !=0:
        #     logger.info(f' GETTING INITIAL PON INFO (after {method} method) ... ')
        #     read_init_data = rest_interface_module.get_request(f"/api/gponconfig/pon/getprimaryinfo/"+str(data_set["nodeId"])+"/"+str(data_set["shelfId"])+"/"+str(data_set["slotId"])+"/"+str(data_set["portId"])+"/"+str(data_set["ifIndex"]))
        #     input_data = json.loads(read_init_data.text)
        #     for key in data_get.keys():
        #         logger.info(f"{method} IN {data_get[key]}")
        #         check_set_value(rest_interface_module, data_get[key][0], data_get[key][1],input_data)
        #     logger.info(f'check is completed in {method} method')

        logger.info(f' GETTING INFRASTRUCTURE ONU (after {method} method) ... ')
        input_data_getall = rest_interface_module.get_request(f"/api/gponconfig/onu/getallauthenticated?nodeId="+str(data_set["nodeId"])+"&shelfId="+str(data_set["shelfId"])+"&slotId="+str(data_set["slotId"])+"&portId="+str(data_set["portId"]))
        logger.info(f"input_data_getall {input_data_getall}")
        input_data_getall = json.loads(input_data_getall.text)
        input_data = find_in_getall(input_data_getall, "portId", data_set["portId"])
        logger.info(f"input_data {input_data}")
        logger.info("third")
        if data_set["adminState"]=="ENABLE":
            assert input_data["onuState"] == "OPERATION_STATE"
        else:   
            assert input_data["onuState"] == "ADDED"

        logger.info("forth")
    else:
        assert 500 == response.status_code
 


 
def test_onu_authentication(rest_interface_module, node_id):

    for data in onu_general_Data:
        onu_auto_learn(rest_interface_module, node_id, data, "ADD")