"""
in this smoke_test we test :
1) Operational or added situation for any ONu

and in ultimately our outcomes must be in order below:
{Port1:[ONU_number, Serial_number], ..., Port?:[ONU_number, Serial_number]}

in this senario we must have 5 intact onus with operational situation. 
rest of onus will be for executing Pon_los in system.
you can config them or not.

"""

import pytest
import logging
import json
from config import *
from conftest import *
from Pon.test_Pon_Initial_Information import Pon_Initial_Information
from Pon.test_onu_auto_learn import read_only_Onu_State,read_only_Onu_SN
from Switch.test_vlan import vlan_config
from copy_log_system import copy_log_to_server

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def no_shutDown_Pon(rest_interface_module,port,node_id):
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/pon/getprimaryinfo/{node_id}/1/1/{port}/{port}")
    Pon_Initial_Information(rest_interface_module, node_id, pon_init_info(1, {"nodeId": None,"shelfId": 1,"slotId": 1,"portId": port,"ifIndex": port,"adminState": "ENABLE",
                                                                                                            "ponServiceEnable5100": "ENABLE","ponOnuAutoDiscovery": "ENABLE","ifModuleState5100": "DISABLED",
                                                                                                            "sfpModuleState5100": "DISABLED", "ponMulticastState5100": 0,"operationalState": None,"scbPort": None,"modulePresent": 4,
                                                                                                            "scbMaxBw": None,"autoLearn": "ENABLE","operationalStateStr": "act_working","modulePresentStr": "Disabled"},{
                                                                                                            "portId": [port, "portId"],
                                                                                                            "ifIndex": [port, "ifIndex"],
                                                                                                            "adminState": ["ENABLE", "adminState"],
                                                                                                            "ponServiceEnable5100": ["ENABLE", "ponServiceEnable5100"],
                                                                                                            "ponOnuAutoDiscovery": ["ENABLE", "ponOnuAutoDiscovery"],
                                                                                                            "sfpModuleState5100": ["ENABLED", "sfpModuleState5100"],
                                                                                                            "ifModuleState5100": ["ENABLED", "ifModuleState5100"],
                                                                                                            "ponMulticastState5100": [0, "ponMulticastState5100"],
                                                                                                            "autoLearn": ["ENABLE", "autoLearn"],
                                                                                                            "operationalStateStr": ["act_working", "operationalStateStr"],
                                                                                                            "modulePresentStr": ["Enabled", "modulePresentStr"],},result="Pass",method="UPDATE")  )                                               
    logger.info("****** no_shutDown_Pon complete *************")

def read_number_of_Onus_On_Pon(rest_interface_module, port, node_id, onu_On_Pon=0):
    read_data = rest_interface_module.get_request(f"/api/gponconfig/onu/getpononunumber/{node_id}/1/1/{port}")
    Onu_Detected = json.loads(read_data.text)
    if onu_On_Pon !=0:
        assert Onu_Detected["totalOnu"] == onu_On_Pon
    logger.info("****** read_number_of_Onus_On_Pon complete *************")
    return Onu_Detected["totalOnu"]

def extract_Serial_number_of_ONUs(rest_interface_module, port, node_id, ONUs):
    SN = []    
    for onu in range(ONUs):
        SN.append(read_only_Onu_SN(rest_interface_module, node_id ,1,1,port,onu+1))  
    logger.info("****** extract Serial number of Onus complete*************")
    logger.info(f"serial {SN}")
    return SN   


def check_Operation_Onus_On_Pon(rest_interface_module, port, node_id, SN, ONUs):  
    active = "ADDED" 
    for onu in range(ONUs):
        for serial_num in SN:    
            if serial_num == read_only_Onu_SN(rest_interface_module, node_id ,1,1,port,onu+1):
                while("OPERATION_STATE"!=active):
                    active = read_only_Onu_State(rest_interface_module, node_id ,1,1,port,onu+1) 
    logger.info("****** Onus are operational *************")


def test_Smoke(rest_interface_module, node_id):
    # try:
    Serial_number_of_operation_onus= ["UTEL20FC5178", "HWTCF448E19E"]
    Serial_of_all_onus = []
    PORT_TotalNumberOnusInThisPort= {10:1, 4:1}
    for port,total_of_onu in PORT_TotalNumberOnusInThisPort.items():
        no_shutDown_Pon(rest_interface_module,port,node_id)
        ONUs = read_number_of_Onus_On_Pon(rest_interface_module, port, node_id, total_of_onu)
        Serial_of_all_onus.append(extract_Serial_number_of_ONUs(rest_interface_module, port, node_id, ONUs))
        check_Operation_Onus_On_Pon(rest_interface_module, port, node_id, Serial_number_of_operation_onus, ONUs)    
    assert sorted(Serial_of_all_onus) == sorted(Serial_number_of_operation_onus)
    # except:
    #     copy_log_to_server("smoke", board_ip, "root", "sbkt4v")    
 




