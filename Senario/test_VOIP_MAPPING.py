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

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)



def test_Shut_Down_On(rest_interface_module, node_id):
    # response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/bridgeconfig/getall?nodeId=11&shelfId=1&slotId=1")
    # bridge_config(rest_interface_module, node_id, Bridge_conf(), method='POST')
    read_data = rest_interface_module.get_request("/api/gponconfig/onu/getallonunumber?nodeId=11&shelfId=1&slotId=1")
    read_onu = json.loads(read_data.text)
    assert read_onu["totalOnu"] == 2
    Vlan,priority,dict_sn_onu = detect_onu_with_Serial_number(rest_interface_module,3, 1, node_id)
    vlan_string = ""
    for v in Vlan:
        vlan_string = f"{v}"+vlan_string
    # # ****************************************************************************************************************************
    for i in len(Vlan):
        response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/vlan/getall?nodeId=11&shelfId=1&slotId=1")
        vlan_config(rest_interface_module, node_id, Vlan_conf(Vlan[i], 'CUSTOMER'), method='POST')    
    vlan_config(rest_interface_module, node_id, Vlan_conf(700, 'CUSTOMER'), method='POST')            
    for port in range(1,2):
        response = getall_and_update_condition(rest_interface_module, "/api/gponconfig/sp5100/bridgegroupconfig/getall?nodeId=11&shelfId=1&slotId=1")
        switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port, index=4), method='POST')
        response = getall_and_update_condition(rest_interface_module, "/api/gponconfig/sp5100/portvlan/getall?nodeId=11&shelfId=1&slotId=1")
        uplink_vlan_config(rest_interface_module, node_id, uplink_vlan_conf_DATA[1]._replace(ethIfIndex=port,taggedVlanSet=vlan_string+",700"), method='POST') 

    #     mapping_add_1 = replace_dictionary(Mapping_Add, "set",{"ifIndex": 1, "vlanId": 10,"vlanTranslatedId": 11})
    #     mapping_add_1 = replace_dictionary(mapping_add_1,"get", {"ifIndex":[1,"ifIndex"],"vlanId":[10,"vlanId"],"vlanTranslatedId":[11,"vlanTranslatedId"]})     
    #     Mapping(rest_interface_module, node_id, mapping_add_1, method='ADD')

    #     mapping_add_2 = replace_dictionary(Mapping_Add, "set",{"ifIndex": 1, "vlanId": 12,"vlanTranslatedId": 13})
    #     mapping_add_2 = replace_dictionary(mapping_add_2,"get", {"ifIndex":[1,"ifIndex"],"vlanId":[12,"vlanId"],"vlanTranslatedId":[13,"vlanTranslatedId"]})     
    #     Mapping(rest_interface_module, node_id, mapping_add_2, method='ADD')

#**********************************PON Config ****************************************
    # for port in range(1,2):
    #     response = getall_and_update_condition(rest_interface_module, "/api/gponconfig/sp5100/bridgegroupconfig/getall?nodeId=11&shelfId=1&slotId=1")
    #     switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port+8, index=4), method='POST')
    #     response = getall_and_update_condition(rest_interface_module, "/api/gponconfig/sp5100/portvlan/getall?nodeId=11&shelfId=1&slotId=1")
    #     uplink_vlan_config(rest_interface_module, node_id, uplink_vlan_conf_DATA[1]._replace(ethIfIndex=port+8, taggedVlanSet=vlan_string+",700"), method='POST') 
    
    # response = getall_and_update_condition(rest_interface_module, "/api/gponconfig/dbaProfile/getall?nodeId=11&shelfId=1&slotId=1")
    # dba_HSI = replace_dictionary(dba_profile[0], "set",{"dbaId":1,"name": "HSI", "dbaType": -1, "fixedBwValue": None, "assureBwValue": 250, "maxBwValue": 1000000})
    # dba_HSI = replace_dictionary(dba_HSI,"get", {"namedba": ["HSI", "name"],
    #                                                         "dbatype": [-1, "dbaType"],
    #                                                         "fixedbwvalue": [None, "fixedBwValue"],
    #                                                         "assurebwvalue": [250, "assureBwValue"],
    #                                                         "maxbwvalue": [1000000, "maxBwValue"]} )     
    # DBA_Profile(rest_interface_module, node_id, dba_HSI, method='ADD')
    # dba_VOIP = replace_dictionary(dba_profile[0], "set",{"dbaId":1,"name": "VOIP", "dbaType": -1, "fixedBwValue": None, "assureBwValue": 250, "maxBwValue": 1000})
    # dba_VOIP = replace_dictionary(dba_VOIP,"get", {"namedba": ["VOIP", "name"],
    #                                                         "dbatype": [-1, "dbaType"],
    #                                                         "fixedbwvalue": [None, "fixedBwValue"],
    #                                                         "assurebwvalue": [250, "assureBwValue"],
    #                                                         "maxbwvalue": [1000, "maxBwValue"]} )     
    # DBA_Profile(rest_interface_module, node_id, dba_VOIP, method='ADD')
    # for port in range(2,3):
    #     for i in  range(len(Onu_Number)) :
    #         response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/tcont/getall?nodeId=11&shelfId=1&slotId=1&portId={port}&onuId=-1")
    #         tcont_hsi = replace_dictionary(tcont_Data_Config[0], "set",{"bwProfileId":1,"bwProfileName": "HSI", "name": "", "onuId": i, "portId": port, "tcontId": 2})
    #         tcont_hsi = replace_dictionary(tcont_hsi,"get", {
    #                                                             # "bwProfileId": [1, "bwProfileId"],
    #                                                             "bwProfileName": ["HSI", "bwProfileName"],
    #                                                             "name": ["", "name"],
    #                                                             "onuId": [i, "onuId"],
    #                                                             "portId": [port, "portId"],
    #                                                             "tcontId": [2, "tcontId"]} )                                                         
    #         Tcont_Management(rest_interface_module, node_id, tcont_voip)
    #         tcont_voip = replace_dictionary(tcont_Data_Config[0], "set",{"bwProfileId":1,"bwProfileName": "VOIP", "name": "", "onuId": i, "portId": port, "tcontId": 4})
            # tcont_voip = replace_dictionary(tcont_voip,"get", {
            #                                                     # "bwProfileId": [1, "bwProfileId"],
            #                                                     "bwProfileName": ["VOIP", "bwProfileName"],
            #                                                     "name": ["", "name"],
            #                                                     "onuId": [i, "onuId"],
            #                                                     "portId": [port, "portId"],
            #                                                     "tcontId": [4, "tcontId"]} )                                                         
            # Tcont_Management(rest_interface_module, node_id, tcont_voip)

            # response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/gem/getall?nodeId=17&shelfId=1&slotId=1&portId={port}&onuId={i}")
            # gem_hsi = replace_dictionary(gem_profile_Data_Config[0], "set",{ "gemId":"1","name": "", "onuId": i, "portId": port, "tcontId": 2})
            # gem_hsi = replace_dictionary(gem_hsi,"get", {
            #                                                 "gemid": [1, "gemId"],
            #                                                 "name": ["", "name"],
            #                                                 "onuId": [i, "onuId"],
            #                                                 "portId": [port, "portId"],
            #                                                 "tcontId": [2, "tcontId"] })                                                         
            # Gem_Management(rest_interface_module, node_id, gem_hsi)
            # gem_voip = replace_dictionary(gem_profile_Data_Config[0], "set",{ "gemId":"2","name": "", "onuId": i, "portId": port, "tcontId": 4})
            # gem_voip = replace_dictionary(gem_voip,"get", {
            #                                                 "gemid": [2, "gemId"],
            #                                                 "name": ["", "name"],
            #                                                 "onuId": [i, "onuId"],
            #                                                 "portId": [port, "portId"],
            #                                                 "tcontId": [4, "tcontId"] } )                                                           
            # Gem_Management(rest_interface_module, node_id, gem_voip)

            # response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/service/getall?nodeId=17&shelfId=1&slotId=1&portId={port}&onuId={i}")
            # service_hsi = replace_dictionary(olt_service_profile_Data_Config[0], "set",{ "servicePortId": "1", "portShowName": "PON ","onuId": i,"gemId": 1,"userVlan": f"{Vlan[i]}"})
            # service_hsi = replace_dictionary(service_hsi,"get", {"servicePortId": [1, "servicePortId"],
            #                                                 "userVlan": [Vlan[i], "userVlan"],
            #                                                 "onuId": [i, "onuId"],
            #                                                 "gemId": [1, "gemId"]} )                                                         
            # OLT_Service(rest_interface_module, node_id, service_hsi)
            # service_voip = replace_dictionary(olt_service_profile_Data_Config[0], "set",{ "servicePortId": "2", "portShowName": "PON ","onuId": i,"gemId": 2,"userVlan": "700"})
            # service_voip = replace_dictionary(service_voip,"get", {"servicePortId": [1, "servicePortId"],
            #                                                 "userVlan": [700, "userVlan"],
            #                                                 "onuId": [i, "onuId"],
            #                                                 "gemId": [2, "gemId"]} ) 
            # OLT_Service(rest_interface_module, node_id, service_voip)

            # response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/sp5100/rmonu/service/getall?nodeId=17&shelfId=1&slotId=1&onuId={i}&portId={port}")
            # remote_1 = replace_dictionary(remote_service_profile_Data_Config[0], "set",{"onuId": i, "rmServiceId": "1","onuPortType": "ETH_UNI","vlanMode": "TRUNK", "vlanList":f"{Vlan[i]}", "gemId": 1,"priority": f"{priority[i]}",})
            # remote_1 = replace_dictionary(remote_1,"get", {"rmServiceId": [1, "rmServiceId"],
            #                                             "onuPortType": ["ETH_UNI", "onuPortType"],
            #                                             "vlanMode": ["TRUNK", "vlanMode"],
            #                                             "vlanList": [Vlan[i], "vlanList"],
            #                                             "priority": [priority[i], "priority"],
            #                                             "onuId": [i, "onuId"],
            #                                             "gemId": [1, "gemId"]})                                                       
        #     ONU_remote_Service(rest_interface_module, node_id, remote_1)
        #     remote_2 = replace_dictionary(remote_service_profile_Data_Config[0], "set",{"onuId": i, "rmServiceId": "1","onuPortType": "ETH_UNI","vlanMode": "TRUNK", "vlanList":f"{Vlan[i]}", "gemId": 1,"priority": f"{priority[i]}",})
        #     remote_2 = replace_dictionary(remote_2,"get", {"rmServiceId": [1, "rmServiceId"],
        #                                                 "onuPortType": ["ETH_UNI", "onuPortType"],
        #                                                 "vlanMode": ["TRUNK", "vlanMode"],
        #                                                 "vlanList": [Vlan[i], "vlanList"],
        #                                                 "priority": [priority[i], "priority"],
        #                                                 "onuId": [i, "onuId"],
        #                                                 "gemId": [1, "gemId"]})                                                       
        #     ONU_remote_Service(rest_interface_module, node_id, remote_2)

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


   