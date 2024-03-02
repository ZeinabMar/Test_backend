import pytest
import logging
import json
from conftest import *
from config import *
from Switch.bridge_funcs import bridge_config
from Switch.test_vlan import vlan_config
from Switch.test_Bridge_group_conf import switch_config
from Switch.test_Bridge_Stp_conf import Bridge_Stp_config
from Switch.test_Bridge_Mstp_instance_conf import Bridge_Mstp_config
from Switch.test_Port_Mstp_conf import Port_Mstp_config
# from pytest-check import check


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

Port_Mstp_report = namedtuple('Port_Stp_report', ['ifIndex', 'stpIndex', "specMstpInstanceInterfaceConfiguredCSTExternalPathCost", 'specMstpInstanceInterfaceConfiguredInternalPathCost',
                              'specMstpInstanceInterfaceCSTPriority', 'specMstpInstanceInterfaceDesignatedBridge', 'specMstpInstanceInterfaceDesignatedInternalPathCost',
                              'specMstpInstanceInterfaceDesignatedPortId', 'specMstpInstanceInterfaceDesignatedRoot', 'specMstpInstanceInterfaceForwardDelay',
                              'specMstpInstanceInterfaceForwardTimer', 'specMstpInstanceInterfaceHelloTime', 'specMstpInstanceInterfaceHelloTimer', 'specMstpInstanceInterfaceIfIndex',
                              'specMstpInstanceInterfaceMessageAge', 'specMstpInstanceInterfaceMessageAgeTimer', 'specMstpInstanceInterfacePortId', 'specMstpInstanceInterfacePortNumber',
                              'specMstpInstanceInterfaceRole', 'specMstpInstanceInterfaceState', 'specMstpInstanceInterfaceMSTIPriority','shelfId', 'slotId', 'nodeId'])

def Port_Mstp_report(rest_interface_module, node_id, Port_Mstp_rp=Bridge_conf(), ifIndex=1, stpIndex=5, method='POST'):
    data = Port_Mstp_rp._replace(nodeId=node_id)
    logger.info(f"TRY TO {method} Port_Mstp_report CONFIG ...")

    if method == 'GET':  
        read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/interfacemstpstatereport/get/{data.nodeId}/{data.shelfId}/{data.slotId}/{ifIndex}/{stpIndex}")
        input_data = json.loads(read_data.text)

        assert read_data.status_code == 200, f'{method} ERROR in Port_Mstp config {data._asdict}'
        if read_data.status_code != 200:
            logger.error(read_data.message)
        logger.info(f' GETTING Port_Mstp_report (after {method} method) ... ')

                #*********************************************************
        if method == 'GET':
            if data.bridgeProtocol == "MSTP" or "MSTP_RING" or "PROVIDER_MSTP" or "PROVIDER_MSTP_EDGE":
                assert (input_data["ifIndex"]== ifIndex and
                        input_data["stpIndex"] != 5 and 
                        input_data["specMstpInstanceInterfaceMSTIPriority"] == 128 and 
                        # input_data["specMstpInstanceInterfaceHelloTime"] == data.helloTime and
                        input_data["specMstpInstanceInterfaceMessageAgeTimer"] != 0 ),f'it appeares problem in Port_Mstp_report config(after {method}'
                        # input_data["specMstpMaxAge"] == data.maxAge and
                        # input_data["specMstpMaxHops"] == data.maxHops and
                        # len(str(input_data["specMstpTopologyChangeCount"])) != 0 and
                        # len(str(input_data["specMstpRootId"])) != 0 and
                        # input_data["specMstpStpEnable"] == 1 and
                        # input_data["stpBridgeStpErrDisableState"] == data.stpBridgeStpErrDisableState and
                        #str(input_data["stpBridgeStpPathCost"]) == str(data.stpBridgeStpPathCost)
                        
                logger.info(f'every thing ok after Port_Mstp_report config(after {method} ')

            # else:
            #     assert (input_data["stpIndex"] == 1 and
            #             # len(str(input_data["specStpBridgeId"])) != 0 and 
            #             input_data["specMstpInstanceInterfaceMSTIPriority"] == data.priority and 
            #             input_data["specMstpInstanceInterfaceHelloTime"] == data.helloTime and
            #             input_data["specMstpMaxAge"] == data.maxAge and
            #             input_data["specMstpMaxHops"] == data.maxHops and
            #             len(str(input_data["specMstpTopologyChangeCount"])) != 0 and
            #             len(str(input_data["specMstpRootId"])) != 0 and
            #             input_data["specMstpStpEnable"] == 1 and
            #             input_data["stpBridgeStpErrDisableState"] == data.stpBridgeStpErrDisableState and
            #             str(input_data["stpBridgeStpPathCost"]) == str(data.stpBridgeStpPathCost)),f'IN Everythig is ok Bridge_Mstp config(after {method}'
            #     logger.info(f'every thing ok after Bridge_Mstp config(after {method} ')


def test_Port_Mstp_report(rest_interface_module, node_id):
    def mstp(bridge=Bridge_conf,vlan=Vlan_conf):
        response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgemstpinstanceconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
        Bridge_Mstp_config(rest_interface_module, node_id, Bridge_Mstp_conf(1, 5, 1, None, None, f"{vlan.vlanId}", "Pass", 1, 1, None), "add")

        for port in range(1,2):
            response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgegroupconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
            switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port,index=4), method='POST')
            response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/portmstpconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
            Port_Mstp_config(rest_interface_module, node_id, Port_Mstp_conf_DATA_ADD, method='add')
            
            Port_Mstp_report(rest_interface_module, node_id, bridge, port, 1, method='GET')
            
            response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/portmstpconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
            Port_Mstp_config(rest_interface_module, node_id, Port_Mstp_conf_DATA_ADD, method='DELETE')

            response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgegroupconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
            switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port,index=9), method='DELETE')    

        response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgemstpinstanceconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
        Bridge_Mstp_config(rest_interface_module, node_id, Bridge_Mstp_conf(1, 5), "DELETE")

    for bridge in Bridge_Mstp:
        response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgeconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
        bridge_config(rest_interface_module, node_id, bridge, method='POST')
        if bridge.bridgeProtocol == 'PROVIDER_MSTP' or bridge.bridgeProtocol== 'PROVIDER_MSTP_EDGE':
            for vlan in VLAN_DATA_conf_service:
                response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/vlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
                vlan_config(rest_interface_module, node_id, vlan, method='POST') 
                mstp(bridge=bridge, vlan=vlan)
                vlan_config(rest_interface_module, node_id, vlan, method='DELETE')
        elif bridge.bridgeProtocol== 'PROVIDER_MSTP_EDGE':
            for vlan in VLAN_DATA_conf_service:
                response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/vlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
                vlan_config(rest_interface_module, node_id, vlan, method='POST')  
                mstp(bridge=bridge, vlan=vlan)
                vlan_config(rest_interface_module, node_id, vlan, method='DELETE')

            for vlan in VLAN_DATA_conf_CUSTOM:
                response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/vlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
                vlan_config(rest_interface_module, node_id, vlan, method='POST')   
                mstp(bridge=bridge, vlan=vlan)
                vlan_config(rest_interface_module, node_id, vlan, method='DELETE')
        else:
            for vlan in VLAN_DATA_conf_CUSTOM:
                response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/vlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
                vlan_config(rest_interface_module, node_id, vlan, method='POST')   
                mstp(bridge=bridge, vlan=vlan)
                vlan_config(rest_interface_module, node_id, vlan, method='DELETE')
        response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgeconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
        bridge_config(rest_interface_module, node_id, bridge, method='DELETE')





