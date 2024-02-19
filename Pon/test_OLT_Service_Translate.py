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
import time


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)

service_olt = namedtuple('service_olt', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
service_olt.__new__.__defaults__ = (None, {}, {},None, None)

service_olt_Data = (
service_olt(1,{
  "nodeId": 45,
  "shelfId": 1,
  "slotId": 1,
  "portId": 2,
  "onuId": 1,
  "servicePortId": 1,
  "gemId": 1,
  "vlan": 11,
  "svlan": 0,
  "userVlan": 10,
  "innerVlan": 0,
  "vlanAction": "VLAN_TRANSLATE",
  "vlanPriority": 0,
  "svlanPriority": 0,
  "vlanPriorityAction": "1",
  "svlanPriorityAction": "1",
  "queue": 0,
  "cosQueueProfileId": 0,
  "queueSelectMode": 0,
  "upLinkC2CId": 0,
  "downLinkC2CId": 0,
  "deviceType": 0,
  "isServiceProfile": True,
  "errorCode": 0}, {                        "portId": [2, "portId"],
                                            "onuId": [1, "onuId"],
                                            "servicePortId": [1,"servicePortId"],
                                            "gemId": [1, "gemId"],
                                            "vlan": [11,"vlan"],
                                            "userVlan": [10,"userVlan"],
                                            "vlanAction": ["VLAN_TRANSLATE", 'vlanAction']},result="Pass",method="ADD"), 
service_olt(2,{
  "nodeId": 45,
  "shelfId": 1,
  "slotId": 1,
  "portId": 2,
  "onuId": 1,
  "servicePortId": 2,
  "gemId": 1,
  "vlan": 0,
  "svlan": 0,
  "userVlan": 10,
  "innerVlan": 0,
  "vlanAction": "VLAN_TRANSPARENT",
  "vlanPriority": 0,
  "svlanPriority": 0,
  "vlanPriorityAction": "1",
  "svlanPriorityAction": "1",
  "queue": 0,
  "cosQueueProfileId": 0,
  "queueSelectMode": 0,
  "upLinkC2CId": 0,
  "downLinkC2CId": 0,
  "deviceType": 0,
  "isServiceProfile": True,
  "errorCode": 0}, {                        "portId": [2, "portId"],
                                            "onuId": [1, "onuId"],
                                            "servicePortId": [2,"servicePortId"],
                                            "gemId": [1, "gemId"],
                                            "vlan": [-2,"vlan"],
                                            "userVlan": [10,"userVlan"],
                                            "vlanAction": ["VLAN_TRANSPARENT", 'vlanAction']},result="Pass",method="ADD"), 

service_olt(3,{
  "nodeId": 45,
  "shelfId": 1,
  "slotId": 1,
  "portId": 2,
  "onuId": 1,
  "servicePortId": 1,
  "gemId": 1,
  "vlan": 11,
  "svlan": 0,
  "userVlan": 11,
  "innerVlan": 0,
  "vlanAction": "VLAN_TRANSLATE",
  "vlanPriority": 0,
  "svlanPriority": 0,
  "vlanPriorityAction": "1",
  "svlanPriorityAction": "1",
  "queue": 0,
  "cosQueueProfileId": 0,
  "queueSelectMode": 0,
  "upLinkC2CId": 0,
  "downLinkC2CId": 0,
  "deviceType": 0,
  "isServiceProfile": True,
  "errorCode": 0}, {                        "portId": [2, "portId"],
                                            "onuId": [1, "onuId"],
                                            "servicePortId": [1,"servicePortId"],
                                            "gemId": [1, "gemId"],
                                            "vlan": [11,"vlan"],
                                            "userVlan": [10,"userVlan"],
                                            "vlanAction": ["VLAN_TRANSLATE", 'vlanAction']},result="Fail",method="ADD"), #service ID repeated  

  service_olt(4,{
  "nodeId": 45,
  "shelfId": 1,
  "slotId": 1,
  "portId": 2,
  "onuId": 1,
  "servicePortId": 3,
  "gemId": 1,
  "vlan": 11,
  "svlan": 0,
  "userVlan": 11,
  "innerVlan": 0,
  "vlanAction": "VLAN_TRANSLATE",
  "vlanPriority": 0,
  "svlanPriority": 0,
  "vlanPriorityAction": "1",
  "svlanPriorityAction": "1",
  "queue": 0,
  "cosQueueProfileId": 0,
  "queueSelectMode": 0,
  "upLinkC2CId": 0,
  "downLinkC2CId": 0,
  "deviceType": 0,
  "isServiceProfile": True,
  "errorCode": 0}, {                        "portId": [2, "portId"],
                                            "onuId": [1, "onuId"],
                                            "servicePortId": [3,"servicePortId"],
                                            "gemId": [1, "gemId"],
                                            "vlan": [11,"vlan"],
                                            "userVlan": [11,"userVlan"],
                                            "vlanAction": ["VLAN_TRANSLATE", 'vlanAction']},result="Pass",method="ADD"),    

  service_olt(5,{
  "nodeId": 45,
  "shelfId": 1,
  "slotId": 1,
  "portId": 2,
  "onuId": 1,
  "servicePortId": 3,
  "gemId": 1,
  "vlan": 12,
  "svlan": 0,
  "userVlan": 10,
  "innerVlan": 0,
  "vlanAction": "VLAN_TRANSLATE",
  "vlanPriority": 0,
  "svlanPriority": 0,
  "vlanPriorityAction": "1",
  "svlanPriorityAction": "1",
  "queue": 0,
  "cosQueueProfileId": 0,
  "queueSelectMode": 0,
  "upLinkC2CId": 0,
  "downLinkC2CId": 0,
  "deviceType": 0,
  "isServiceProfile": True,
  "errorCode": 0} ,{"lengetall":3},result="Fail",method="ADD"), 
)   
  
service_olt_Data_Delete = (
    service_olt(1, {"nodeId":None, "slotId":1,"shelfId":1, "servicePortId": 1, "onuId": 1, "portId": 2},result="Pass",method="DELETE"),  
    service_olt(2, {"nodeId":None, "slotId":1,"shelfId":1, "servicePortId": 2, "onuId": 1, "portId": 2},result="Pass",method="DELETE"),  
    service_olt(3, {"nodeId":None, "slotId":1,"shelfId":1, "servicePortId": 3, "onuId": 1, "portId": 2},result="Pass",method="DELETE"),  
)

def OLT_Service(rest_interface_module, node_id, service_olt_data=service_olt(), method='ADD'):
    method = service_olt_data.method
    logger.info(f'SERVICE OLT TEST DATA ------- > {service_olt_data.index}')
    expected_set = service_olt_data.expected_result_Set
    expected_set["nodeId"]= node_id
    expected_get = service_olt_data.expected_result_Get  

    logger.info(f"TRY TO {method} SERVICE OLT CONFIG ...")
    if method == 'ADD':
        url = "/api/gponconfig/service/add"
        response = rest_interface_module.post_request(url, expected_set)    
    else:  # method==DELETE   
        url = f"/api/gponconfig/service/delete/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["servicePortId"])
        response = rest_interface_module.delete_request(url)

    if service_olt_data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in SERVICE OLT config {expected_set}'
        if response.status_code != 200:
            logger.error(response.message)
        #**********************************************************************
        if len(expected_get.keys()) !=0:
            logger.info(f' GETTING SERVICE OLT (after {method} method) ... ')
            read_data = rest_interface_module.get_request(f"/api/gponconfig/service/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["servicePortId"]))
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"{method} IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
            logger.info(f'check is completed in {method} method')

    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in SERVICE OLT {expected_set}'
        if len(expected_get.keys()) !=0:
            logger.info(f'HIIIII {expected_get.keys()}')
            if expected_get.keys() != dict_keys(['lengetall']):
                read_data = rest_interface_module.get_request(f"/api/gponconfig/service/get/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"])+"/"+str(expected_set["servicePortId"]))
                input_data = json.loads(read_data.text)
                for key in expected_get.keys():
                    logger.info(f"set steeep IN {expected_get[key]}")
                    check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
            else:
                read_data = rest_interface_module.get_request(f"/api/gponconfig/service/getall+?nodeId="+str(expected_set["nodeId"])+"&shelfId="+str(expected_set["shelfId"])+"&slotId="+str(expected_set["slotId"])+"&portId="+str(expected_set["portId"])+"&onuId="+str(expected_set["onuId"]))
                input_data = json.loads(read_data.text)
                assert len(input_data)==expected_get["lengetall"]
                        





def test_OLT_Service(rest_interface_module, node_id):
    # response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgeconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
    # bridge_config(rest_interface_module, node_id, Bridge_conf(), method='POST')
    # # ****************************************************************************************************************************
    # response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/vlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
    # for vlan in VLAN_DATA_conf_CUSTOM:
    #     vlan_config(rest_interface_module, node_id, vlan, method='POST')  
    # response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/dbaProfile/getall?nodeId={node_id}&shelfId=1&slotId=1")
    # for dba in dba_profile_Data_Config:
    #     DBA_Profile(rest_interface_module, node_id, dba, method='ADD')
    # response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/tcont/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=2&onuId=-1")
    # response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/tcont/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=3&onuId=-1")
    # for tcont in tcont_Data_Config:
    #     Tcont_Management(rest_interface_module, node_id, tcont)
    # response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/gem/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=2&onuId=1")
    # response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/gem/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=3&onuId=1")
    # for gem in gem_profile_Data_Config:
    #     Gem_Management(rest_interface_module, node_id, gem)

    for serviceolt in service_olt_Data:
        response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/service/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=2&onuId=1")
        response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/service/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=3&onuId=1")
        OLT_Service(rest_interface_module, node_id, serviceolt)

    # for serviceolt in service_olt_Data_Delete:
    #     response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/service/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=2&onuId=1")
    #     response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/service/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=3&onuId=1")
    #     time.sleep(4)
    #     OLT_Service(rest_interface_module, node_id, serviceolt)

    # for gem in gem_profile_Data_Delete_Config:
    #     response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/gem/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=2&onuId=1")
    #     response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/gem/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=3&onuId=1")
    #     time.sleep(2)
    #     Gem_Management(rest_interface_module, node_id, gem)

    # for tcont in tcont_Data_Delete_Config:
    #     response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/tcont/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=2&onuId=-1")
    #     response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/tcont/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=3&onuId=-1")
    #     time.sleep(2)
    #     Tcont_Management(rest_interface_module, node_id, tcont)

    # response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/dbaProfile/getall?nodeId={node_id}&shelfId=1&slotId=1")
    # for dba in dba_profile_Data_Config_Delete:
    #     DBA_Profile(rest_interface_module, node_id, dba, method='DELETE')       
    # response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/vlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
    # for vlan in VLAN_DATA_conf_CUSTOM:
    #     vlan_config(rest_interface_module, node_id, vlan, method='DELETE')  
    # #****************************************************************************************************************************
    # bridge_config(rest_interface_module, node_id, Bridge_conf(), method='DELETE')    