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
from Senario.detect_onu_with_serial import detect_onu_with_Serial_number
from Pon.test_tcont_profile import Tcont_Management
from Pon.test_dba_profile import DBA_Profile
from Pon.test_gem_profile import Gem_Management
from Pon.test_OLT_Service import OLT_Service
from Pon.test_ONU_remote_Service import ONU_remote_Service

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)


priority = [0,0,0,0,1,0,0,0,2,0,3,0,7,0,3,0,2,0,0,3,0,0,5,6,6,2,0,0] #
Vlan = [333,330,229,112,224,334,338,313,226,335,227,111,221,223,115,220,114,336,110,228,117,337,118,332,331,225,119,222]#
def test_Shut_Down_On(rest_interface_module, node_id):
    # response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgeconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
    # bridge_config(rest_interface_module, node_id, Bridge_conf(1,"RSTP_VLAN_BRIDGE"), method='POST')
    # # read_data = rest_interface_module.get_request("/api/gponconfig/onu/getallonunumber?nodeId=11&shelfId=1&slotId=1")
    # # read_onu = json.loads(read_data.text)
    # # assert read_onu["totalOnu"] == 2
    # # Vlan,priority,dict_sn_onu = detect_onu_with_Serial_number(rest_interface_module,3, 1, node_id)
    # # vlan_string = ""
    # # for v in Vlan:
    # #     vlan_string = f"{v}"+vlan_string
    # # # ****************************************************************************************************************************
    # # for i in len(Vlan):
    # #     response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/vlan/getall?nodeId=11&shelfId=1&slotId=1")
    # #     vlan_config(rest_interface_module, node_id, Vlan_conf(Vlan[i], 'CUSTOMER'), method='POST')    
    # response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/vlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
    # vlan_config(rest_interface_module, node_id, Vlan_conf(700, 'CUSTOMER'), method='POST')  
    # for i in range(len(Vlan)):
    #     response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/vlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
    #     vlan_config(rest_interface_module, node_id, Vlan_conf(Vlan[i], 'CUSTOMER'), method='POST')  
    
#     for port in range(1,2):
#         response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/sp5100/bridgegroupconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
#         switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port, index=4), method='POST')
#         response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/sp5100/portvlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
#         uplink_vlan_config(rest_interface_module, node_id, uplink_vlan_conf_DATA[1]._replace(ethIfIndex=port,taggedVlanSet="700,333,330,229,112,224,334,338,313,226"), method='POST') 
#         uplink_vlan_config(rest_interface_module, node_id, uplink_vlan_conf_DATA[1]._replace(ethIfIndex=port,taggedVlanSet="335,227,111,221,223,115,220,114,336,110"), method='POST') 
#         uplink_vlan_config(rest_interface_module, node_id, uplink_vlan_conf_DATA[1]._replace(ethIfIndex=port,taggedVlanSet="228,117,337,118,332,331,225,119,222"), method='POST') 

#     #     mapping_add_1 = replace_dictionary(Mapping_Add, "set",{"ifIndex": 1, "vlanId": 10,"vlanTranslatedId": 11})
#     #     mapping_add_1 = replace_dictionary(mapping_add_1,"get", {"ifIndex":[1,"ifIndex"],"vlanId":[10,"vlanId"],"vlanTranslatedId":[11,"vlanTranslatedId"]})     
#     #     Mapping(rest_interface_module, node_id, mapping_add_1, method='ADD')

#     #     mapping_add_2 = replace_dictionary(Mapping_Add, "set",{"ifIndex": 1, "vlanId": 12,"vlanTranslatedId": 13})
#     #     mapping_add_2 = replace_dictionary(mapping_add_2,"get", {"ifIndex":[1,"ifIndex"],"vlanId":[12,"vlanId"],"vlanTranslatedId":[13,"vlanTranslatedId"]})     
#     #     Mapping(rest_interface_module, node_id, mapping_add_2, method='ADD')

# #**********************************PON Config ****************************************
#     for port in range(1,2):
#         response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/sp5100/bridgegroupconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
#         switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port+8, index=4), method='POST')
#         response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/sp5100/portvlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
#         uplink_vlan_config(rest_interface_module, node_id, uplink_vlan_conf_DATA[1]._replace(ethIfIndex=port+8, taggedVlanSet="700,333,330,229,112,224,334,338,313,226"), method='POST') 
#         uplink_vlan_config(rest_interface_module, node_id, uplink_vlan_conf_DATA[1]._replace(ethIfIndex=port+8, taggedVlanSet="335,227,111,221,223,115,220,114,336,110"), method='POST') 
#         uplink_vlan_config(rest_interface_module, node_id, uplink_vlan_conf_DATA[1]._replace(ethIfIndex=port+8, taggedVlanSet="700"), method='228,117,337,118,332,331,225,119,222') 

    response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/dbaProfile/getall?nodeId={node_id}&shelfId=1&slotId=1")
    # DBA_Profile(rest_interface_module, node_id, dba_profile(1, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":1,"name": "HSI", "dbaType": 2, "fixedBwValue": None, "assureBwValue": 250, "maxBwValue": 100000},
    #                                                        {
    #                                                         "namedba": ["dba_test1", "name"],
    #                                                         "dbatype": [2, "dbaType"],
    #                                                         "fixedbwvalue": [None, "fixedBwValue"],
    #                                                         "assurebwvalue": [250, "assureBwValue"],
    #                                                         "maxbwvalue": [100000, "maxBwValue"]},result="Pass"), method='ADD')
    # DBA_Profile(rest_interface_module, node_id, dba_profile(2, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":2,"name": "VOIP", "dbaType": 1, "fixedBwValue": None, "assureBwValue": 250, "maxBwValue": 1000},
    #                                                        {
    #                                                         "namedba": ["dba_test1", "name"],
    #                                                         "dbatype": [1, "dbaType"],
    #                                                         "fixedbwvalue": [None, "fixedBwValue"],
    #                                                         "assurebwvalue": [250, "assureBwValue"],
    #                                                         "maxbwvalue": [1000, "maxBwValue"]},result="Pass"), method='ADD')
    for port in range(1,2):
        for i in  range(20,21) :
            response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/tcont/getall?nodeId={node_id}&shelfId=1&slotId=1&portId={port}&onuId=-1")
            Tcont_Management(rest_interface_module, node_id, tcont(1, {"nodeId":None, "slotId":1,"shelfId":1,"bwProfileId":1,"bwProfileName": "HSI", "name": "tcont_valid1", "onuId": i, "portId": port, "tcontId": 1},
                                                           {
                                                            "bwProfileId": [1, "bwProfileId"],
                                                            "bwProfileName": ["HSI", "bwProfileName"],
                                                            "name": ["tcont_valid1", "name"],
                                                            "onuId": [i, "onuId"],
                                                            "portId": [port, "portId"],
                                                            "tcontId": [1, "tcontId"]},result="Pass", method="ADD"))
            Tcont_Management(rest_interface_module, node_id, tcont(1, {"nodeId":None, "slotId":1,"shelfId":1,"bwProfileId":2,"bwProfileName": "VOIP", "name": "tcont_valid2", "onuId": i, "portId": port, "tcontId": 2},
                                                           {
                                                            "bwProfileId": [2, "bwProfileId"],
                                                            "bwProfileName": ["VOIP", "bwProfileName"],
                                                            "name": ["tcont_valid2", "name"],
                                                            "onuId": [i, "onuId"],
                                                            "portId": [port, "portId"],
                                                            "tcontId": [2, "tcontId"]},result="Pass", method="ADD"))

            response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/gem/getall?nodeId={node_id}&shelfId=1&slotId=1&portId={port}&onuId={i}")
            Gem_Management(rest_interface_module, node_id, gem_profile(1, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"1","name": "gem1", "onuId": i, "portId": port, "tcontId": 1},
                                                           {
                                                            "gemid": [1, "gemId"],
                                                            "name": ["gem1", "name"],
                                                            "onuId": [i, "onuId"],
                                                            "portId": [port, "portId"],
                                                            "tcontId": [1, "tcontId"]},result="Pass",method="ADD"))
            Gem_Management(rest_interface_module, node_id, gem_profile(2, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"2","name": "gem2", "onuId": i, "portId": port, "tcontId": 2},
                                                           {
                                                            "gemid": [2, "gemId"],
                                                            "name": ["gem2", "name"],
                                                            "onuId": [i, "onuId"],
                                                            "portId": [port, "portId"],
                                                            "tcontId": [2, "tcontId"]},result="Pass",method="ADD"))

            response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/service/getall?nodeId={node_id}&shelfId=1&slotId=1&portId={port}&onuId={i}")
            OLT_Service(rest_interface_module, node_id, service_profile(1, {"nodeId":None, "slotId":1,"shelfId":1, "servicePortId": "1", "onuId": i, "portId": port, "gemId": 1, "userVlan": f"{Vlan[i-1]}"},
                                                           {
                                                            "gemId": [1, "gemId"],
                                                            "servicePortId": [1, "servicePortId"],
                                                            "onuId": [i, "onuId"],
                                                            "portId": [port, "portId"],
                                                            "userVlan": [Vlan[i-1], "userVlan"],},result="Pass",method="ADD"))
            OLT_Service(rest_interface_module, node_id, service_profile(1, {"nodeId":None, "slotId":1,"shelfId":1, "servicePortId": "2", "onuId": i, "portId": port, "gemId": 2, "userVlan": "700"},
                                                           {
                                                            "gemId": [2, "gemId"],
                                                            "servicePortId": [2, "servicePortId"],
                                                            "onuId": [i, "onuId"],
                                                            "portId": [port, "portId"],
                                                            "userVlan": [700, "userVlan"],},result="Pass",method="ADD"))

            response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/sp5100/rmonu/service/getall?nodeId={node_id}&shelfId=1&slotId=1&onuId={i}&portId={port}")
            ONU_remote_Service(rest_interface_module, node_id, remote_service(1, {
                 "nodeId": None,"shelfId": 1,"slotId": 1,"portId": port,"onuId": i, "rmServiceId": "1",
                 "onuPortType": "VEIP","onuPortId": 0,"vlanMode": "ACCESS","gemId": 1,"pvId": f"{Vlan[i-1]}","priority": f"{priority[i-1]}",}, {"rmServiceId": [1, "rmServiceId"],
                                                                                                "onuPortType": ["VEIP", "onuPortType"],
                                                                                                # "onuPortId": [0, "onuPortId"],
                                                                                                "onuId": [i, "onuId"],
                                                                                                "portId": [port, "portId"],
                                                                                                "gemId": [1, "gemId"],
                                                                                                "vlanMode": ["ACCESS", "vlanMode"],
                                                                                                "pvId": [Vlan[i-1], "pvId"],
                                                                                                "priority": [priority[i-1], "priority"],},result="Pass",method="ADD")
)
            ONU_remote_Service(rest_interface_module, node_id, remote_service(1, {
                 "nodeId": None,"shelfId": 1,"slotId": 1,"portId": port,"onuId": i, "rmServiceId": "2",
                 "onuPortType": "VEIP","onuPortId": 0,"vlanMode": "ACCESS","gemId": 2,"pvId": f"700","priority": f"5",}, {"rmServiceId": [2, "rmServiceId"],
                                                                                                "onuPortType": ["VEIP", "onuPortType"],
                                                                                                # "onuPortId": [0, "onuPortId"],
                                                                                                "onuId": [i, "onuId"],
                                                                                                "portId": [port, "portId"],
                                                                                                "gemId": [2, "gemId"],
                                                                                                "vlanMode": ["ACCESS", "vlanMode"],
                                                                                                "pvId": [700, "pvId"],
                                                                                                "priority": [5, "priority"],},result="Pass",method="ADD"))

        # for i in range(len(Onu_Number)):
        #     remote_2_del = replace_dictionary(remote_service_profile_Data_Delete[0], "set",{"rmServiceId": 1, "onuId": i, "portId": port})
        #     ONU_remote_Service(rest_interface_module, node_id, remote_2_del)
        #     remote_1_del = replace_dictionary(remote_service_profile_Data_Delete[0], "set",{"rmServiceId": 2, "onuId": i, "portId": port})
        #     ONU_remote_Service(rest_interface_module, node_id, remote_1_del)

        #     service_1_del = replace_dictionary(service_profile_Data_Delete_Config[0], "set",{"servicePortId": 1, "onuId": i, "portId": port})
        #     OLT_Service(rest_interface_module, node_id, service_1_del)
        #     service_2_del = replace_dictionary(service_profile_Data_Delete_Config[0], "set",{"servicePortId": 2, "onuId": i, "portId": port})
        #     OLT_Service(rest_interface_module, node_id, service_2_del)

        #     gem_2_del = replace_dictionary(gem_profile_Data_Delete_Config[0], "set",{"gemId":"2","name": "", "onuId": i, "portId": port, "tcontId": 4})
        #     Gem_Management(rest_interface_module, node_id, gem_2_del)
        #     gem_1_del = replace_dictionary(gem_profile_Data_Delete_Config[0], "set",{"gemId":"1","name": "", "onuId": i, "portId": port, "tcontId": 2})
        #     Gem_Management(rest_interface_module, node_id, gem_1_del)

        #     tcont_2_del = replace_dictionary(tcont_Data_Delete_Config[0], "set",{"onuId": i, "portId": port, "tcontId": 4})
        #     Gem_Management(rest_interface_module, node_id, tcont_2_del)
        #     tcont_1_del = replace_dictionary(tcont_Data_Delete_Config[0], "set",{"onuId": i, "portId": port, "tcontId": 2})
        #     Gem_Management(rest_interface_module, node_id, tcont_1_del)
        # # mapping_add_1 = replace_dictionary(Mapping_Add, "set",{"ifIndex": port+8, "vlanId": 10,"vlanTranslatedId": 11})
        # # mapping_add_1 = replace_dictionary(mapping_add_1,"get", {"ifIndex":[port+8,"ifIndex"],"vlanId":[10,"vlanId"],"vlanTranslatedId":[11,"vlanTranslatedId"]})     
        # # Mapping(rest_interface_module, node_id, mapping_add_1, method='ADD')

        # # mapping_add_2 = replace_dictionary(Mapping_Add, "set",{"ifIndex": port+8, "vlanId": 12,"vlanTranslatedId": 13})
        # # mapping_add_2 = replace_dictionary(mapping_add_2,"get", {"ifIndex":[port+8,"ifIndex"],"vlanId":[12,"vlanId"],"vlanTranslatedId":[13,"vlanTranslatedId"]})     
        # # Mapping(rest_interface_module, node_id, mapping_add_2, method='ADD')

#**********************************PON UNconfig ****************************************
    # for port in range(2,3):
    #     # mapping_del_1 = replace_dictionary(Mapping_Delete, "set",{"ifIndex": port+8, "vlanId": 10,"vlanTranslatedId": 11})
    #     # Mapping(rest_interface_module, node_id, mapping_del_1, method='DELETE')
    #     # mapping_del_2 = replace_dictionary(Mapping_Delete, "set",{"ifIndex": port+8, "vlanId": 12,"vlanTranslatedId": 13})
    #     # Mapping(rest_interface_module, node_id, mapping_del_2, method='DELETE')
    #     uplink_vlan_config(rest_interface_module, node_id, uplink_vlan_conf_DATA[1]._replace(ethIfIndex=port+8), method='DELETE')   
    #     switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port+8, index=9), method='DELETE')
    #     pon_shut = replace_dictionary(pon_init_info_shutdown, "set", {"portId":port,"ifIndex":port})
    #     pon_shut = replace_dictionary(pon_shut,"get", {"portId":[port,"portId"],"ifIndex":[port,"ifIndex"]})   
    #     Pon_Initial_Information(rest_interface_module, node_id, pon_shut, method='UPDATE')  

#**********************************Switch UNconfig ****************************************

    # for port in range(1,2):
    #     mapping_del_1 = replace_dictionary(Mapping_Delete, "set",{"ifIndex": port, "vlanId": 10,"vlanTranslatedId": 11})
    #     Mapping(rest_interface_module, node_id, mapping_del_1, method='DELETE')

    #     mapping_del_2 = replace_dictionary(Mapping_Delete, "set",{"ifIndex": port, "vlanId": 12,"vlanTranslatedId": 13})
    #     Mapping(rest_interface_module, node_id, mapping_del_2, method='DELETE')

    # for port in range(1,2):
    #     uplink_vlan_config(rest_interface_module, node_id, uplink_vlan_conf_DATA[1]._replace(ethIfIndex=port), method='DELETE')   
    #     switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port, index=9), method='DELETE')
    # for i in len(Vlan):
    #     vlan_config(rest_interface_module, node_id, Vlan_conf(Vlan[i], 'CUSTOMER'), method='DELETE')    

    # # #****************************************************************************************************************************
    # bridge_config(rest_interface_module, node_id, Bridge_conf(), method='DELETE')      


   