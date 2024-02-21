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

Instance_Mstp_report = namedtuple('Instance_Mstp_report', ['stpIndex', "specMstpInstanceBridgeId", 'specMstpInstanceBridgePriority',
                              'specMstpInstanceRootId', 'specMstpInstanceRootPathCost', 'specMstpInstanceRootPort',
                              'shelfId', 'slotId', 'nodeId'])
Instance_Mstp_report.__new__.__defaults__ = (0, 0, 0, 0, 0, 0, 1, 1, None)

def Instannce_Mstp_report(rest_interface_module, node_id, instance_Mstp_rp=Instance_Mstp_report(), method='GET'):
    data = instance_Mstp_rp._replace(nodeId=node_id)
    logger.info(f"TRY TO {method} Instance_Mstp_report CONFIG ...")
    if method == 'GET':  
        read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/instancemstpstatereport/get/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.stpIndex}")
        input_data = json.loads(read_data.text)
        assert read_data.status_code == 200, f'{method} ERROR in Instance_Mstp_report'
        if read_data.status_code != 200:
            logger.error(read_data.message)
        logger.info(f' GETTING Instance_Mstp_report (after {method} method) ... ')
        #*********************************************************
        if method == 'GET':
            assert (input_data["stpIndex"]== data.stpIndex and
                    input_data["specMstpInstanceBridgeId"] == data.specMstpInstanceBridgeId and 
                    input_data["specMstpInstanceBridgePriority"] == data.specMstpInstanceBridgePriority and 
                    input_data["specMstpInstanceRootId"] == data.specMstpInstanceRootId and
                    input_data["specMstpInstanceRootPathCost"] == data.specMstpInstanceRootPathCost and 
                    input_data["specMstpInstanceRootPort"] == data.specMstpInstanceRootPort),f'it appeares problem in Instance_Mstp_report in {input_data}'
            logger.info(f'every thing ok after Instance_Mstp_report')

def test_Instannce_Mstp_report(rest_interface_module, node_id):
    for bridge in Bridge_Mstp:
        response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgeconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
        bridge_config(rest_interface_module, node_id, bridge, method='POST')
        if bridge.bridgeProtocol == 'PROVIDER_MSTP':
            for vlan in VLAN_DATA_conf_service:
                response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/vlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
                vlan_config(rest_interface_module, node_id, vlan, method='POST') 
            
            response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgemstpinstanceconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
            Bridge_Mstp_config(rest_interface_module, node_id, Bridge_Mstp_conf(1, 5, 1, None, None, "15-23", "Pass", 1, 1, None), "add")
            response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/instancemstpstatereport/getall?nodeId={node_id}&shelfId=1&slotId=1")
            Instannce_Mstp_report(rest_interface_module, node_id, Instance_Mstp_report(5, "8005000000000000", bridge.priority, "8005000000000000",0,"0", 1, 1, None), "GET")
            response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgemstpinstanceconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
            Bridge_Mstp_config(rest_interface_module, node_id, Bridge_Mstp_conf(1, 5, 1, "15-23", "15-23", "", "Pass", 1, 1, None), "DELETE")
            
            for vlan in VLAN_DATA_conf_service:
                response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/vlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
                vlan_config(rest_interface_module, node_id, vlan, method='DELETE')

        elif bridge.bridgeProtocol== 'PROVIDER_MSTP_EDGE':
            for vlan in VLAN_DATA_conf_service:
                response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/vlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
                vlan_config(rest_interface_module, node_id, vlan, method='POST') 
            response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgemstpinstanceconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
            Bridge_Mstp_config(rest_interface_module, node_id, Bridge_Mstp_conf(1, 5, 1, None, None, "15-23", "Pass", 1, 1, None), "add")
            response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/instancemstpstatereport/getall?nodeId={node_id}&shelfId=1&slotId=1")
            Instannce_Mstp_report(rest_interface_module, node_id, Instance_Mstp_report(5, "8005000000000000", bridge.priority, "8005000000000000",0,"0", 1, 1, None), "GET")
            response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgemstpinstanceconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
            Bridge_Mstp_config(rest_interface_module, node_id, Bridge_Mstp_conf(1, 5, 1, "15-23", "15-23", "", "Pass", 1, 1, None), "DELETE")
            for vlan in VLAN_DATA_conf_service:
                response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/vlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
                vlan_config(rest_interface_module, node_id, vlan, method='DELETE')
                
            for vlan in VLAN_DATA_conf_CUSTOM:
                response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/vlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
                vlan_config(rest_interface_module, node_id, vlan, method='POST') 
            response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgemstpinstanceconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
            Bridge_Mstp_config(rest_interface_module, node_id, Bridge_Mstp_conf(1, 4, 1, None, None, "10-14", "Pass", 1, 1, None), "add")
            response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/instancemstpstatereport/getall?nodeId={node_id}&shelfId=1&slotId=1")
            Instannce_Mstp_report(rest_interface_module, node_id, Instance_Mstp_report(4, "8004000000000000", bridge.priority, "8004000000000000",0,"0", 1, 1, None), "GET")
            response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgemstpinstanceconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
            Bridge_Mstp_config(rest_interface_module, node_id, Bridge_Mstp_conf(1, 4, 1, "10-14", "10-14", "", "Pass", 1, 1, None), "DELETE")
            for vlan in VLAN_DATA_conf_CUSTOM:
                response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/vlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
                vlan_config(rest_interface_module, node_id, vlan, method='DELETE')
                
        else:
            for vlan in VLAN_DATA_conf_CUSTOM:
                response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/vlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
                vlan_config(rest_interface_module, node_id, vlan, method='POST')   
            response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgemstpinstanceconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
            Bridge_Mstp_config(rest_interface_module, node_id, Bridge_Mstp_conf(1, 5, 1, None, None, "10-14", "Pass", 1, 1, None), "add")
            response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/instancemstpstatereport/getall?nodeId={node_id}&shelfId=1&slotId=1")
            Instannce_Mstp_report(rest_interface_module, node_id, Instance_Mstp_report(5, "8005000000000000", bridge.priority, "8005000000000000",0,"0", 1, 1, None), "GET")
            response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgemstpinstanceconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
            Bridge_Mstp_config(rest_interface_module, node_id, Bridge_Mstp_conf(1, 5, 1, "10-14", "10-14", "", "Pass", 1, 1, None), "DELETE")
            for vlan in VLAN_DATA_conf_CUSTOM:
                response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/vlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
                vlan_config(rest_interface_module, node_id, vlan, method='DELETE')
        response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgeconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
        bridge_config(rest_interface_module, node_id, bridge, method='DELETE')





