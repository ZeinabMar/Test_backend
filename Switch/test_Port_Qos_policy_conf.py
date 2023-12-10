import pytest
import logging
import json
from conftest import *
from config import *
from Switch.bridge_funcs import bridge_config
from Switch.test_Qos_management import Qos_Manage_config
from Switch.bridge_funcs import bridge_config
from Switch.test_vlan import vlan_config
from Switch.test_Qos_class_definition import Qos_Class_config
from Switch.test_Qos_policy_New_feature import Qos_Policy_config
# from pytest-check import check


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

Port_Qos_Policy = namedtuple('Port_Qos_Policy', ['index' ,'ifIndex', 'qosIfPolicyName','shelfId', 'slotId', 'result', 'nodeId'])
Port_Qos_Policy.__new__.__defaults__ = (None, 1, None, 1, 1, "Pass", None)
Port_Qos_Policy_DATA = (
    Port_Qos_Policy(1, None, "policy1", 1, 1, "Pass", None),
    Port_Qos_Policy(2, None, "policy2", 1, 1, "Pass", None),
)

def Port_Qos_Policy_config(rest_interface_module, node_id, Port_Qos_Policy_data=Port_Qos_Policy(), method='POST'):
    data = Port_Qos_Policy_data._replace(nodeId=node_id)
    logger.info(f"TRY TO {method} Port_Qos_Policy CONFIG ...")
    if method == 'POST' or method == 'DELETE':  
        url = "/api/gponconfig/sp5100/portsqospolicyconfig/update"
        response = rest_interface_module.post_request(url, data._asdict()) 

    if data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in Port_Qos_Policy config {data._asdict}'
        if response.status_code != 200:
            logger.error(response.message)
        logger.info(f' GETTING Port_Qos_Policy-config (after {method} method) ... ')
        read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/portsqospolicyconfig/get/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.ifIndex}")
        input_data = json.loads(read_data.text)
        logger.info(f'data after read input_data {input_data}')
        logger.info(f'data.indexxxxx {data.index}')
        #*********************************************************
        if method == 'POST': 
            assert (input_data["qosIfPolicyName"] == data.qosIfPolicyName and
                        len(input_data["qosIfPolicyName"])!=0),f'IN Everythig is ok Port_Qos_Policy config(after {method}'
        if method == 'DELETE': 
            assert len(input_data["qosIfPolicyName"]) == 0,f'IN Everythig is ok Port_Qos_Policy config(after {method} in index 3 or 5'       
        logger.info(f'every thing ok after Port_Qos_Policy config(after {method} ')
            
    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in Port_Qos_Policy config {data._asdict}'


def test_Port_Qos_Policy_config(rest_interface_module, node_id):
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgeconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
    bridge_config(rest_interface_module, node_id, Bridge_conf_s_c[0], method='POST')
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/vlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
    for vlan in VLAN_DATA_conf_S_C:
        vlan_config(rest_interface_module, node_id, vlan, method='POST')  
    #**************************************************************************************************************
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/qosmanagement/get/{node_id}/1/1")
    Qos_Manage_config(rest_interface_module, node_id, Qos_Manage_conf()._replace(qosState=1),method='POST')
    # *******************************************************************************************************
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/qosclassdef/getall?nodeId={node_id}&shelfId=1&slotId=1")
    Qos_Class_config(rest_interface_module, node_id, Qos_Class_conf_DATA[0], method='add')
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/qosclassdef/getall?nodeId={node_id}&shelfId=1&slotId=1")
    Qos_Class_config(rest_interface_module, node_id, Qos_Class_conf_DATA[1], method='add')
    #*********************************************************************************************
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/qospolicyconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
    Qos_Policy_config(rest_interface_module, node_id, Qos_Policy_DATA_Config[0], method='add')
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/qospolicyconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
    Qos_Policy_config(rest_interface_module, node_id, Qos_Policy_DATA_Config[1], method='add')
    # **********************************************************************************
    for port in range(1,2):
        for port_policy in Port_Qos_Policy_DATA:
            response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/portsqospolicyconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
            Port_Qos_Policy_config(rest_interface_module, node_id, port_policy._replace(ifIndex=port), method='POST')
        Port_Qos_Policy_config(rest_interface_module, node_id, Port_Qos_Policy()._replace(ifIndex=port), method='DELETE')
    #**********************************************************************************
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/qospolicyconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
    Qos_Policy_config(rest_interface_module, node_id, Qos_Policy_Delete_Config[0], method='DELETE')
    Qos_Policy_config(rest_interface_module, node_id, Qos_Policy_Delete_Config[1], method='DELETE')
    #*********************************************************************************************            
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/qosclassdef/getall?nodeId={node_id}&shelfId=1&slotId=1")
    Qos_Class_config(rest_interface_module, node_id, Qos_Class_conf_DATA[2], method='DELETE')
    Qos_Class_config(rest_interface_module, node_id, Qos_Class_conf_DATA[3], method='DELETE')
    # ********************************************************************************************************
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/qosmanagement/get/{node_id}/1/1")
    Qos_Manage_config(rest_interface_module, node_id, Qos_Manage_conf(),method='DELETE')
    #***************************************************************************************************************
    for vlan in VLAN_DATA_conf_S_C:
        vlan_config(rest_interface_module, node_id, vlan, method='DELETE')
    bridge_config(rest_interface_module, node_id, Bridge_conf_s_c[0], method='DELETE')

