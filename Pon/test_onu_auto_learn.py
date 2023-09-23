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
onu_general_Data = (
    onu_general(1, {"nodeId": 17,
                "shelfId": 1,
                "slotId": 1,
                "portId": 1,
                "ifIndex": 1,
                "adminState": "ENABLE",
                "ponServiceEnable5100": "ENABLE",
                "ponOnuAutoDiscovery": "DISABLE",
                "ifModuleState5100": "DISABLED",
                "sfpModuleState5100": "DISABLED",
                "operationalState": None,
                "scbPort": None,
                "modulePresent": 4,
                "scbMaxBw": None,
                "autoLearn": "ENABLE",
                "operationalStateStr": "act_working",
                "modulePresentStr": "Disabled",
                "deviceType": None,
                "errorCode": 0},None, result = "Pass"),
                )

def onu_auto_learn(rest_interface_module, node_id, ONU_data=onu_general()):
    logger.info(f"ONU TEST-DATA --> {ONU_data}")
    data_set = ONU_data.expected_result_Set
    data_set["nodeId"] = node_id
    
    response = rest_interface_module.post_request("/api/gponconfig/pon/saveprimaryinfo", data_set)
    if ONU_data.result == "Pass":
        logger.info("first")
        assert 200 == response.status_code
        logger.info("second")
        read_data = rest_interface_module.get_request("/api/gponconfig/onu/getallauthenticated")
        read_data = json.loads(read_data.text)
        logger.info(f"data_set {data_set}")
        logger.info(f"read_data {read_data}")
        input_data = list(filter(lambda dic: dic["ifIndex"] == data_set["ifIndex"], read_data))
        logger.info("third")
        assert input_data[0]["onuState"] == "OPERATION_STATE"
        logger.info("forth")
    else:
        assert 500 == response.status_code
 


 
def test_onu_authentication(rest_interface_module, node_id):

    for data in onu_general_Data:
        onu_auto_learn(rest_interface_module, node_id, data)