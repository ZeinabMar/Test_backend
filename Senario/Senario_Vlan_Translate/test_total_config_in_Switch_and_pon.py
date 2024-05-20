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

def test_Vlan_Translate(rest_interface_module, node_id):
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgeconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
    bridge_config(rest_interface_module, node_id, Bridge_conf(1,"RSTP_VLAN_BRIDGE"), method='POST')
    # # # # ****************************************************************************************************************************
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/vlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/vlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
    vlan_config(rest_interface_module, node_id, Vlan_conf(702, 'CUSTOMER'), method='POST')  
    vlan_config(rest_interface_module, node_id, Vlan_conf(700, 'CUSTOMER'), method='POST') 
    vlan_config(rest_interface_module, node_id, Vlan_conf(800, 'CUSTOMER'), method='POST') 
    vlan_config(rest_interface_module, node_id, Vlan_conf(802, 'CUSTOMER'), method='POST') 
    response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/dbaProfile/getall?nodeId={node_id}&shelfId=1&slotId=1")
    DBA_Profile(rest_interface_module, node_id, dba_profile(1, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":1,"name": "VOIP", "dbaType": 3, "fixedBwValue": None, "assureBwValue": 250, "maxBwValue": 100000},
                                                           {
                                                            "namedba": ["VOIP", "name"],
                                                            "dbatype": [3, "dbaType"],
                                                            "fixedbwvalue": [0, "fixedBwValue"],
                                                            "assurebwvalue": [250, "assureBwValue"],
                                                            "maxbwvalue": [100000, "maxBwValue"]},result="Pass"), method='ADD')

    response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/dbaProfile/getall?nodeId={node_id}&shelfId=1&slotId=1")
    DBA_Profile(rest_interface_module, node_id, dba_profile(1, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":2,"name": "unicast", "dbaType": 3, "fixedBwValue": None, "assureBwValue": 250, "maxBwValue": 100000},
                                                           {
                                                            "namedba": ["unicast", "name"],
                                                            "dbatype": [3, "dbaType"],
                                                            "fixedbwvalue": [0, "fixedBwValue"],
                                                            "assurebwvalue": [250, "assureBwValue"],
                                                            "maxbwvalue": [100000, "maxBwValue"]},result="Pass"), method='ADD')

    response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/sp5100/bridgegroupconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
    switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=1, index=4), method='POST')
    response = getall_and_update_condition(rest_interface_module, f"/api/gponconfig/sp5100/portvlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
    uplink_vlan_config(rest_interface_module, node_id, uplink_vlan_conf_DATA[1]._replace(ethIfIndex=1,taggedVlanSet="702,802,700"), method='POST') 


    # uplink_vlan_config(rest_interface_module, node_id, uplink_vlan_conf(1, None, "TRUNK", -1, "" , "702,700,802", "", -1, "Pass"), method='POST')
    # switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=1, index=9), method='DELETE')
    # DBA_Profile(rest_interface_module, node_id, dba_profile(1, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":1}, result="Pass"), method='DELETE')       
    # DBA_Profile(rest_interface_module, node_id, dba_profile(1, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":2}, result="Pass"), method='DELETE')       
    # vlan_config(rest_interface_module, node_id, Vlan_conf(800, 'CUSTOMER'), method='DELETE')    
    # vlan_config(rest_interface_module, node_id, Vlan_conf(802, 'CUSTOMER'), method='DELETE')  
    # vlan_config(rest_interface_module, node_id, Vlan_conf(702, 'CUSTOMER'), method='DELETE')    
    # vlan_config(rest_interface_module, node_id, Vlan_conf(700, 'CUSTOMER'), method='DELETE')    
    # # # #****************************************************************************************************************************
    # bridge_config(rest_interface_module, node_id, Bridge_conf(), method='DELETE') 
