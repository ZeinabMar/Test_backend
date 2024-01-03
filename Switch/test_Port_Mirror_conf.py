import pytest
import logging
import json
from config import *
from conftest import *
# from pytest-check import check


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

Port_Mirror = namedtuple('Port_Mirror', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
Port_Mirror.__new__.__defaults__ = (None, {}, {},None, None)

Port_Mirror_DATA = (
Port_Mirror(1, {"nodeId": None,"shelfId": 1,"slotId": 1,"ethIfIndex": 1,
                "mirrorDirection": "MirrorBoth", "phyIfMirrorBoth": 2,"phyIfMirrorRx": -1,
                "phyIfMirrorTx": -1,},{"ethIfIndex": [1, "ethIfIndex"],
                                       "mirrorDirection": ["MirrorBoth", "mirrorDirection"],
                                       "phyIfMirrorBoth": [2, "phyIfMirrorBoth"],
                                       "phyIfMirrorRx": [-1, "phyIfMirrorRx"],
                                       "phyIfMirrorTx": [-1, "phyIfMirrorTx"]},result="Pass", method="UPDATE"),  

 Port_Mirror(2, {
 "nodeId": None,
 "shelfId": 1,
 "slotId": 1,
 "ethIfIndex": 1,
 "mirrorDirection": "MirrorRx", 
 "phyIfMirrorBoth": -1,
 "phyIfMirrorRx": 2,
 "phyIfMirrorTx": -1,},{"ethIfIndex": [1, "ethIfIndex"],
                                       "mirrorDirection": ["MirrorRx", "mirrorDirection"],
                                       "phyIfMirrorBoth": [-1, "phyIfMirrorBoth"],
                                       "phyIfMirrorRx": [2, "phyIfMirrorRx"],
                                       "phyIfMirrorTx": [-1, "phyIfMirrorTx"]},result="Pass", method="UPDATE"),  
 Port_Mirror(3, {
 "nodeId": None,
 "shelfId": 1,
 "slotId": 1,
 "ethIfIndex": 1,
 "mirrorDirection": "MirrorRx", 
 "phyIfMirrorBoth": -1,
 "phyIfMirrorRx": 1,
 "phyIfMirrorTx": -1,},{"ethIfIndex": [1, "ethIfIndex"],
                                       "mirrorDirection": ["MirrorRx", "mirrorDirection"],
                                       "phyIfMirrorBoth": [-1, "phyIfMirrorBoth"],
                                       "phyIfMirrorRx": [2, "phyIfMirrorRx"],
                                       "phyIfMirrorTx": [-1, "phyIfMirrorTx"]},result="Fail", method="UPDATE"), 
 Port_Mirror(4, {
 "nodeId": None,
 "shelfId": 1,
 "slotId": 1,
 "ethIfIndex": 1,
 "mirrorDirection": "MirrorRx", 
 "phyIfMirrorBoth": -1,
 "phyIfMirrorRx": 3,
 "phyIfMirrorTx": -1,},{"ethIfIndex": [1, "ethIfIndex"],
                                       "mirrorDirection": ["MirrorRx", "mirrorDirection"],
                                       "phyIfMirrorBoth": [-1, "phyIfMirrorBoth"],
                                       "phyIfMirrorRx": [3, "phyIfMirrorRx"],
                                       "phyIfMirrorTx": [-1, "phyIfMirrorTx"]},result="Pass", method="UPDATE"),                                       
Port_Mirror(5, {
 "nodeId": None,
 "shelfId": 1,
 "slotId": 1,
 "ethIfIndex": 2,
 "mirrorDirection": "MirrorRx", 
 "phyIfMirrorBoth": -1,
 "phyIfMirrorRx": 1,
 "phyIfMirrorTx": -1,},{"ethIfIndex": [2, "ethIfIndex"],
                                       "mirrorDirection": ["MirrorRx", "mirrorDirection"],
                                       "phyIfMirrorBoth": [-1, "phyIfMirrorBoth"],
                                       "phyIfMirrorRx": [1, "phyIfMirrorRx"],
                                       "phyIfMirrorTx": [-1, "phyIfMirrorTx"]},result="Passs", method="UPDATE"), 

 Port_Mirror(6, {
 "nodeId": None,
 "shelfId": 1,
 "slotId": 1,
 "ethIfIndex": 2,
 "mirrorDirection": "MirrorTx", 
 "phyIfMirrorBoth": -1,
 "phyIfMirrorRx": -1,
 "phyIfMirrorTx": 1,},{"ethIfIndex": [2, "ethIfIndex"],
                                       "mirrorDirection": ["MirrorTx", "mirrorDirection"],
                                       "phyIfMirrorBoth": [-1, "phyIfMirrorBoth"],
                                       "phyIfMirrorRx": [-1, "phyIfMirrorRx"],
                                       "phyIfMirrorTx": [1, "phyIfMirrorTx"]},result="Passs", method="UPDATE"),   
                                                                                                                                  

)

Port_Mirror_Delete = (
    Port_Mirror(1, {"nodeId": None,"shelfId": 1,"slotId": 1,"ethIfIndex": 1,"mirrorDirection": "MirrorRx", "phyIfMirrorBoth": -1,"phyIfMirrorRx": -1,"phyIfMirrorTx": -1,},result="Pass", method="DELETE"),
    Port_Mirror(2, {"nodeId": None,"shelfId": 1,"slotId": 1,"ethIfIndex": 2,"mirrorDirection": "MirrorRx", "phyIfMirrorBoth": -1,"phyIfMirrorRx": -1,"phyIfMirrorTx": -1,},result="Pass", method="DELETE"),

)



def Port_Mirror_config(rest_interface_module, node_id, Port_Mirror_data=Port_Mirror(), method='UPDATE'):
    logger.info(f'Port_Mirror_data CONFIGURATION TEST DATA ------- > {Port_Mirror_data.index}')
    method = Port_Mirror_data.method
    expected_set = Port_Mirror_data.expected_result_Set
    expected_set["nodeId"]= int(node_id)
    expected_get = Port_Mirror_data.expected_result_Get  

    logger.info(f"TRY TO {method} Port_Mirror CONFIG ...")
    if method == 'UPDATE' or method == 'DELETE':  
        url = "/api/gponconfig/sp5100/portmirrorconfig/update"
        response = rest_interface_module.post_request(url, expected_set) 

    if Port_Mirror_data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in MIRROR CONFIGURATION  {expected_set}'
        if response.status_code != 200:
            logger.error(response.message)
        #**********************************************************************
        if len(expected_get.keys()) !=0:
            logger.info(f' GETTING MIRROR CONFIGURATION (after {method} method) ... ')
            read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/portmirrorconfig/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["ethIfIndex"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"{method} IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
            logger.info(f'check is completed in {method} method')
    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in MIRROR CONFIGURATION {Port_Mirror_data._asdict}'
        if len(expected_get.keys()) !=0:
            read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/portmirrorconfig/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["ethIfIndex"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"set steeep IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)


def test_Port_Mirror_config(rest_interface_module, node_id):

    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/portmirrorconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
    for mirror in Port_Mirror_DATA:
        Port_Mirror_config(rest_interface_module, node_id, mirror, method='UPDATE')
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/portmirrorconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")    
    for mirror in Port_Mirror_Delete:
        Port_Mirror_config(rest_interface_module, node_id, mirror, method='DELETE')
 
                


        






