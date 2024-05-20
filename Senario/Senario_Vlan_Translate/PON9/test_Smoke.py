import pytest
import logging
import json
from config import *
from conftest import *
from config import dict_Serial_Mapping_Vlan
from Pon.test_Pon_Initial_Information import Pon_Initial_Information
from Pon.test_onu_auto_learn import read_only_Onu_State,read_only_Onu_SN
from Switch.test_vlan import vlan_config
from copy_log_system import copy_log_to_server
from pytest_sina_framework import cli_interface_module
from pytest_sina_framework import rest_interface_module


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.ssh_dev("server_olt"), pytest.mark.rest_dev("olt_nms")]

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
        while("OPERATION_STATE"!=active):
            active = read_only_Onu_State(rest_interface_module, node_id ,1,1,port,onu+1) 
        SN.append(read_only_Onu_SN(rest_interface_module, node_id ,1,1,port,onu+1))  
    logger.info("****** check_Operation_Onus_On_Pon complete *************")
    logger.info(f"serial {SN}")
    return SN   

def find_vlan_from_Serial(rest_interface_module, port, node_id, SN):
    vlan =[]
    for sn in SN:
        for key,value in dict_Serial_Mapping_Vlan.items():
            if key==sn:
                vlan.append(dict_Serial_Mapping_Vlan[sn])
    logger.info("****** find_vlan_from_Serial complete *************")            
    logger.info(f"Vlan {vlan}")
    return vlan  


def test_Smoke(rest_interface_module, node_id):
    # ssh_interface_module.ex
    PORT_TotalNumberOnusInThisPort= {9:4}
    # try:
    for port,total_of_onu in PORT_TotalNumberOnusInThisPort.items():
        no_shutDown_Pon(rest_interface_module,port,node_id)
        ONUs = read_number_Onus_On_Pon(rest_interface_module, port, node_id, total_of_onu)
        SN = check_Operation_Onus_On_Pon(rest_interface_module, port, node_id, ONUs)
        Vlan = find_vlan_from_Serial(rest_interface_module, port, node_id, SN)
        Vlan_From_Serial_Of_ONUs[port]=Vlan  
    logger.info(f"Vlan_after_map {Vlan_From_Serial_Of_ONUs}")
    assert Vlan_From_Serial_Of_ONUs == {9:[700, 700, 700, 700]} #700, 700, 700, 700, 700, 700, 700, 700, 700, 700, 700, 700, 700, 700, 700, 700,
        #700, 700, 700, 700, 700, 700, 700, 700, 700, 700, 700, 700, 700, 700, 700, 700, 700, 700, 700, 700
    # except:
    #     copy_log_to_server("smoke", board_ip, "root", "sbkt4v")    
 




