import pytest
import logging
import json
from config import *
from conftest import *
from Pon.test_Pon_Initial_Information import Pon_Initial_Information
from Pon.test_onu_auto_learn import read_only_Onu_State
from Switch.test_Mapping import Mapping
from Switch.bridge_funcs import bridge_config
from Switch.test_vlan import vlan_config
from Switch.test_Bridge_group_conf import switch_config
from Switch.test_uplink_port_Vlan_conf import uplink_vlan_config
from Pon.test_tcont_profile import Tcont_Management
from Pon.test_dba_profile import DBA_Profile
from Pon.test_gem_profile import Gem_Management
from Pon.test_OLT_Service_Translate import OLT_Service
from Pon.test_ONU_remote_Service import ONU_remote_Service
import time

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Vlan_From_Serial_Of_ONUs ={2: [11], 3: [10]} 

def test_Vlan_Translate(rest_interface_module, node_id):
    PORT_INFORMATION = {9:40}
#**********************************PON Config ****************************************
    response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/sp5100/bridgegroupconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
    switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=9+8, index=4), method='POST')
    response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/sp5100/portvlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
    uplink_vlan_config(rest_interface_module, node_id, uplink_vlan_conf_DATA[1]._replace(ethIfIndex=9+8,taggedVlanSet="700,702,900,902"), method='POST') 
    
    response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/dbaProfile/getall?nodeId={node_id}&shelfId=1&slotId=1")
    # DBA_Profile(rest_interface_module, node_id, dba_profile(1, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":1,"name": "VOIP", "dbaType": 3, "fixedBwValue": None, "assureBwValue": 250, "maxBwValue": 100000},
    #                                                        {
    #                                                         "namedba": ["VOIP", "name"],
    #                                                         "dbatype": [3, "dbaType"],
    #                                                         "fixedbwvalue": [0, "fixedBwValue"],
    #                                                         "assurebwvalue": [250, "assureBwValue"],
    #                                                         "maxbwvalue": [100000, "maxBwValue"]},result="Pass"), method='ADD')
    for PORT,Number_of_Onus in PORT_INFORMATION.items():
        for i in range(Number_of_Onus) :
            response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/tcont/getall?nodeId={node_id}&shelfId=1&slotId=1&portId={PORT}&onuId=-1")
            Tcont_Management(rest_interface_module, node_id, tcont(1, {"nodeId":None, "slotId":1,"shelfId":1,"bwProfileId":1,"bwProfileName": "VOIP", "name": "tcont_valid1", "onuId": i+1, "portId": PORT, "tcontId": 1},
                                                           {"bwProfileId": [1, "bwProfileId"],
                                                            "bwProfileName": ["VOIP", "bwProfileName"],
                                                            "name": ["tcont_valid1", "name"],
                                                            "onuId": [i+1, "onuId"],
                                                            "portId": [PORT, "portId"],
                                                            "tcontId": [1, "tcontId"]},result="Pass", method="ADD"))
            response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/gem/getall?nodeId={node_id}&shelfId=1&slotId=1&portId={PORT}&onuId={i+1}")
            Gem_Management(rest_interface_module, node_id, gem_profile(1, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"1","name": "gem1", "onuId": i+1, "portId": PORT, "tcontId": 1},
                                                           {
                                                            "gemid": [1, "gemId"],
                                                            "name": ["gem1", "name"],
                                                            "onuId": [i+1, "onuId"],
                                                            "portId": [PORT, "portId"],
                                                            "tcontId": [1, "tcontId"]},result="Pass",method="ADD"))
            response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/service/getall?nodeId={node_id}&shelfId=1&slotId=1&portId={PORT}&onuId={i+1}")

            
            OLT_Service(rest_interface_module, node_id, service_profile(1, {
                                    "nodeId": None,"shelfId": 1,"slotId": 1,"portId": PORT,"onuId": i+1,"servicePortId": 1,"gemId": 1,"vlan": 702,"svlan": 0,"userVlan": "700",
                                    "innerVlan": 0,"vlanAction": "VLAN_TRANSLATE","vlanPriority": 0,"svlanPriority": 0,"vlanPriorityAction": "1","svlanPriorityAction": "1","queue": 0,
                                    "cosQueueProfileId": 0,"queueSelectMode": 0,"upLinkC2CId": 0,"downLinkC2CId": 0,"deviceType": 0,"isServiceProfile": True,"errorCode": 0},
                                                           {"portId": [PORT, "portId"],
                                                            "onuId": [i+1, "onuId"],
                                                            "servicePortId": [1,"servicePortId"],
                                                            "gemId": [1, "gemId"],
                                                            "vlan": [702,"vlan"],
                                                            "userVlan": [700,"userVlan"],
                                                            "vlanAction": ["VLAN_TRANSLATE", 'vlanAction']},result="Pass",method="ADD"))

            response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/sp5100/rmonu/service/getall?nodeId={node_id}&shelfId=1&slotId=1&onuId={i+1}&portId={PORT}")
            ONU_remote_Service(rest_interface_module, node_id, remote_service(1, {
                 "nodeId": None,"shelfId": 1,"slotId": 1,"portId": PORT,"onuId": i+1, "rmServiceId": "1",
                 "onuPortType": "VEIP","onuPortId": 0,"vlanMode": "ACCESS","gemId": 1,"pvId": "700","priority": "0",}, {"rmServiceId": [1, "rmServiceId"],
                                                                                                "onuPortType": ["VEIP", "onuPortType"],
                                                                                                # "onuPortId": [0, "onuPortId"],
                                                                                                "onuId": [i+1, "onuId"],
                                                                                                "portId": [PORT, "portId"],
                                                                                                "gemId": [1, "gemId"],
                                                                                                "vlanMode": ["ACCESS", "vlanMode"],
                                                                                                "pvId": [700, "pvId"],
                                                                                                "priority":[ 0, "priority"],},result="Pass",method="ADD")
)
            
            response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/tcont/getall?nodeId={node_id}&shelfId=1&slotId=1&portId={PORT}&onuId=-1")
            Tcont_Management(rest_interface_module, node_id, tcont(1, {"nodeId":None, "slotId":1,"shelfId":1,"bwProfileId":2,"bwProfileName": "HSI", "name": "tcont_valid2", "onuId": i+1, "portId": PORT, "tcontId": 2},
                                                           {"bwProfileId": [2, "bwProfileId"],
                                                            "bwProfileName": ["HSI", "bwProfileName"],
                                                            "name": ["tcont_valid2", "name"],
                                                            "onuId": [i+1, "onuId"],
                                                            "portId": [PORT, "portId"],
                                                            "tcontId": [2, "tcontId"]},result="Pass", method="ADD"))
            response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/gem/getall?nodeId={node_id}&shelfId=1&slotId=1&portId={PORT}&onuId={i+1}")
            Gem_Management(rest_interface_module, node_id, gem_profile(1, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"2","name": "gem2", "onuId": i+1, "portId": PORT, "tcontId": 2},
                                                           {
                                                            "gemid": [2, "gemId"],
                                                            "name": ["gem2", "name"],
                                                            "onuId": [i+1, "onuId"],
                                                            "portId": [PORT, "portId"],
                                                            "tcontId": [2, "tcontId"]},result="Pass",method="ADD"))
            response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/service/getall?nodeId={node_id}&shelfId=1&slotId=1&portId={PORT}&onuId={i+1}")
            OLT_Service(rest_interface_module, node_id, service_profile(1, {
                                    "nodeId": None,"shelfId": 1,"slotId": 1,"portId": PORT,"onuId": i+1,"servicePortId": 2,"gemId": 2,"vlan": 902,"svlan": 0,"userVlan": "900",
                                    "innerVlan": 0,"vlanAction": "VLAN_TRANSLATE","vlanPriority": 0,"svlanPriority": 0,"vlanPriorityAction": "1","svlanPriorityAction": "1","queue": 0,
                                    "cosQueueProfileId": 0,"queueSelectMode": 0,"upLinkC2CId": 0,"downLinkC2CId": 0,"deviceType": 0,"isServiceProfile": True,"errorCode": 0},
                                                           {"portId": [PORT, "portId"],
                                                            "onuId": [i+1, "onuId"],
                                                            "servicePortId": [2,"servicePortId"],
                                                            "gemId": [2, "gemId"],
                                                            "vlan": [902,"vlan"],
                                                            "userVlan": [900,"userVlan"],
                                                            "vlanAction": ["VLAN_TRANSLATE", 'vlanAction']},result="Pass",method="ADD"))

            response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/sp5100/rmonu/service/getall?nodeId={node_id}&shelfId=1&slotId=1&onuId={i+1}&portId={PORT}")
            ONU_remote_Service(rest_interface_module, node_id, remote_service(1, {
                 "nodeId": None,"shelfId": 1,"slotId": 1,"portId": PORT,"onuId": i+1, "rmServiceId": "2",
                 "onuPortType": "VEIP","onuPortId": 0,"vlanMode": "ACCESS","gemId": 1,"pvId": "900","priority": "0",}, {"rmServiceId": [2, "rmServiceId"],
                                                                                                "onuPortType": ["VEIP", "onuPortType"],
                                                                                                # "onuPortId": [0, "onuPortId"],
                                                                                                "onuId": [i+1, "onuId"],
                                                                                                "portId": [PORT, "portId"],
                                                                                                "gemId": [2, "gemId"],
                                                                                                "vlanMode": ["ACCESS", "vlanMode"],
                                                                                                "pvId": [900, "pvId"],
                                                                                                "priority":[ 0, "priority"],},result="Pass",method="ADD")
)
    
    time.sleep(2)
    for PORT,Number_of_Onus in PORT_INFORMATION.items():
        for i in  range(Number_of_Onus) :
            response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/sp5100/rmonu/service/getall?nodeId={node_id}&shelfId=1&slotId=1&onuId={i+1}&portId={PORT}")
            ONU_remote_Service(rest_interface_module, node_id, 
            remote_service(1, {"nodeId":None, "slotId":1,"shelfId":1, "rmServiceId": 1, "onuId": i+1, "portId": PORT},result="Pass",method="DELETE"))
            
            response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/service/getall?nodeId={node_id}&shelfId=1&slotId=1&portId={PORT}&onuId={i+1}")
            OLT_Service(rest_interface_module, node_id, 
            service_profile(1, {"nodeId":None, "slotId":1,"shelfId":1, "servicePortId": 1, "onuId": i+1, "portId": PORT},result="Pass",method="DELETE"))
            
            response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/gem/getall?nodeId={node_id}&shelfId=1&slotId=1&portId={PORT}&onuId={i+1}")
            Gem_Management(rest_interface_module, node_id,gem_profile(1, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"1","name": "gem1", "onuId": i+1, "portId": PORT, "tcontId": 1},result="Pass",method="DELETE"))

            response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/tcont/getall?nodeId={node_id}&shelfId=1&slotId=1&portId={PORT}&onuId=-1")
            Tcont_Management(rest_interface_module, node_id,tcont(1, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": i+1, "portId": PORT, "tcontId": 1},result="Pass",method="DELETE"))
            
            response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/sp5100/rmonu/service/getall?nodeId={node_id}&shelfId=1&slotId=1&onuId={i+1}&portId={PORT}")
            ONU_remote_Service(rest_interface_module, node_id, 
            remote_service(1, {"nodeId":None, "slotId":1,"shelfId":1, "rmServiceId": 2, "onuId": i+1, "portId": PORT},result="Pass",method="DELETE"))
            
            response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/service/getall?nodeId={node_id}&shelfId=1&slotId=1&portId={PORT}&onuId={i+1}")
            OLT_Service(rest_interface_module, node_id, 
            service_profile(1, {"nodeId":None, "slotId":1,"shelfId":1, "servicePortId": 2, "onuId": i+1, "portId": PORT},result="Pass",method="DELETE"))
            
            response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/gem/getall?nodeId={node_id}&shelfId=1&slotId=1&portId={PORT}&onuId={i+1}")
            Gem_Management(rest_interface_module, node_id,gem_profile(1, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"2","name": "gem2", "onuId": i+1, "portId": PORT, "tcontId": 2},result="Pass",method="DELETE"))

            response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/tcont/getall?nodeId={node_id}&shelfId=1&slotId=1&portId={PORT}&onuId=-1")
            Tcont_Management(rest_interface_module, node_id,tcont(1, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": i+1, "portId": PORT, "tcontId": 2},result="Pass",method="DELETE"))
    

#     DBA_Profile(rest_interface_module, node_id, dba_profile(1, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":1}, result="Pass"), method='DELETE')       

# #**********************************PON UNconfig ****************************************
#     uplink_vlan_config(rest_interface_module, node_id, uplink_vlan_conf(9+8, None, "TRUNK", -1, "" , "700,702,900,902", "", -1, "Pass"), method='POST')
#     switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=9+8, index=9), method='DELETE')

   