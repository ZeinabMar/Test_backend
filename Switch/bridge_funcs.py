import pytest
import logging
import json
from collections import namedtuple
pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("nms")]



logger = logging.getLogger(__name__)


Bridge = namedtuple('Bridge', ['bridgeId', 'bridgeProtocol', 'ageingTime', 'forwardTime', 'helloTime', 'maxAge',
                               'maxHops', 'priority', 'id', 'result', 'shelfId', 'slotId', 'nodeId'])
Bridge.__new__.__defaults__ = (1, "IEEE_VLAN_BRIDGE", 100, 15, 2, 20, 20, 32768, 1, "Pass", 1, 1, None)



def bridge_config(rest_interface_module, node_id, BRIDGE_data=Bridge(), method='POST'):
    data = BRIDGE_data._replace(nodeId=node_id)
    logger.info(f"TRY TO {method} BRIDGE CONFIG ...")
    if method == 'POST':
        data_add = Bridge()
        data_add = data_add._replace(nodeId=node_id)
        url = "/api/gponconfig/sp5100/bridgeconfig/add"
        response = rest_interface_module.post_request(url, data_add._asdict())
        url = "/api/gponconfig/sp5100/bridgeconfig/update"
        response = rest_interface_module.post_request(url, data._asdict())
    else:  # method==DELETE
        url = f"/api/gponconfig/sp5100/bridgeconfig/delete/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.bridgeId}"
        response = rest_interface_module.delete_request(url)
    if data.result == "Pass":
        assert response.status_code == 200, f'{response.status_code }{method} ERROR in bridge config {data._asdict}'
        if response.status_code != 200:
            logger.error(response.message)
        logger.info(f' GETTING bridge-config (after {method} method) ... ')
        read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/bridgeconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
        if method == 'POST':
            input_data = list(filter(lambda dic: dic["bridgeId"] == data.bridgeId, json.loads(read_data.text)))
            assert (str(input_data[0]["bridgeProtocol"]) == str(data.bridgeProtocol) and
                    input_data[0]["ageingTime"] == data.ageingTime  and
                    input_data[0]["forwardTime"] == data.forwardTime and
                    input_data[0]["maxAge"] == data.maxAge and 
                    input_data[0]["maxHops"] == data.maxHops and
                    input_data[0]["priority"] == data.priority), f'GET ERROR in bridge config(after {method} in {data.priority})'
            if str(data.bridgeProtocol) == "PROVIDER_RSTP_EDGE" or str(data.bridgeProtocol)== "PROVIDER_MSTP_EDGE" :
                assert (input_data[0]["helloTime"] == 2), f'GET ERROR in bridge config(after {method} in {data.priority})'       
        else:  # method==DELETE
            assert not read_data.text, f'GET ERROR in bridge config (after {method})'
    else:
        assert response.status_code in range(400, 505), f'{method} ERROR in bridge config {data._asdict}'


# BRIDGE_DATA = (
#     Bridge(1, 'IEEE', 100, 30, 1, 6, priority=4096),
#     Bridge(1, 'IEEE_VLAN_BRIDGE', 1000, 29, 2, 7, priority=8192),
#     Bridge(1, 'MSTP', 100, 30, maxAge=6, maxHops=1, priority=12288),
#     Bridge(1, 'MSTPRING', 1000, 29, maxAge=7, maxHops=20, priority=16384),
#     Bridge(1, 'RPVSTP', 100, priority=20480),
#     Bridge(1, 'RSTP', 1000, 29, 2, 7, priority=24576),
#     Bridge(1, 'RSTP_RING', 100, 30, 1, 6, priority=28672),
#     Bridge(1, 'RSTP_VLAN_BRIDGE', 1000, 29, 2, 7, priority=32768),
#     Bridge(1, 'RSTP_VLAN_BRIDGE_RING', 100, 30, 1, 6, priority=36864),
#     Bridge(1, 'PROVIDER_MSTP', 1000, 29, maxAge=7, maxHops=35, priority=40960),
#     Bridge(1, 'PROVIDER_MSTP_EDGE', 100, 30, maxAge=6, maxHops=39, priority=45056),
#     Bridge(1, 'PROVIDER_RSTP', 1000, 29, 2, 7, priority=49152),
#     Bridge(1, 'PROVIDER_RSTP_EDGE', 1000, 29, 2, 7, priority=53248)
# )



# def prepare_bridge_data(request):
#     test_name = request.node.name
#     if 'svlan' in test_name:
#         SETUP_DATA = filter(lambda x: x.bridgeProtocol in ['PROVIDER_MSTP', 'PROVIDER_RSTP''PROVIDER_MSTP_EDGE',
#                                                            'PROVIDER_RSTP_EDGE'], BRIDGE_DATA)
#         SETUP_IDS = [f"test number :{i}, bridgeId :{bridge.bridgeId}, bridgeProtocol :{bridge.bridgeProtocol}"
#                      for i, bridge in enumerate(SETUP_DATA)]
#     else:  # 'cvlan' in test_name
#         SETUP_DATA = filter(lambda x: x.bridgeProtocol in ['IEEE_VLAN_BRIDGE', 'MSTP', 'MSTPRING', 'RPVSTP',
#                                                            'RSTP_VLAN_BRIDGE', 'RSTP_VLAN_BRIDGE_RING',
#                                                            'PROVIDER_MSTP_EDGE',  'PROVIDER_RSTP_EDGE'], BRIDGE_DATA)
#         SETUP_IDS = [f"test number :{i}, bridgeId :{bridge.bridgeId}, bridgeProtocol :{bridge.bridgeProtocol}"
#                      for i, bridge in enumerate(SETUP_DATA)]
#     return SETUP_DATA


# @pytest.fixture()
# def bridge_setup(rest_interface_module, node_id, request):
#     data = request.param
#     logger.info(f'SETUP BRIDGE DATA:{data}')
#     bridge_config(rest_interface_module, node_id, data, method='POST')

#     yield  # wait for run test

#     logger.info(f'TEARDOWN BRIDGE DATA:{data}')
#     bridge_config(rest_interface_module, node_id, data, method='DELETE')
