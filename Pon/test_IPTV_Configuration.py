import pytest
import logging
import json
from config import *
from conftest import *
from Pon.test_Pon_Initial_Information import Pon_Initial_Information


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)

IPTV = namedtuple('IPTV', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
IPTV.__new__.__defaults__ = (None, {}, {},None, None)


IPTV_DATA = (
IPTV(1, {"nodeId": None,"shelfId": 1, "slotId": 1, "portId": 2,
        "onuId": 1,"uniType": "veip","rmOnuPortId": 2,"vlanId": 10,"priority": 7,},{
                                                            "portId": [2, "portId"],
                                                            "uniType": ["veip", "uniType"],
                                                            "onuId": [1, "onuId"],
                                                            "rmOnuPortId": [2, "rmOnuPortId"],
                                                            "vlanId": [10, "vlanId"],
                                                            "priority": [7, "priority"],},result="Pass",method="ADD"),
IPTV(2, {"nodeId": None,"shelfId": 1, "slotId": 1, "portId": 3,
        "onuId": 1,"uniType": "veip","rmOnuPortId": 3,"vlanId": 10,"priority": 7,},{
                                                            "portId": [3, "portId"],
                                                            "uniType": ["veip", "uniType"],
                                                            "onuId": [1, "onuId"],
                                                            "rmOnuPortId": [3, "rmOnuPortId"],
                                                            "vlanId": [10, "vlanId"],
                                                            "priority": [7, "priority"],},result="Pass",method="ADD"),                                                             

IPTV(3, {"nodeId": None,"shelfId": 1, "slotId": 1, "portId": 2,
        "onuId": 1,"uniType": "veip","rmOnuPortId": 2,"vlanId": 11,"priority": 8,},{
                                                            "portId": [2, "portId"],
                                                            "uniType": ["veip", "uniType"],
                                                            "onuId": [1, "onuId"],
                                                            "rmOnuPortId": [2, "rmOnuPortId"],
                                                            "vlanId": [11, "vlanId"],
                                                            "priority": [8, "priority"],},result="Pass",method="UPDATE"), 

IPTV(4, {"nodeId": None,"shelfId": 1, "slotId": 1, "portId": 2,
        "onuId": 1,"uniType": "pptp","rmOnuPortId": 2,"vlanId": 11,"priority": 8,},{
                                                            "portId": [2, "portId"],
                                                            "uniType": ["pptv", "uniType"],
                                                            "onuId": [1, "onuId"],
                                                            "rmOnuPortId": [2, "rmOnuPortId"],
                                                            "vlanId": [11, "vlanId"],
                                                            "priority": [8, "priority"],},result="Pass",method="UPDATE"),                                                             
IPTV(5, {"nodeId": None,"shelfId": 1, "slotId": 1, "portId": 2,
        "onuId": 1,"uniType": "veip","rmOnuPortId": 2,"vlanId": 10,"priority": 7,},{
                                                            "portId": [2, "portId"],
                                                            "uniType": ["veip", "uniType"],
                                                            "onuId": [1, "onuId"],
                                                            "rmOnuPortId": [2, "rmOnuPortId"],
                                                            "vlanId": [11, "vlanId"],
                                                            "priority": [8, "priority"],},result="Fail",method="ADD"),                                                             
                                                                                                                         
)
IPTV_Delete = (
    IPTV(1, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 1, "portId": 2},result="Pass",method="DELETE"), 
    IPTV(1, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 1, "portId": 3},result="Pass",method="DELETE"), 
)

def IPTV_Configuration(rest_interface_module, node_id, IPTV_data=IPTV(), method='ADD'):
    method = IPTV_data.method
    logger.info(f'IPTV CONFIGURATION TEST DATA ------- > {IPTV_data.index}')
    expected_set = IPTV_data.expected_result_Set
    expected_set["nodeId"]= int(node_id)
    expected_get = IPTV_data.expected_result_Get  

    logger.info(f"TRY TO {method} IPTV CONFIGURATION ...")
    if method == 'ADD':
        url = "/api/gponconfig/sp5100/rmonu/multicast/add"
        response = rest_interface_module.post_request(url, expected_set)  
    elif method == 'UPDATE':  
        url = "/api/gponconfig/sp5100/rmonu/multicast/update"
        response = rest_interface_module.post_request(url, data._asdict())       
    else:  # method==DELETE   
        url = f"/api/gponconfig/sp5100/rmonu/multicast/delete/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"])
        response = rest_interface_module.delete_request(url)

    if IPTV_data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in IPTV CONFIGURATION  {expected_set}'
        if response.status_code != 200:
            logger.error(response.message)
        #**********************************************************************
        if len(expected_get.keys()) !=0:
            logger.info(f' GETTING IPTV CONFIGURATION (after {method} method) ... ')
            read_data = rest_interface_module.get_request(f"/api/ggponconfig/sp5100/rmonu/multicast/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"{method} IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
            logger.info(f'check is completed in {method} method')
    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in IPTV CONFIGURATION {gem_data._asdict}'
        if len(expected_get.keys()) !=0:
            read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/rmonu/multicast/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"set steeep IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)





def test_IPTV_Configuration(rest_interface_module, node_id):
    Pon_Initial_Information(rest_interface_module, node_id, pon_init_info_Enable_Multicast, method='UPDATE')       
    for iptv in IPTV_DATA:
        IPTV_Configuration(rest_interface_module, node_id, iptv)
    for iptv in IPTV_Delete:
        IPTV_Configuration(rest_interface_module, node_id, iptv)
    Pon_Initial_Information(rest_interface_module, node_id, pon_init_info_Disable_Multicast, method='UPDATE')       
