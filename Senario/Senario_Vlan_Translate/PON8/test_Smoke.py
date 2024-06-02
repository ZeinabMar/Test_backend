"""
in this smoke_test we test :
1) Operational or added situation for any ONu

and in ultimately our outcomes must be in order below:
{Port1:[ONU_number, Serial_number, Vlan_Translate, Vlan_Transparent], ..., Port?:[ONU_number, Serial_number, Vlan_Translate, Vlan_Transparent]}

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


Vlan_Translate = {"HWTC1a27a188":900, "HWTC1A74B09C":900, "HWTCA67EDEA4":800,"HWTC96610DA3":800, "HWTCD2099E7C":700, "UTEL20FC5410":700,
                  "HWTCA4C5349C":700, "HWTC41D47EAC":700, "HWTC7758307C":700}
Vlan_Transparent = {"HWTC1a27a188": 700, "HWTC1A74B09C":700, "HWTCA67EDEA4":900, "HWTC96610DA3":900, "HWTCD2099E7C":900, "UTEL20FC5410":900,
                    "HWTCA4C5349C":900, "HWTC41D47EAC":900, "HWTC7758307C":900}

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

def generate_list_of_serial_number_based_on_onu_number_and_Vlan(rest_interface_module, port, node_id, SN_operationl_onus):
    SerialNumber_ONUsNumber_Vlans =[]
    counter = 0
    for serial_num_op in SN_operationl_onus:
        counter = counter+1
        SerialNumber_ONUsNumber_Vlans.append({"ONUnumber":counter, "Serialnumber":serial_num_op, "Vlan_Translate": Vlan_Translate[serial_num_op], "Vlan_Transparent":Vlan_Transparent[serial_num_op]})
    logger.info("****** find list of Serial with onus number complete *************")            
    return SerialNumber_ONUsNumber_Vlans  

def config_smoke_requirement(rest_interface_module, node_id):
    PORTs_information = {}
    PORT_TotalNumberOnusInThisPort= {8:9}
    Serial_number_of_operation_onus= ["HWTC1A74B09C", "HWTC1a27a188", "HWTCA67EDEA4", "HWTC96610DA3", "HWTCD2099E7C", "UTEL20FC5410", "HWTCA4C5349C","HWTC41D47EAC", "HWTC7758307C"]
    for port,total_of_onu in PORT_TotalNumberOnusInThisPort.items():
        no_shutDown_Pon(rest_interface_module,port,node_id)
        ONUs = read_number_of_Onus_On_Pon(rest_interface_module, port, node_id, total_of_onu)
        Serial_number_of_all_onus = extract_Serial_number_of_ONUs(rest_interface_module, port, node_id, ONUs)
        check_Operation_Onus_On_Pon(rest_interface_module, port, node_id, Serial_number_of_all_onus, ONUs)    
        Serial_num_Mapping_Onu_num = generate_list_of_serial_number_based_on_onu_number_and_Vlan(rest_interface_module, port, node_id, Serial_number_of_all_onus)
        assert sorted(Serial_number_of_operation_onus) == sorted(Serial_number_of_all_onus)
        PORTs_information[port]= Serial_num_Mapping_Onu_num 
    logger.info(f"PORTs_information {PORTs_information}")
    return PORTs_information

def test_Smoke(rest_interface_module, node_id):
    # try:
    PORTs_information = config_smoke_requirement(rest_interface_module, node_id)
    assert PORTs_information != None
    # except:
    #     copy_log_to_server("smoke", board_ip, "root", "sbkt4v")    
 




