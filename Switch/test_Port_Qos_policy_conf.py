import pytest
import logging
import json
from config import *
from Switch.bridge_funcs import bridge_config
from Switch.test_Qos_management import Qos_Manage_config
from Switch.bridge_funcs import bridge_config
from Switch.test_vlan import vlan_config
from Switch.test_Qos_class_definition import Qos_Class_config
from Switch.test_Qos_policy_conf import Qos_Policy_config
# from pytest-check import check


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

Port_Qos_Policy = namedtuple('Port_Qos_Policy', ['index' ,'ifIndex', 'qosIfPolicyName','shelfId', 'slotId', 'result', 'nodeId'])
Port_Qos_Policy.__new__.__defaults__ = (None, 1, "C", "", 1, 1, "Pass", None)
Port_Qos_Policy_DATA = (
    Port_Qos_Policy(1, None, "P", 1, 1, "Pass", None),
    Port_Qos_Policy(2, None, "D", 1, 1, "Fail", None),
    Port_Qos_Policy(3, None, None, 1, 1, "Pass", None),
    Port_Qos_Policy(4, None, "D", 1, 1, "Pass", None),
    Port_Qos_Policy(5, None, None, 1, 1, "Pass", None)
)

def Port_Qos_Policy_config(rest_interface_module, node_id, Port_Qos_Policy_data=Port_Qos_Policy(), method='POST'):
    data = Port_Qos_Policy_data._replace(nodeId=node_id)
    logger.info(f"TRY TO {method} Port_Qos_Policy CONFIG ...")
    if method == 'POST':  
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
            if (data.index == 3) or (data.index == 5):
                assert len(input_data["qosIfPolicyName"]) == 0,f'IN Everythig is ok Port_Qos_Policy config(after {method} in index 3 or 5'
            else:
                assert (input_data["qosIfPolicyName"] == data.qosIfPolicyName and
                        len(input_data["qosIfPolicyName"])!=0),f'IN Everythig is ok Port_Qos_Policy config(after {method}'

            logger.info(f'every thing ok after Port_Qos_Policy config(after {method} ')
    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in Port_Qos_Policy config {data._asdict}'


def test_Port_Qos_Policy_config(rest_interface_module, node_id):

    for vlan in VLAN_DATA_conf_S_C:
        vlan_config(rest_interface_module, node_id, vlan, method='POST')  
    #**************************************************************************************************************
    Qos_Manage_config(rest_interface_module, node_id, Qos_Manage_conf()._replace(qosState=1),method='POST')
    #*******************************************************************************************************
    Qos_Class_config(rest_interface_module, node_id, Qos_Class_conf_DATA[0], method='add')
    Qos_Class_config(rest_interface_module, node_id, Qos_Class_conf_DATA[1], method='add')
    #*********************************************************************************************
    Qos_Policy_config(rest_interface_module, node_id, Qos_Policy_DATA_conf[0], method='add')
    Qos_Policy_config(rest_interface_module, node_id, Qos_Policy_DATA_conf[1], method='add')
    # **********************************************************************************
    for port in range(1,4):
        for port_policy in Port_Qos_Policy_DATA:
            Port_Qos_Policy_config(rest_interface_module, node_id, port_policy._replace(ifIndex=port), method='POST')
    #**********************************************************************************
    # Qos_Policy_config(rest_interface_module, node_id, Qos_Policy_DATA_conf[2], method='DELETE')
    # Qos_Policy_config(rest_interface_module, node_id, Qos_Policy_DATA_conf[3], method='DELETE')
    # #*********************************************************************************************            
    # Qos_Class_config(rest_interface_module, node_id, Qos_Class_conf_DATA[2], method='DELETE')
    # Qos_Class_config(rest_interface_module, node_id, Qos_Class_conf_DATA[3], method='DELETE')
    # #********************************************************************************************************
    # Qos_Manage_config(rest_interface_module, node_id, Qos_Manage_conf(),method='POST')
    # #***************************************************************************************************************
    # for vlan in VLAN_DATA_conf_S_C:
    #         vlan_config(rest_interface_module, node_id, vlan, method='DELETE')

