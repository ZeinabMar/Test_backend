import pytest
import logging
import json
from config import *
from conftest import *

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)

onus_init_info = namedtuple('onus_init_info', ['index', "expected_result_Set", 'expected_result_Get', "result", "method"])                                       
onus_init_info.__new__.__defaults__ = (None, {}, {}, None, None)
                                                       

ONUs_Init_Info_Data = (
onus_init_info(1,{"nodeId": None,"shelfId": 1,"slotId": 1,"portId": 2,"onuId": 1}, {"portId": [2, "portId"],
                                                                                    "onuId": [1, "onuId"],
                                                                                    "version": ["AF6.A", "version"],
                                                                                    "sn": ["HWTC50ac3392", "sn"],
                                                                                    "snPass": [None, "snPass"],
                                                                                    "loid": ["", "loid"],
                                                                                    "loidPass": ["", "loidPass"],
                                                                                    "eqptId": ["HG8120C", "eqptId"],
                                                                                    "omccVersion": ["ITU-T G.988 (2010) Base and Extended", "omccVersion"],
                                                                                    "vendorId": ["HWTC", "vendorId"],
                                                                                    "priorityQueue": [88, "priorityQueue"],
                                                                                    "onuType": ["UNKNOWN","onuType"]},result="Pass",method="GET"),   
onus_init_info(2,{"nodeId": None,"shelfId": 1,"slotId": 1,"portId": 3,"onuId": 1}, {"portId": [3, "portId"],
                                                                                    "onuId": [1, "onuId"],
                                                                                    # "version": ["     ", "version"],
                                                                                    "sn": ["HWTC8f30f67c", "sn"],
                                                                                    "snPass": [None, "snPass"],
                                                                                    "loid": ["", "loid"],
                                                                                    "loidPass": ["", "loidPass"],
                                                                                    "eqptId": ["HG8245Q2", "eqptId"],
                                                                                    "omccVersion": ["ITU-T G.988 (2010) Base and Extended", "omccVersion"],
                                                                                    "vendorId": ["HWTC", "vendorId"],
                                                                                    "priorityQueue": [104, "priorityQueue"],
                                                                                    "onuType": ["HGU","onuType"]},result="Pass",method="GET"),                                                                                      

)


def ONUs_Initial_Information(rest_interface_module, node_id, onus_init_info_data=onus_init_info(), method='UPDATE'):
    method = onus_init_info_data.method
    logger.info(f'ONUs INITIAL INFORMATION TEST DATA ------- > {onus_init_info_data.index}')
    expected_set = onus_init_info_data.expected_result_Set
    expected_set["nodeId"]= node_id
    expected_get = onus_init_info_data.expected_result_Get  

    logger.info(f"TRY TO {method} ONUs INITIAL INFORMATION ...")
    if len(expected_get.keys()) !=0: 
        logger.info(f' GETTING ONUs INITIAL INFORMATION (after {method} method) ... ')
        read_data = rest_interface_module.get_request(f"/api/gponconfig/rmonu/info/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"]))
        input_data = json.loads(read_data.text)
        #**********************************************************************
        for key in expected_get.keys():
            logger.info(f"{method} IN {expected_get[key]}")
            check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
        logger.info(f'check is completed in {method} method')

    else:
        if len(expected_get.keys()) !=0:
            read_data = rest_interface_module.get_request(f"/api/gponconfig/rmonu/info/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"set steeep IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)





def test_ONUs_Initial_Information(rest_interface_module, node_id):
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/onu/getallauthenticated?nodeId={node_id}&shelfId=1&slotId=1&portId=2")
    for onu_init in ONUs_Init_Info_Data:
        ONUs_Initial_Information(rest_interface_module, node_id, onu_init)       