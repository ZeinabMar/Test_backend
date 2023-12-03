import pytest
import logging
import json
from config import *
from conftest import *
from Pon.test_Pon_Initial_Information import Pon_Initial_Information
from Pon.test_onu_auto_learn import read_only_Onu_State

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)



def test_Shut_Down_On(rest_interface_module, node_id):

    pon_init = replace_dictionary(pon_init_info_no_shutdown, "set", {"portId":2,"ifIndex":2})
    pon_init = replace_dictionary(pon_init,"get", {"portId":[2,"portId"],"ifIndex":[2,"ifIndex"]})
    Pon_Initial_Information(rest_interface_module, node_id, pon_init, method='UPDATE') 

    # pon_init = replace_dictionary(pon_init_info_shutdown, "set", {"portId":3,"ifIndex":3})
    # pon_init = replace_dictionary(pon_init,"get", {"portId":[3,"portId"],"ifIndex":[3,"ifIndex"]})   
    # Pon_Initial_Information(rest_interface_module, node_id, pon_init, method='UPDATE')  

    active = "ADDED"
    while("OPERATION_STATE"!=active):
        active = read_only_Onu_State(rest_interface_module, node_id ,1,1,2)   
    pon_init = replace_dictionary(pon_init_info_shutdown, "set", {"portId":2,"ifIndex":2})
    pon_init = replace_dictionary(pon_init,"get", {"portId":[2,"portId"],"ifIndex":[2,"ifIndex"]})
    Pon_Initial_Information(rest_interface_module, node_id, pon_init, method='UPDATE') 
    active = read_only_Onu_State(rest_interface_module, node_id ,1,1,2) 
    assert active== "ADDED"

    # pon_init = replace_dictionary(pon_init_info_no_shutdown, "set", {"portId":3,"ifIndex":3})
    # pon_init = replace_dictionary(pon_init,"get", {"portId":[3,"portId"],"ifIndex":[3,"ifIndex"]})   
    # Pon_Initial_Information(rest_interface_module, node_id, pon_init, method='UPDATE') 
    # active = "ADDED"
    # while("OPERATION_STATE"!=active):
    #     active = read_only_Onu_State(rest_interface_module, node_id ,1,1,3) 