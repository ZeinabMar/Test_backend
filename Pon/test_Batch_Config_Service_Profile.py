import pytest
import logging
import json
from config import *
from conftest import *
from Pon.test_tcont_profile import Tcont_Management
from Pon.test_dba_profile import DBA_Profile
from Pon.test_Service_Profile_Definition import Service_Profile_Definition
from Switch.bridge_funcs import bridge_config
from Switch.test_vlan import vlan_config
from Pon.test_Service_Profile_Tcont import Tcont_Service_Profile
from Pon.test_Service_Profile_Gem import Gem_Service_Profile
from Pon.test_Service_Profile_OLT import Olt_Service_Profile
from Pon.test_Service_Profile_Onu_Remote import Remote_Service_Profile

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)


batch_config = namedtuple('batch_config', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
batch_config.__new__.__defaults__ = (None, {}, {},None, None)



batch_config_Data = (
batch_config(1, {"nodeId": None,"shelfId": 1, "slotId": 1,"onuServiceProfileId": 1, "portId": 2,"onuRange": 1,},result="Pass",method="ADD"),
# batch_config(2, {"nodeId": None,"shelfId": 1, "slotId": 1,"onuServiceProfileId": 1, "portId": 3,"onuRange": 1,},result="Pass",method="ADD"),
)  

batch_config_Delete = (
    batch_config(1, {"nodeId": None,"shelfId": 1, "slotId": 1,"onuServiceProfileId": 1, "portId": 2},result="Pass",method="DELETE"),
    # batch_config(2, {"nodeId": None,"shelfId": 1, "slotId": 1,"onuServiceProfileId": 1, "portId": 3},result="Pass",method="DELETE"),
)

def Batch_Config(rest_interface_module, node_id, batch_config_data=batch_config(), method='ADD'):
    method = batch_config_data.method
    logger.info(f'SERVICE Batch_Config TEST DATA ------- > {batch_config_data.index}')
    expected_set = batch_config_data.expected_result_Set
    expected_set["nodeId"]= int(node_id)
    expected_get = batch_config_data.expected_result_Get  

    logger.info(f"TRY TO {method} Batch_Config CONFIG ...")
    if method == 'ADD':
        url = "/api/gponconfig/onu/batchconfig"+"?nodeId="+str(expected_set["nodeId"])+"&shelfId="+str(expected_set["shelfId"])+"&slotId="+str(expected_set["slotId"])+"&portId="+str(expected_set["portId"])+"&onuServiceProfileId="+str(expected_set["onuServiceProfileId"])+"&onuRange="+str(expected_set["onuRange"])
        response = rest_interface_module.post_request(url, None)    
    else:  # method==DELETE   
        url = f"/api/gponconfig/onu/batchconfig/delete/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])
        response = rest_interface_module.delete_request(url)

    if batch_config_data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in Batch_Config {expected_set}'
    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in Batch_Config {service_data._asdict}'



def test_Batch_Config(rest_interface_module, node_id):

    bridge_config(rest_interface_module, node_id, Bridge_conf(), method='POST')
    # ****************************************************************************************************************************
    for vlan in VLAN_DATA_conf_CUSTOM:
        vlan_config(rest_interface_module, node_id, vlan, method='POST')  

    for dba in dba_profile_Data_Config:
        DBA_Profile(rest_interface_module, node_id, dba, method='ADD')
    for service_def in Onu_Service_Profile_Data_Config:
        Service_Profile_Definition(rest_interface_module, node_id, service_def, method='ADD')
    for service_tcont in Tcont_service_profile_Data_Config:
        Tcont_Service_Profile(rest_interface_module, node_id, service_tcont)
    for service_gem in Gem_service_profile_Data_Config:
        Gem_Service_Profile(rest_interface_module, node_id, service_gem)
    for olt_service_p in olt_service_profile_Data_Config:
        Olt_Service_Profile(rest_interface_module, node_id, olt_service_p)
    for remote_p in remote_service_profile_Data_Config:
        Remote_Service_Profile(rest_interface_module, node_id, remote_p)
    for batch in batch_config_Data:
        Batch_Config(rest_interface_module, node_id, batch)

    get_rest(rest_interface_module, "TCONT", {"bwProfileId": [1, "bwProfileId"],
                                     "bwProfileName": ["dba_type1", "bwProfileName"],
                                     "name": ["test_tcont1", "name"],
                                     "onuId": [1, "onuId"],
                                     "portId": [2, "portId"],
                                     "tcontId": [1, "tcontId"]}, "/api/gponconfig/tcont/get", ["nodeId", node_id],["shelfId", 1], ["slotId", 1], ["portId", 2], ["onuId", 1], ["tcontId", 1])    
    get_rest(rest_interface_module, "GEM",  {"gemid": [1, "gemId"],
                                     "name": ["test_gem1", "name"],
                                     "onuId": [1, "onuId"],
                                     "portId": [2, "portId"],
                                     "tcontId": [1, "tcontId"]}, "/api//gponconfig/gem/get", ["nodeId", node_id],["shelfId", 1], ["slotId", 1], ["portId", 2], ["onuId", 1], ["gemId", 1])    
    get_rest(rest_interface_module, "SERVICE", {"gemId": [1, "gemId"],
                                     "servicePortId": [1, "servicePortId"],
                                     "onuId": [1, "onuId"],
                                     "portId": [2, "portId"],
                                     "userVlan": [10, "userVlan"],}, "/api/gponconfig/service/get", ["nodeId", node_id],["shelfId", 1], ["slotId", 1], ["portId", 2], ["onuId", 1], ["servicePortId", 1])    
    get_rest(rest_interface_module, "REMOTE", {"rmServiceId": [1, "rmServiceId"],
                                     "onuPortType": ["VEIP", "onuPortType"],
                                     "onuPortId": [0, "onuPortId"],
                                     "onuId": [1, "onuId"],
                                     "portId": [2, "portId"],
                                     "gemId": [1, "gemId"],
                                     "vlanMode": ["ACCESS", "vlanMode"],
                                     "pvId": [10, "pvId"],
                                     "priority": [1, "priority"],}, "/api/gponconfig/sp5100/rmonu/service/get", ["nodeId", node_id],["shelfId", 1], ["slotId", 1], ["portId", 2], ["onuId", 1], ["rmServiceId", 1])    

    for batch in batch_config_Delete:
        Batch_Config(rest_interface_module, node_id, batch)
    for remote_p in remote_service_profile_Delete_Config:
        Remote_Service_Profile(rest_interface_module, node_id, remote_p)
    for olt_service_p in olt_service_profile_Delete_Config:
        Olt_Service_Profile(rest_interface_module, node_id, olt_service_p)    
    for service_gem in Gem_service_profile_Delete_Config:
        Gem_Service_Profile(rest_interface_module, node_id, service_gem)
    for service_tcont in Tcont_service_profile_Delete_Config:
        Tcont_Service_Profile(rest_interface_module, node_id, service_tcont)
    for service_def in Onu_Service_Profile_Delete_Config:
        Service_Profile_Definition(rest_interface_module, node_id, service_def, method='DELETE')    
    for dba in dba_profile_Data_Config_Delete:
        DBA_Profile(rest_interface_module, node_id, dba, method='DELETE')      

    for vlan in VLAN_DATA_conf_CUSTOM:
        vlan_config(rest_interface_module, node_id, vlan, method='DELETE')  
    #****************************************************************************************************************************
    bridge_config(rest_interface_module, node_id, Bridge_conf(), method='DELETE')    