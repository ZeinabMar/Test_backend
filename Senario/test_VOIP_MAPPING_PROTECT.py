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

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)



def test_Shut_Down_On(rest_interface_module, node_id):
    # response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/bridgeconfig/getall?nodeId=11&shelfId=1&slotId=1")
    # bridge_config(rest_interface_module, node_id, Bridge_conf(), method='POST')
    # # ****************************************************************************************************************************
    # for vlan in VLAN_DATA_conf_CUSTOM:
    #     response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/vlan/getall?nodeId=11&shelfId=1&slotId=1")
    #     vlan_config(rest_interface_module, node_id, vlan, method='POST')      
    # for port in range(1,2):
    #     response = getall_and_update_condition(rest_interface_module, "/api/gponconfig/sp5100/bridgegroupconfig/getall?nodeId=11&shelfId=1&slotId=1")
    #     switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port, index=4), method='POST')
    #     response = getall_and_update_condition(rest_interface_module, "/api/gponconfig/sp5100/portvlan/getall?nodeId=11&shelfId=1&slotId=1")
    #     uplink_vlan_config(rest_interface_module, node_id, uplink_vlan_conf_DATA[1]._replace(ethIfIndex=port), method='POST') 

    #     mapping_add_1 = replace_dictionary(Mapping_Add, "set",{"ifIndex": 1, "vlanId": 10,"vlanTranslatedId": 11})
    #     mapping_add_1 = replace_dictionary(mapping_add_1,"get", {"ifIndex":[1,"ifIndex"],"vlanId":[10,"vlanId"],"vlanTranslatedId":[11,"vlanTranslatedId"]})     
    #     Mapping(rest_interface_module, node_id, mapping_add_1, method='ADD')

    #     mapping_add_2 = replace_dictionary(Mapping_Add, "set",{"ifIndex": 1, "vlanId": 12,"vlanTranslatedId": 13})
    #     mapping_add_2 = replace_dictionary(mapping_add_2,"get", {"ifIndex":[1,"ifIndex"],"vlanId":[12,"vlanId"],"vlanTranslatedId":[13,"vlanTranslatedId"]})     
    #     Mapping(rest_interface_module, node_id, mapping_add_2, method='ADD')

#**********************************PON Config ****************************************
    for port in range(2,3):
        response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/pon/getprimaryinfo/11/1/1/{port}/{port}")
        pon_no_shut = replace_dictionary(pon_init_info_no_shutdown, "set", {"portId":port,"ifIndex":port})
        pon_no_shut = replace_dictionary(pon_no_shut,"get", {"portId":[port,"portId"],"ifIndex":[port,"ifIndex"]})
        Pon_Initial_Information(rest_interface_module, node_id, pon_no_shut, method='UPDATE') 

        active = "ADDED"
        while("OPERATION_STATE"!=active):
            active = read_only_Onu_State(rest_interface_module, node_id ,1,1,port)   
        # response = getall_and_update_condition(rest_interface_module, "/api/gponconfig/sp5100/bridgegroupconfig/getall?nodeId=11&shelfId=1&slotId=1")
        # switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port+8, index=4), method='POST')
        # response = getall_and_update_condition(rest_interface_module, "/api/gponconfig/sp5100/portvlan/getall?nodeId=11&shelfId=1&slotId=1")
        # uplink_vlan_config(rest_interface_module, node_id, uplink_vlan_conf_DATA[1]._replace(ethIfIndex=port+8), method='POST') 

        mapping_add_1 = replace_dictionary(Mapping_Add, "set",{"ifIndex": port+8, "vlanId": 10,"vlanTranslatedId": 11})
        mapping_add_1 = replace_dictionary(mapping_add_1,"get", {"ifIndex":[port+8,"ifIndex"],"vlanId":[10,"vlanId"],"vlanTranslatedId":[11,"vlanTranslatedId"]})     
        Mapping(rest_interface_module, node_id, mapping_add_1, method='ADD')

        mapping_add_2 = replace_dictionary(Mapping_Add, "set",{"ifIndex": port+8, "vlanId": 12,"vlanTranslatedId": 13})
        mapping_add_2 = replace_dictionary(mapping_add_2,"get", {"ifIndex":[port+8,"ifIndex"],"vlanId":[12,"vlanId"],"vlanTranslatedId":[13,"vlanTranslatedId"]})     
        Mapping(rest_interface_module, node_id, mapping_add_2, method='ADD')

#**********************************PON UNconfig ****************************************
    for port in range(2,3):
        mapping_del_1 = replace_dictionary(Mapping_Delete, "set",{"ifIndex": port+8, "vlanId": 10,"vlanTranslatedId": 11})
        Mapping(rest_interface_module, node_id, mapping_del_1, method='DELETE')
        mapping_del_2 = replace_dictionary(Mapping_Delete, "set",{"ifIndex": port+8, "vlanId": 12,"vlanTranslatedId": 13})
        Mapping(rest_interface_module, node_id, mapping_del_2, method='DELETE')
        uplink_vlan_config(rest_interface_module, node_id, uplink_vlan_conf_DATA[1]._replace(ethIfIndex=port), method='DELETE')   
        switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port, index=9), method='DELETE')
    
        pon_shut = replace_dictionary(pon_init_info_shutdown, "set", {"portId":port,"ifIndex":port})
        pon_shut = replace_dictionary(pon_shut,"get", {"portId":[port,"portId"],"ifIndex":[port,"ifIndex"]})   
        Pon_Initial_Information(rest_interface_module, node_id, pon_shut, method='UPDATE')  







#**********************************Switch UNconfig ****************************************

    for port in range(1,2):
        mapping_del_1 = replace_dictionary(Mapping_Delete, "set",{"ifIndex": port, "vlanId": 10,"vlanTranslatedId": 11})
        Mapping(rest_interface_module, node_id, mapping_del_1, method='DELETE')

        mapping_del_2 = replace_dictionary(Mapping_Delete, "set",{"ifIndex": port, "vlanId": 12,"vlanTranslatedId": 13})
        Mapping(rest_interface_module, node_id, mapping_del_2, method='DELETE')

    for port in range(1,2):
        uplink_vlan_config(rest_interface_module, node_id, uplink_vlan_conf_DATA[1]._replace(ethIfIndex=port), method='DELETE')   
        switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port, index=9), method='DELETE')
    for vlan in VLAN_DATA_conf_CUSTOM:
        vlan_config(rest_interface_module, node_id, vlan, method='DELETE')
    #****************************************************************************************************************************
    bridge_config(rest_interface_module, node_id, Bridge_conf(), method='DELETE')      


   