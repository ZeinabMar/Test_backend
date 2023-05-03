import pytest
import logging
import json
from config import *
from Switch.test_vlan import vlan_config
from Switch.bridge_funcs import bridge_config
from collections import namedtuple
# from pytest-check import check


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("nms")]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


Switch = namedtuple('Switch', ['ethIfIndex', 'index', 'bridgeIfSwitchPort', 'bridgeIfBridgeGroupId', 
                    'bridgeIfStp', 'result', 'shelfId', 'slotId', 'nodeId'])
Switch.__new__.__defaults__ = (None, 9, -1, -1, -1, "Pass", 1, 1, None)
Switch_DATA = (
    Switch(None, 0, 1, 1, -1),
    Switch(None, 1, 1, 1, 1),
    Switch(None, 2, 1, -1, -1),
    Switch(None, 3, -1, -1, -1),
    Switch(None, 4, 1, 1, 1),
    Switch(None, 5, -1 , -1, -1, "Fail"),
    Switch(None, 6, -1 , -1, 1, "Fail"),
    Switch(None, 7, -1, 1, 1, "Fail"),
    Switch(None, 8, -1 , 1, -1, "Fail"),
    Switch(None, 9, 1, 1, 1)
)

def switch_config(rest_interface_module, node_id, SWITCH_data=Switch(), method='POST'):
    data = SWITCH_data._replace(nodeId=node_id)
    logger.info(f"TRY TO {method} SWITCH CONFIG ...")
    if method == 'POST':
        url = "/api/gponconfig/sp5100/bridgegroupconfig/update"
        response = rest_interface_module.post_request(url, data._asdict())
    else:  # method==DELETE
        data = data._replace(bridgeIfBridgeGroupId=-1,bridgeIfStp=-1)
        url = "/api/gponconfig/sp5100/bridgegroupconfig/update"
        response = rest_interface_module.post_request(url, data._asdict())
        #****************************************************************
        data = data._replace(bridgeIfSwitchPort=-1)
        url = "/api/gponconfig/sp5100/bridgegroupconfig/update"
        response = rest_interface_module.post_request(url, data._asdict())
        
    if data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in switch config {data._asdict}'
        if response.status_code != 200:
            logger.error(response.message)
        logger.info(f' GETTING switch-config (after {method} method) ... ')
        read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/bridgegroupconfig/get/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.ethIfIndex}")
        input_data = json.loads(read_data.text)
        if method == 'POST':
            if data.index == 0:
                assert (str(input_data["ethIfIndex"]) == str(data.ethIfIndex) and
                        input_data["bridgeIfBridgeGroupId"] == 1 and
                        input_data["bridgeIfSwitchPort"] == 1) ,f'IN {data.ethIfIndex} and {data.index} Everythig is ok switch config(after {method}'
            if data.index == 1:
                assert (str(input_data["ethIfIndex"]) == str(data.ethIfIndex) and
                        input_data["bridgeIfStp"] == 1) ,f'IN {data.ethIfIndex} and {data.index} Everythig is ok switch config(after {method}'
            if data.index == 2:
                assert (str(input_data["ethIfIndex"]) == str(data.ethIfIndex) and
                        input_data["bridgeIfStp"] == -1 and
                        input_data["bridgeIfBridgeGroupId"] == -1) ,f'IN {data.ethIfIndex} and {data.index} Everythig is ok switch config(after {method}'
            if data.index == 3:
                assert (str(input_data["ethIfIndex"]) == str(data.ethIfIndex) and
                        input_data["bridgeIfSwitchPort"] == -1) ,f'IN {data.ethIfIndex} and {data.index} Everythig is ok switch config(after {method}'
            if data.index == 4:
                assert (str(input_data["ethIfIndex"]) == str(data.ethIfIndex) and
                        input_data["bridgeIfSwitchPort"] == 1 and
                        input_data["bridgeIfBridgeGroupId"] == 1 and
                        input_data["bridgeIfStp"] == 1) ,f'IN {data.ethIfIndex} and {data.index} Everythig is ok switch config(after {method}'

            logger.info(f'{data.ethIfIndex} every thing ok after switch config(after {method} ')
            # check.equal(str(input_data[0]["ethIfIndex"]) ,str(data.ethIfIndex), f'IN {data.ethIfIndex} Everythig is ok switch config(after {method}')

        else:  # method==DELETE
            # check.equal(str(input_data[0]["ethIfIndex"]) ,None ,f'IN {data.ethIfIndex} Everythig is ok switch config(after {method}')
            assert (input_data["bridgeIfSwitchPort"] == -1 and 
                    input_data["bridgeIfBridgeGroupId"] == -1 and
                    input_data["bridgeIfStp"] == -1), f'GET ERROR in switch config (after {method})'
    else:
        assert response.status_code in range(400, 505), f'{method} ERROR in switch config {data._asdict}'


def delete_switch():
    
    read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/bridgegroupconfig/get/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.ethIfIndex}")
    input_D = json.loads(read_data.text)
    input_D = input_D._replace(bridgeIfBridgeGroupId=-1,bridgeIfStp=-1)
    url = "/api/gponconfig/sp5100/bridgegroupconfig/update"
    response = rest_interface_module.post_request(url, input_D._asdict())
    #****************************************************************
    read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/bridgegroupconfig/get/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.ethIfIndex}")
    input_D = json.loads(read_data.text)
    input_D = input_D._replace(bridgeIfSwitchPort=-1)
    url = "/api/gponconfig/sp5100/bridgegroupconfig/update"
    response = rest_interface_module.post_request(url, input_D._asdict())

    assert (input_data["bridgeIfSwitchPort"] == -1 and 
            input_data["bridgeIfBridgeGroupId"] == -1 and
            input_data["bridgeIfStp"] == -1), f'GET ERROR in switch config (after {method})'



def test_switch_config(rest_interface_module, node_id):
    # bridge_config(rest_interface_module, node_id, Bridge_conf(), method='POST')
    # for vlan in VLAN_DATA_conf:
    #     vlan_config(rest_interface_module, node_id, vlan, method='POST')  
    for port in range(9,10):
        counter=0
        for stw_data in Switch_DATA:
            counter=counter+1  
            if counter==10:
                # pass
                switch_config(rest_interface_module, node_id, stw_data._replace(ethIfIndex=port), method='DELETE')
            else:
                switch_config(rest_interface_module, node_id, stw_data._replace(ethIfIndex=port), method='POST')       

    # # for vlan in VLAN_DATA_conf:
    #     vlan_config(rest_interface_module, node_id, vlan, method='DELETE')
    # bridge_config(rest_interface_module, node_id, Bridge_conf(), method='DELETE')
         



