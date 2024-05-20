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

# Serial_mapping_vlan_transparent = {
#     "UTEL20FC5178": 700, "HWTCF448E19E": 700, "HWTC5A93CF3F": 700, "HWTC20B3DAF0": 700, "HWTC20F3C478": 700
# }

# Serial_mapping_vlan_translate = {
#     "HWTC1A74B09C": 700, "HWTC1a27a188": 700, "HWTCA67EDEA4": 700, "HWTC96610DA3": 700, "HWTCD2099E7C": 700, "UTEL20FC5410":700
# }

Serial_mapping_vlan_transparent = {
    "HWTC9c828f95": 700, "HWTC20b3cc48": 700, 
}
    
Serial_mapping_vlan_translate = {
    "HWTC20f3ce08": 700, "HWTC20b3cb18": 700
}


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

def read_number_Onus_On_Pon(rest_interface_module, port, node_id, onu_On_Pon=0):
    read_data = rest_interface_module.get_request(f"/api/gponconfig/onu/getpononunumber/{node_id}/1/1/{port}")
    Onu_Detected = json.loads(read_data.text)
    if onu_On_Pon !=0:
        assert Onu_Detected["totalOnu"] == onu_On_Pon
    logger.info("****** read_number_Onus_On_Pon complete *************")
    return Onu_Detected["totalOnu"]


def check_Operation_Onus_On_Pon(rest_interface_module, port, node_id, ONUs):  
    active = "ADDED" 
    SN = []    
    for onu in range(ONUs):
        # while("OPERATION_STATE"!=active):
        #     active = read_only_Onu_State(rest_interface_module, node_id ,1,1,port,onu+1) 
        SN.append(read_only_Onu_SN(rest_interface_module, node_id ,1,1,port,onu+1))  
    logger.info("****** check_Operation_Onus_On_Pon complete *************")
    logger.info(f"serial {SN}")
    return SN   

def extract_Onusnumber_Serialnumber_Vlan(rest_interface_module, port, node_id, SN, mapping_data):
    SerialNumber_ONUsNumber_Vlan =[]
    for index in range(len(SN)):
        for key,value in mapping_data.items():
            if key==SN[index]:
                SerialNumber_ONUsNumber_Vlan.append({"ONUnumber":index+1, "Serialnumber":SN[index], "Vlan": mapping_data[SN[index]]})
    logger.info("****** find_vlan_from_Serial complete *************")            
    # logger.info(f"SerialNumber_ONUsNumber_Vlan {SerialNumber_ONUsNumber_Vlan}")
    return SerialNumber_ONUsNumber_Vlan  


def test_Smoke(rest_interface_module, node_id):
    PORT_TotalNumberOnusInThisPort= {1:4}
    PORTs_information_translate = {}
    PORTs_information_transparent = {}
    # try:
    for port,total_of_onu in PORT_TotalNumberOnusInThisPort.items():
        no_shutDown_Pon(rest_interface_module,port,node_id)
        ONUs = read_number_Onus_On_Pon(rest_interface_module, port, node_id, total_of_onu)
        SN= ["HWTC20b3cc48", "HWTC20b3cb18", "HWTC20f3ce08", "HWTC9c828f95"]
        # SN = check_Operation_Onus_On_Pon(rest_interface_module, port, node_id, ONUs)
        SerialNumber_ONUsNumber_Vlan_mapping_translate = extract_Onusnumber_Serialnumber_Vlan(rest_interface_module, port, node_id, SN, Serial_mapping_vlan_translate)
        SerialNumber_ONUsNumber_Vlan_mapping_transparent = extract_Onusnumber_Serialnumber_Vlan(rest_interface_module, port, node_id, SN, Serial_mapping_vlan_transparent)
        PORTs_information_translate[port]= SerialNumber_ONUsNumber_Vlan_mapping_translate 
        PORTs_information_transparent[port]= SerialNumber_ONUsNumber_Vlan_mapping_transparent 
    logger.info(f"transparent {PORTs_information_transparent}")
    logger.info(f"translate {PORTs_information_translate}")

    # except:
    #     copy_log_to_server("smoke", board_ip, "root", "sbkt4v")    
 




