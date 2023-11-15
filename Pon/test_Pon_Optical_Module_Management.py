import pytest
import logging
import json
from config import *
from conftest import *

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)

pon_optic_module = namedtuple('pon_optic_module', ['index', 'expected_result_Set', 'expected_result_Get',])                                       
pon_optic_module.__new__.__defaults__ = (None, {}, {},None, None)



pon_optic_module_Data = (
pon_optic_module(1, {"nodeId": None,"shelfId": 1,"slotId": 1,"portId": 2,"ifIndex": 1}),                                                          
)


def Pon_Optical_Module_Managment(rest_interface_module, node_id, pon_optic_module_data=pon_optic_module()):
    logger.info(f'PON OPTICAL MODULE TEST DATA ------- > {pon_optic_module_data.index}')
    expected_set = pon_optic_module_data.expected_result_Set  
    expected_set["nodeId"]= node_id
    expected_get = pon_optic_module_data.expected_result_Get  
    logger.info(f' GETTING PON OPTICAL MODULE')
    read_data = rest_interface_module.get_request(f"/api/gponconfig/opticModule/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["ifIndex"]))
    read_Rx = json.loads(read_data.text)
    assert read_Rx !=0 
    logger.info(f'check is completed and  RX = {read_Rx}')



def test_Pon_Optical_Module_Managment(rest_interface_module, node_id):
    Pon_Optical_Module_Managment(rest_interface_module, node_id, pon_optic_module_Data[0])       