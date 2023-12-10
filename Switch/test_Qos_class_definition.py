import pytest
import logging
import json
from conftest import *
from config import *
from Switch.test_Qos_management import Qos_Manage_config
from Switch.bridge_funcs import bridge_config
from test_vlan import vlan_config
# from pytest-check import check

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



Qos_Class = namedtuple('Qos_Class', ['index','qosIndex', 'qosClassName','qosClassVlan', 'qosClassVlanClr',
                        'qosClassVlanSet' ,'shelfId', 'slotId', 'result', 'nodeId'])
Qos_Class.__new__.__defaults__ = (None, 1, "C", None, None, "", 1, 1, "Pass", None)
Qos_Class_DATA = (
    Qos_Class(1, 1, "C", None, None, "10", 1, 1, "Pass", None),
    Qos_Class(2, 2, "B", None, None, "11", 1, 1, "Pass", None),
    Qos_Class(3, 1, "C", "10", "VLAN_RANGE", "", 1, 1, "Pass", None),
    Qos_Class(4, 1, "C", "10", "SINGLE_VLAN", "", 1, 1, "Pass", None),
    Qos_Class(5, 2, "B", "11", None, "12", 1, 1, "Pass", None),
    Qos_Class(6, 2, "B", "11-12", "ALL", "", 1, 1, "Pass", None),
    Qos_Class(7, 2, "B", "", None, "11-12", 1, 1, "Pass", None),
    Qos_Class(8, 2, "B", "11-12", "VLAN_RANGE", "", 1, 1, "Pass", None),
    Qos_Class(9, 1, "C", "", None, "10", 1, 1, "Pass", None),
    # Qos_Class(8, 2, "B", "11", "SINGLE_VLAN", "10", 1, 1, "Fail", None),
    Qos_Class(10, 1, "C"),
    Qos_Class(11, 2, "B")
)

def Qos_Class_config(rest_interface_module, node_id, Qos_Class_data=Qos_Class(), method='POST'):
    data = Qos_Class_data._replace(nodeId=node_id)
    logger.info(f"TRY TO {method} Qos_Class CONFIG ...")
    if method == 'add':
        url = "/api/gponconfig/sp5100/qosclassdef/add"
        response = rest_interface_module.post_request(url, data._asdict()) 
    elif method == 'POST':  
        url = "/api/gponconfig/sp5100/qosclassdef/update"
        response = rest_interface_module.post_request(url, data._asdict()) 
    else:  # method==DELETE
        url = f"/api/gponconfig/sp5100/qosclassdef/delete/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.qosIndex}"
        response = rest_interface_module.delete_request(url)

    if data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in Qos_Class config {data._asdict}'
        if response.status_code != 200:
            logger.error(response.message)
        logger.info(f' GETTING Qos_Class-config (after {method} method) ... ')
        read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/qosclassdef/get/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.qosIndex}")
        input_data = json.loads(read_data.text)
        logger.info(f'data after read input_data {input_data}')
        #*********************************************************
        if method == 'add': 
            assert str(input_data["qosClassVlan"]).find(str(data.qosClassVlanSet)) != -1 ,f'IN Everythig is ok Qos_Class config(after {method}'
            logger.info(f'every thing ok after Qos_Class config(after {method} ')
            # check.equal(str(input_data[0]["ethIfIndex"]) ,str(data.ethIfIndex), f'IN {data.ethIfIndex} Everythig is ok switch config(after {method}')
        elif method == 'POST':
            if data.qosClassVlanClr==None:
                assert str(input_data["qosClassVlan"]).find(str(data.qosClassVlanSet)) != -1 ,f'IN Everythig is ok Qos_Class config(after {method} in step 1'
                logger.info(f'every thing ok after Qos_Class config(after {method} ')
            else:
                if data.index == 3:
                    assert int(input_data["qosClassVlan"]) == int(data.qosClassVlan) ,f'IN Everythig is ok Qos_Class config(after {method} in index 3'
                else:    
                    assert str( input_data["qosClassVlan"]).find(str(data.qosClassVlanClr)) == -1 ,f'IN Everythig is ok Qos_Class config(after {method} in step 2'
                logger.info(f'every thing ok after Qos_Class config(after {method} ')
            # check.equal(str(input_data[0]["ethIfIndex"]) ,str(data.ethIfIndex), f'IN {data.ethIfIndex} Everythig is ok switch config(after {method}')
        else:  # method==DELETE
            # check.equal(str(input_data[0]["ethIfIndex"]) ,None ,f'IN {data.ethIfIndex} Everythig is ok switch config(after {method}')
            assert (input_data["qosClassName"] and input_data["qosClassVlan"] and 
                    input_data["qosClassVlanClr"] and input_data["qosClassVlanSet"])==None,f'GET ERROR in Qos_Class config (after {method})'
    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in Qos_Class config {data._asdict}'


def test_Qos_Class_config(rest_interface_module, node_id):
    response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/bridgeconfig/getall?nodeId=11&shelfId=1&slotId=1")
    bridge_config(rest_interface_module, node_id, Bridge_conf(1, "PROVIDER_MSTP_EDGE"), method='POST')
    response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/vlan/getall?nodeId=11&shelfId=1&slotId=1")
    for vlan in VLAN_DATA_conf_S_C:
        vlan_config(rest_interface_module, node_id, vlan, method='POST')  
    # **************************************************************************************************************
    response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/qosmanagement/get/11/1/1")
    Qos_Manage_config(rest_interface_module, node_id, Qos_Manage_conf()._replace(qosState=1),method='POST')
    #*******************************************************************************************************
    response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/qosclassdef/getall?nodeId=17&shelfId=1&slotId=1")
    Qos_Class_config(rest_interface_module, node_id, Qos_Class_DATA[0], method='add')
    response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/qosclassdef/getall?nodeId=17&shelfId=1&slotId=1")
    Qos_Class_config(rest_interface_module, node_id, Qos_Class_DATA[1], method='add')
    response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/qosclassdef/getall?nodeId=17&shelfId=1&slotId=1")
    Qos_Class_config(rest_interface_module, node_id, Qos_Class_DATA[2], method='POST')
    Qos_Class_config(rest_interface_module, node_id, Qos_Class_DATA[3], method='POST')
    Qos_Class_config(rest_interface_module, node_id, Qos_Class_DATA[4], method='POST')
    Qos_Class_config(rest_interface_module, node_id, Qos_Class_DATA[5], method='POST')
    Qos_Class_config(rest_interface_module, node_id, Qos_Class_DATA[6], method='POST')
    Qos_Class_config(rest_interface_module, node_id, Qos_Class_DATA[7], method='POST')
    Qos_Class_config(rest_interface_module, node_id, Qos_Class_DATA[8], method='POST')
    # Qos_Class_config(rest_interface_module, node_id, Qos_Class_DATA[7], method='POST')
    response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/qosclassdef/getall?nodeId=17&shelfId=1&slotId=1")
    Qos_Class_config(rest_interface_module, node_id, Qos_Class_DATA[9], method='DELETE')
    response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/qosclassdef/getall?nodeId=17&shelfId=1&slotId=1")
    Qos_Class_config(rest_interface_module, node_id, Qos_Class_DATA[10], method='DELETE')
    #*******************************************************************************************************
    Qos_Manage_config(rest_interface_module, node_id, Qos_Manage_conf(),method='DELETE')
    #**************************************************************************************************************
    for vlan in VLAN_DATA_conf_S_C:
            vlan_config(rest_interface_module, node_id, vlan, method='DELETE')
    bridge_config(rest_interface_module, node_id, Bridge_conf(1, "PROVIDER_MSTP_EDGE"), method='DELETE')
