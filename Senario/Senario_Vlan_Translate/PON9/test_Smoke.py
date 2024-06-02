"""
in this smoke_test we test :
1) Operational or added situation for any ONu

and in ultimately our outcomes must be in order below:
{Port1:[ONU_number, Serial_number], ..., Port?:[ONU_number, Serial_number]}

in this senario we must have all intact onus with operational situation. 

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
        while("OPERATION_STATE"!=active):
            active = read_only_Onu_State(rest_interface_module, node_id ,1,1,port,onu+1) 
    logger.info("****** Onus are operational *************")


def test_Smoke(rest_interface_module, node_id):
    # try:
    PORT_TotalNumberOnusInThisPort= {9:40}
    Serial_number_of_operation_onus= ["HWTCdc99d69a", "HWTCf65efc9a", "HWTCc0a5899d", "HWTC70bbc89b", "HWTCd69f299c", "HWTC67ae299c", "HWTC40a58397", 
                                      "HWTCa151899b", "HWTCda1bb59a", "HWTCd662c09a", "HWTC265f8a9c", "HWTC7df2ba9b", "HWTC3f04589c", "HWTCe152f69b",
                                      "HWTC13fece9a", "HWTCff10df9a", "HWTCb918039a", "HWTCd7a4369a", "HWTC1a55c79c", "HWTC82f40c9b", "HWTCc714199a",
                                      "HWTCff326d9a", "HWTC00f8f19b", "HWTC1423179c", "HWTC0dacf29c", "HWTCcf99709b", "HWTCc685a29b", "HWTC81501a9a",
                                      "HWTC6a32229b", "HWTC24370d9a", "HWTC61fe6c9c", "HWTC13f0d79a", "HWTCdda1d79b", "HWTCe14e069b", "HWTC2a82ff9c",
                                      "HWTC265e039c", "HWTC98728b9b", "HWTC48dcdf9d", "HWTC79268d9a", "HWTC1fb0a09c"]
    for port,total_of_onu in PORT_TotalNumberOnusInThisPort.items():
        no_shutDown_Pon(rest_interface_module,port,node_id)
        ONUs = read_number_of_Onus_On_Pon(rest_interface_module, port, node_id, total_of_onu)
        Serial_number_of_all_onus = extract_Serial_number_of_ONUs(rest_interface_module, port, node_id, ONUs)
        check_Operation_Onus_On_Pon(rest_interface_module, port, node_id, Serial_number_of_all_onus, ONUs)    
        assert sorted(Serial_number_of_operation_onus) == sorted(Serial_number_of_all_onus)
    # except:
    #     copy_log_to_server("smoke", board_ip, "root", "sbkt4v")    
 




