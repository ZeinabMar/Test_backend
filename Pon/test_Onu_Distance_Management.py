import pytest
import logging
import json
from config import *
from conftest import *
from Pon.test_Pon_Initial_Information import Pon_Initial_Information


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)

Onu_Distance = namedtuple('Onu_Distance', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
Onu_Distance.__new__.__defaults__ = (None, {}, {},None, None)
Onu_Distance_logic_Data = (Onu_Distance(1, { "nodeId": None, "shelfId": 1,  "slotId": 1, 
                                                  "portId": 2,  "maxLogicDistance": 20, },{"portId": [2, "portId"],
                                                                                           "maxLogicDistance": [20, "maxLogicDistance"]},result="Pass",method="UPDATE"),
                          Onu_Distance(2, { "nodeId": None, "shelfId": 1,  "slotId": 1, 
                                                  "portId": 2,  "maxLogicDistance": 30, },{"portId": [2, "portId"],
                                                                                           "maxLogicDistance": [30, "maxLogicDistance"]},result="Pass",method="UPDATE"),                                                                                 
)
Onu_Distance_physical_Data = Onu_Distance(1, { "nodeId": None, "shelfId": 1,  "slotId": 1, 
                                               "portId": 2,  "onuId": 1, },result="Pass",method="GET")


def Onu_Distance(rest_interface_module, node_id, Onu_Distance_data=Onu_Distance(), method='UPDATE', type_distance = "logical"):
    method = Onu_Distance_data.method
    logger.info(f'DISTANCE ------- > {Onu_Distance_data.index}')
    expected_set = Onu_Distance_data.expected_result_Set
    expected_set["nodeId"]= node_id
    expected_get = Onu_Distance_data.expected_result_Get  

    if type_distance == "logical":
        if method == "UPDATE":
            logger.info(f"TRY TO {method} PON INITIAL INFORMATION ...")
            url = "/api/gponconfig/pon/maxlogicdistance"
            response = rest_interface_module.post_request(url, expected_set)    
        if Onu_Distance_data.result == "Pass":
            assert response.status_code == 200, f'{method} ERROR in DISTANCE CONFIG {expected_set}'
            if response.status_code != 200:
                logger.error(response.message)
            if len(expected_get.keys()) !=0: 
                logger.info(f' GETTING LOGICAL DISTANCE INFORMATION (after {method} method) ... ')
                read_data = rest_interface_module.get_request(f"/api/gponconfig/pon/getmaxlogicdistance/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"]))
                input_data = json.loads(read_data.text)
                #**********************************************************************
                for key in expected_get.keys():
                    logger.info(f"{method} IN {expected_get[key]}")
                    check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
                logger.info(f'check is completed in {method} method')

        else:
            assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in DISTANCE INFORMATION {Onu_Distance_data._asdict}'
            if len(expected_get.keys()) !=0:
                read_data = rest_interface_module.get_request(f"/api/gponconfig/pon/getmaxlogicdistance/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"]))
                input_data = json.loads(read_data.text)
                for key in expected_get.keys():
                    logger.info(f"set steeep IN {expected_get[key]}")
                    check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
        
    else :
        logger.info(f' GETTING PHISICAL INFORMATION (after {method} method) ... ')
        read_data = rest_interface_module.get_request(f"/api/gponconfig/opticModule/physicaldistance/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"]))
        input_data = json.loads(read_data.text)
        #**********************************************************************
        assert input_data == 20
        logger.info(f'check is completed in {method} method')    


def test_Onu_Distance(rest_interface_module, node_id):
    Pon_Initial_Information(rest_interface_module, node_id, pon_init_info_shutdown, method='UPDATE')       
    for distance in Onu_Distance_logic_Data:
        Onu_Distance(rest_interface_module, node_id, distance, method='UPDATE', type_distance="logical")   
    Onu_Distance(rest_interface_module, node_id, Onu_Distance_physical_Data, method='GET', type_distance="physical")    
    Pon_Initial_Information(rest_interface_module, node_id, pon_init_info_no_shutdown, method='UPDATE')                 