import pytest
import logging
import json
from Switch.bridge_funcs import *
from collections import namedtuple

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

Vlan = namedtuple('Vlan', ['vlanId', 'vlanTypeId', 'vlanState', 'vlanBridgeId', 'result', 'shelfId', 'slotId', 'nodeId'])
Vlan.__new__.__defaults__ = (100, 'CUSTOMER', 1, 1, 'Pass', 1, 1, None)

VLAN_DATA = [
    Vlan(10), Vlan(20), Vlan(150), Vlan(1000), Vlan(2000), Vlan(3400),
    Vlan(10, 'SERVICE_MULTIPOINT_MULTIPOINT'), Vlan(20, 'SERVICE_POINT_POINT'), Vlan(30, 'SERVICE_ROOTED_MUTLIPOINT'),
    Vlan(3500, 'SERVICE_MULTIPOINT_MULTIPOINT'), Vlan(2500, 'SERVICE_POINT_POINT'), Vlan(1100, 'SERVICE_ROOTED_MUTLIPOINT')
]

BridgeData_SVLAN = filter(lambda x: x.bridgeProtocol in ['PROVIDER_MSTP', 'PROVIDER_RSTP', 'PROVIDER_MSTP_EDGE',
                                                         'PROVIDER_RSTP_EDGE'], BRIDGE_DATA)

BridgeData_CVLAN = filter(lambda x: x.bridgeProtocol in ['IEEE_VLAN_BRIDGE', 'MSTP', 'MSTPRING', 'RPVSTP',
                                                   'RSTP_VLAN_BRIDGE', 'RSTP_VLAN_BRIDGE_RING',
                                                   'PROVIDER_MSTP_EDGE', 'PROVIDER_RSTP_EDGE'], BRIDGE_DATA)


# noinspection PyShadowingNames
def vlan_config(rest_interface_module, node_id, vlan_data=Vlan(), method='POST'):
    data = vlan_data._replace(nodeId=node_id)
    logger.info(f"TRY TO {method} VLAN CONFIG ...")
    if method == 'POST':
        url = "/api/gponconfig/sp5100/vlan/add"
        response = rest_interface_module.post_request(url, data._asdict())
    else:  # method==DELETE
        url = f"/api/gponconfig/sp5100/vlan/delete/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.vlanId}/{data.vlanTypeId}"
        response = rest_interface_module.delete_request(url)
    if data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in VLAN config {data._asdict}'
        if response.status_code != 200:
            logger.error(response.message)
        logger.info(f' GETTING vlan-config (after {method} method) ... ')
        read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/vlan/getall?nodeId={node_id}&shelfId=1&slotId=1")
        logger.info(f'GET ALL VLAN-VALUES  :{read_data.text}')
        if method == 'POST':
            input_data = list(filter(lambda dic: dic["vlanId"] == data.vlanId, json.loads(read_data.text)))
            logger.info(f'GETTED VLAN-VALUE (after POST) :{input_data}')
            assert str(input_data[0]["vlanTypeId"]) == str(data.vlanTypeId), f'GET ERROR in VLAN config(after {method})'
        else:  # method==DELETE
            if read_data.text:
                input_data = list(filter(lambda dic: dic["vlanId"] == data.vlanId, json.loads(read_data.text)))
                assert len(input_data) == 0, f'GET ERROR in VLAN config(after {method})'
    else:
        assert response.status_code in range(400, 505), f'{method} ERROR in VLAN config {data._asdict}'


@pytest.mark.parametrize('bridge_setup', BridgeData_CVLAN, indirect=True)
def test_set_cvlan(rest_interface_module, node_id, bridge_setup):
    # set all cvlan
    for vlan in VLAN_DATA:
        if vlan.vlanTypeId == 'CUSTOMER':
            vlan_config(rest_interface_module, node_id, vlan, method='POST')
    # remove all cvlan
    for vlan in VLAN_DATA:
        if vlan.vlanTypeId == 'CUSTOMER':
            vlan_config(rest_interface_module, node_id, vlan, method='DELETE')


# service rooted multipoint has a wrote "mutlipoint" in backend ... modify it
@pytest.mark.parametrize('bridge_setup', BridgeData_SVLAN, indirect=True)
def test_set_svlan(rest_interface_module, node_id, bridge_setup):
    # set all svlans together
    for vlan in VLAN_DATA:
        if 'SERVICE' in vlan.vlanTypeId:
            vlan_config(rest_interface_module, node_id, vlan, method='POST')
    # remove all svlans
    for vlan in VLAN_DATA:
        if 'SERVICE' in vlan.vlanTypeId:
            vlan_config(rest_interface_module, node_id, vlan, method='DELETE')

