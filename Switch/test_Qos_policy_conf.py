import pytest
import logging
import json
from config import *
from Switch.test_Qos_class_definition import Qos_Class_config
from Switch.test_Qos_management import Qos_Manage_config
from Switch.test_vlan import vlan_config
from Switch.bridge_funcs import bridge_config


# from pytest-check import check

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

Qos_Policy = namedtuple('Qos_Policy', ['index','qosIndex', 'qosPolicyName', 'qosPolicyClassName',
                        'qosPolicyPolicerBucket', 'qosPolicyPolicerCBS', 'qosPolicyPolicerCIR',
                        'qosPolicyPolicerEBS', 'qosPolicyPolicerExceedAction','result' ,'shelfId', 
                        'slotId', 'nodeId'])
Qos_Policy.__new__.__defaults__ = (None, None, None, None, None, None, None, None, None, "Pass", 1, 1, None)
Qos_Policy_DATA = (
    Qos_Policy(1, "1", "P", "C", "CBS", "1000", "1000", "2000", "DROP"),
    Qos_Policy(2, "2", "D", "B", "CBS", "1000", "1000", "2000","DROP"),
    Qos_Policy(3, "2", "G", "B", "CBS", "1000", "1000", "2000","DROP", "Fail"),
    # Qos_Policy(4, 1, "C", "P", "CBS", 200, 1000,2000 ,"DROP"),
    # Qos_Policy(5, 1, "C", "P", "FULL", 1000, 1000,2000 ,"DROP"),
    Qos_Policy(6, 1),
    Qos_Policy(7, 2))

def Qos_Policy_config(rest_interface_module, node_id, Qos_Policy_data=Qos_Policy(), method='POST'):
    data = Qos_Policy_data._replace(nodeId=node_id)
    logger.info(f"TRY TO {method} Qos_Policy CONFIG ...")
    if method == 'add':
        url = "/api/gponconfig/sp5100/qospolicyconfig/add"
        response = rest_interface_module.post_request(url, data._asdict()) 
    elif method == 'POST':  
        url = "/api/gponconfig/sp5100/qospolicyconfig/update"
        response = rest_interface_module.post_request(url, data._asdict()) 
    else:  # method==DELETE
        url = f"/api/gponconfig/sp5100/qospolicyconfig/delete/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.qosIndex}"
        response = rest_interface_module.delete_request(url)

    if data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in Qos_Policy config {data._asdict}'
        if response.status_code != 200:
            logger.error(response.message)
        logger.info(f' GETTING Qos_Policy-config (after {method} method) ... ')
        read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/qospolicyconfig/get/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.qosIndex}")
        input_data = json.loads(read_data.text)
        logger.info(f'data after read input_data {input_data}')
        #**********************************************************************
        if method == 'add': 
            assert  (str(input_data["qosIndex"])== str(data.qosIndex) and
                     str(input_data["qosPolicyName"])== str(data.qosPolicyName) and
                     str(input_data["qosPolicyClassName"])== str(data.qosPolicyClassName) and
                     str(input_data["qosPolicyPolicerBucket"])== str(data.qosPolicyPolicerBucket) and
                     str(input_data["qosPolicyPolicerCBS"])== str(data.qosPolicyPolicerCBS) and
                     str(input_data["qosPolicyPolicerCIR"])== str(data.qosPolicyPolicerCIR) and
                     str(input_data["qosPolicyPolicerEBS"])== str(data.qosPolicyPolicerEBS) and
                     str(input_data["qosPolicyPolicerExceedAction"])== str(data.qosPolicyPolicerExceedAction)),f'IN Everythig is ok Qos_Policy config(after {method}'
            logger.info(f'every thing ok after Qos_Policy config(after {method} ')
            # check.equal(str(input_data[0]["ethIfIndex"]) ,str(data.ethIfIndex), f'IN {data.ethIfIndex} Everythig is ok switch config(after {method}')
        # elif method == 'POST':
        #     ,f'IN Everythig is ok Qos_Policy config(after {method}'
        #     logger.info(f'every thing ok after Qos_Policy config(after {method}')
        #     # check.equal(str(input_data[0]["ethIfIndex"]) ,str(data.ethIfIndex), f'IN {data.ethIfIndex} Everythig is ok switch config(after {method}')
        else:  # method==DELETE
            # check.equal(str(input_data[0]["ethIfIndex"]) ,None ,f'IN {data.ethIfIndex} Everythig is ok switch config(after {method}')
            assert (input_data["qosIndex"] and
                    input_data["qosPolicyName"] and
                    input_data["qosPolicyClassName"] and
                    input_data["qosPolicyPolicerBucket"] and
                    input_data["qosPolicyPolicerCBS"] and
                    input_data["qosPolicyPolicerCIR"] and
                    input_data["qosPolicyPolicerEBS"] and
                    input_data["qosPolicyPolicerExceedAction"])== None,f'GET ERROR in Qos_Policy config (after {method})'
    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in Qos_Policy config {data._asdict}'




def test_Qos_Policy_config(rest_interface_module, node_id):

    # bridge_config(rest_interface_module, node_id, Bridge_conf(1, 'PROVIDER_MSTP_EDGE', 100, 30, maxAge=6, maxHops=1, priority=12288), method='POST')
    # for vlan in VLAN_DATA_conf_S_C:
    #     vlan_config(rest_interface_module, node_id, vlan, method='POST')  
    # #**************************************************************************************************************
    # Qos_Manage_config(rest_interface_module, node_id, Qos_Manage_conf()._replace(qosState=1),method='POST')
    # #*******************************************************************************************************
    # Qos_Class_config(rest_interface_module, node_id, Qos_Class_conf_DATA[0], method='add')
    # Qos_Class_config(rest_interface_module, node_id, Qos_Class_conf_DATA[1], method='add')
    #*************************************************************************************************
    Qos_Policy_config(rest_interface_module, node_id, Qos_Policy_DATA[0], method='add')
    Qos_Policy_config(rest_interface_module, node_id, Qos_Policy_DATA[1], method='add')
    Qos_Policy_config(rest_interface_module, node_id, Qos_Policy_DATA[2], method='add')
    # Qos_Policy_config(rest_interface_module, node_id, Qos_Policy_DATA[2], method='update')
    # Qos_Policy_config(rest_interface_module, node_id, Qos_Policy_DATA[3], method='update')
    # Qos_Policy_config(rest_interface_module, node_id, Qos_Policy_DATA[4], method='add')
    # Qos_Policy_config(rest_interface_module, node_id, Qos_Policy_DATA[3], method='delete')
    # Qos_Policy_config(rest_interface_module, node_id, Qos_Policy_DATA[4], method='delete')
    # #*************************************************************************************************
    # Qos_Class_config(rest_interface_module, node_id, Qos_Class_conf_DATA[2], method='DELETE')
    # Qos_Class_config(rest_interface_module, node_id, Qos_Class_conf_DATA[3], method='DELETE')
    # #********************************************************************************************************
    # Qos_Manage_config(rest_interface_module, node_id, Qos_Manage_conf(),method='POST')
    # #**************************************************************************************************************
    # for vlan in VLAN_DATA_conf_S_C:
    #         vlan_config(rest_interface_module, node_id, vlan, method='DELETE')
    # bridge_config(rest_interface_module, node_id, Bridge_conf(1, 'PROVIDER_MSTP_EDGE', 100, 30, maxAge=6, maxHops=1, priority=12288), method='DELETE')

