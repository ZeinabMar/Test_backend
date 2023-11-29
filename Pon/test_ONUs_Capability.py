import pytest
import logging
import json
from config import *
from conftest import *

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)

onus_capability = namedtuple('onus_capability', ['index', "expected_result_Set", 'expected_result_Get', "result", "method"])                                       
onus_capability.__new__.__defaults__ = (None, {}, {}, None, None)
                                                       

ONUs_Capability_Data = (
onus_capability(1,{"nodeId": None,"shelfId": 1,"slotId": 1,"portId": 2,"onuId": 1}, {"portId": [2, "portId"],
                                                                                    "onuId": [1, "onuId"],
                                                                                    "tcontNum": [8, "tcontNum"],
                                                                                    "gemNum": [32, "gemNum"],
                                                                                    "queueNum": [88, "queueNum"],
                                                                                    "usQueueNum": [64, "usQueueNum"],
                                                                                    "dsQueueNum": [24, "dsQueueNum"],
                                                                                    "scheNum": [2, "scheNum"],
                                                                                    "cardNum": [15, "cardNum"],
                                                                                    "ethUniNum": [3, "ethUniNum"],
                                                                                    "veipNum": [4, "veipNum"]},result="Pass",method="GET"), 

onus_capability(2,{"nodeId": None,"shelfId": 1,"slotId": 1,"portId": 3,"onuId": 1}, {"portId": [3, "portId"],
                                                                                    "onuId": [1, "onuId"],
                                                                                    "tcontNum": [8, "tcontNum"],
                                                                                    "gemNum": [32, "gemNum"],
                                                                                    "queueNum": [104, "queueNum"],
                                                                                    "usQueueNum": [64, "usQueueNum"],
                                                                                    "dsQueueNum": [40, "dsQueueNum"],
                                                                                    "scheNum": [2, "scheNum"],
                                                                                    "cardNum": [1, "cardNum"],
                                                                                    "ethUniNum": [5, "ethUniNum"],
                                                                                    "veipNum": [1, "veipNum"]},result="Pass",method="GET"),                                                                                      

)


def ONUs_Capability(rest_interface_module, node_id, onus_capability_data=onus_capability(), method='UPDATE'):
    method = onus_capability_data.method
    logger.info(f'ONUs INITIAL INFORMATION TEST DATA ------- > {onus_capability_data.index}')
    expected_set = onus_capability_data.expected_result_Set
    expected_set["nodeId"]= node_id
    expected_get = onus_capability_data.expected_result_Get  

    logger.info(f"TRY TO {method} ONUs CAPABILITY ...")
    if len(expected_get.keys()) !=0: 
        logger.info(f' GETTING ONUs CAPABILITY (after {method} method) ... ')
        read_data = rest_interface_module.get_request(f"/api/gponconfig/rmonu/capability/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"]))
        input_data = json.loads(read_data.text)
        #**********************************************************************
        for key in expected_get.keys():
            logger.info(f"{method} IN {expected_get[key]}")
            check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
        logger.info(f'check is completed in {method} method')

    else:
        if len(expected_get.keys()) !=0:
            read_data = rest_interface_module.get_request(f"/api/gponconfig/rmonu/capability/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"set steeep IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)





def test_ONUs_Capability(rest_interface_module, node_id):

    for onu_cap in ONUs_Capability_Data:
        ONUs_Capability(rest_interface_module, node_id, onu_cap)       