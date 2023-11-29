import pytest
import logging
import json
from config import *
from conftest import *
from Pon.test_tcont_profile import Tcont_Management
from Pon.test_dba_profile import DBA_Profile
from Pon.test_gem_profile import Gem_Management
from Switch.bridge_funcs import bridge_config
from Switch.test_vlan import vlan_config
from Switch.test_Bridge_group_conf import switch_config
from Switch.test_uplink_port_Vlan_conf import uplink_vlan_config
from Pon.test_OLT_Service import OLT_Service


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)

Aes_management = namedtuple('Aes_management', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
Aes_management.__new__.__defaults__ = (None, {}, {},None, None)

Aes_Management_Pon_Data = (
Aes_management(1, {"nodeId": None, "shelfId": 1,"slotId": 1,
                "portId": 2,"exchangeCtrl": "ENABLE","exchangeInterval": 10000},{ "exchangeCtrl": ["ENABLE", "exchangeCtrl"],
                                                                                  "exchangeInterval": [10000, "exchangeInterval"],
                                                                                  "portId": [2, "portId"]},result="Pass",method="UPDATE"),  
Aes_management(2, {"nodeId": None, "shelfId": 1,"slotId": 1,
                "portId": 2,"exchangeCtrl": "ENABLE","exchangeInterval": 10000},{ "exchangeCtrl": ["ENABLE", "exchangeCtrl"],
                                                                                  "exchangeInterval": [10000, "exchangeInterval"],
                                                                                  "portId": [2, "portId"]},result="Fail",method="UPDATE"),
Aes_management(3, {"nodeId": None, "shelfId": 1,"slotId": 1,
                "portId": 2,"exchangeCtrl": "DISABLE","exchangeInterval": 10000},{ "exchangeCtrl": ["DISABLE", "exchangeCtrl"],
                                                                                  "exchangeInterval": [10000, "exchangeInterval"],
                                                                                  "portId": [2, "portId"]},result="Pass",method="UPDATE"),                                                                                  
)

Aes_Management_Gem_Data = (
Aes_management(1,{"nodeId": None, "shelfId": 1, "slotId": 1, "portId": 2,
                  "gemId": 1, "onuId": 1,"downstreamEncryption": "ENABLE",} ,{ "downstreamEncryption": ["ENABLE", "downstreamEncryption"],
                                                                                  "gemId": [1, "gemId"],
                                                                                  "portId": [2, "portId"],
                                                                                  "onuId" : [1, "onuId"]},result="Pass",method="UPDATE"),  

)

def AES_encryption_Management(rest_interface_module, node_id, Aes_management_data=Aes_management(), method='UPDATE', Operator = "Pon"):
    method = Aes_management_data.method
    logger.info(f'AES encryption MANAGEMENT TEST DATA IN {Operator} ------- > {Aes_management_data.index}')
    expected_set = Aes_management_data.expected_result_Set
    expected_set["nodeId"]= int(node_id)
    expected_get = Aes_management_data.expected_result_Get  

    logger.info(f"TRY TO {method} AES encryption MANAGEMENT CONFIG in {Operator}...")
    if method == 'UPDATE':
        if Operator == "Pon":
            url = "/api/gponconfig/pon/saveaes"   
        else:
            url = "/api//gponconfig/gem/saveaes"    
        response = rest_interface_module.post_request(url, expected_set)     

    if Aes_management_data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in AES encryption MANAGEMENT config in {Operator} {expected_set}'
        if response.status_code != 200:
            logger.error(response.message)
        #**********************************************************************
        if len(expected_get.keys()) !=0:
            logger.info(f' GETTING AES encryption MANAGEMENT in {Operator} (after {method} method) ... ')
            if Operator == "Pon":
                read_data = rest_interface_module.get_request(f"/api/gponconfig/pon/getaes/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"]))
            else:
                read_data = rest_interface_module.get_request(f"/api/gponconfig/gem/getaes/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["gemId"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"{method} IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
            logger.info(f'check is completed in {method} method')
    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in AES encryption MANAGEMENT IN {Operator} {gem_data._asdict}'
        if len(expected_get.keys()) !=0:
            if Operator == "Pon":
                read_data = rest_interface_module.get_request(f"/api/gponconfig/pon/getaes/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"]))
            else:
                read_data = rest_interface_module.get_request(f"/api/gponconfig/gem/getAes/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["gemId"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"set steeep IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)





def test_AES_encryption_Management(rest_interface_module, node_id):

    # for dba in dba_profile_Data_Config:
    #     DBA_Profile(rest_interface_module, node_id, dba, method='ADD')
    # for tcont in tcont_Data_Config:
    #     Tcont_Management(rest_interface_module, node_id, tcont)
    for gem in gem_profile_Data_Config:
        Gem_Management(rest_interface_module, node_id, gem)


    for aes_pon in Aes_Management_Pon_Data:
        AES_encryption_Management(rest_interface_module, node_id, aes_pon, Operator="Pon")
    for aes_gem in Aes_Management_Gem_Data:
        AES_encryption_Management(rest_interface_module, node_id, aes_gem, Operator="Gem")




    for gem in gem_profile_Data_Delete_Config:
        Gem_Management(rest_interface_module, node_id, gem)
    for tcont in tcont_Data_Delete_Config:
        Tcont_Management(rest_interface_module, node_id, tcont)
    for dba in dba_profile_Data_Config_Delete:
        DBA_Profile(rest_interface_module, node_id, dba, method='DELETE')       
                