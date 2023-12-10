import pytest
import logging
import json
from config import *
from conftest import *
from Pon.test_Pon_Initial_Information import Pon_Initial_Information
from Pon.test_onu_auto_learn import read_only_Onu_State
from Switch.test_vlan import vlan_config

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)

def detect_onu_with_Serial_number(rest_interface_module,port,ONU, node_id):
    dict_sn_onu = {}
    for port in range(port,port+1):
        response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/pon/getprimaryinfo/11/1/1/{port}/{port}")
        pon_no_shut = replace_dictionary(pon_init_info_no_shutdown, "set", {"portId":port,"ifIndex":port})
        pon_no_shut = replace_dictionary(pon_no_shut,"get", {"portId":[port,"portId"],"ifIndex":[port,"ifIndex"]})
        Pon_Initial_Information(rest_interface_module, node_id, pon_no_shut, method='UPDATE') 
        for onu in range(ONU):
            active = "ADDED"
            while("OPERATION_STATE"!=active):
                active = read_only_Onu_State(rest_interface_module, node_id ,1,1,port,onu) 
            SN = read_only_Onu_SN(rest_interface_module, node_id ,1,1,port,onu)     
            dict_sn_onu[f"{SN}"]= onu
    vlan =[]
    priority = []        
    for key,value in dict_sn_onu:
        for key2, value in dict_ONU_Vlan_Priority:
            if key==key2:
                vlan.append(dict_ONU_Vlan_Priority[key2][0])
                priority.append(dict_ONU_Vlan_Priority[key2][1])
    return vlan,priority,dict_sn_onu            



