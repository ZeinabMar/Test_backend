import pytest
import logging
import json
from Switch.bridge_funcs import *
from conftest import *
from config import *

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]


logger = logging.getLogger(__name__)

BRIDGE_DATA = (
    Bridge(1, 'IEEE', 100, 30, 1, 6, priority=4096),
    Bridge(1, 'IEEE_VLAN_BRIDGE', 1000, 29, 2, 7, priority=8192),
    Bridge(1, 'MSTP', 100, 30, maxAge=6, maxHops=1, priority=12288),
    Bridge(1, 'MSTPRING', 1000, 29, maxAge=7, maxHops=20, priority=16384),
    # Bridge(1, 'RPVSTP', 100, priority=20480),
    # Bridge(1, 'RSTP', 1000, 29, 2, 7, priority=24576),
    # Bridge(1, 'RSTP_RING', 100, 30, 1, 6, priority=28672),
    # Bridge(1, 'RSTP_VLAN_BRIDGE', 1000, 29, 2, 7, priority=32768),
    # Bridge(1, 'RSTP_VLAN_BRIDGE_RING', 100, 30, 1, 6, priority=36864),
    # Bridge(1, 'PROVIDER_MSTP', 1000, 29, maxAge=7, maxHops=35, priority=40960),
    # Bridge(1, 'PROVIDER_MSTP_EDGE', 100, 30, maxAge=6, maxHops=39, priority=45056),
    # Bridge(1, 'PROVIDER_RSTP', 1000, 29, 2, 7, priority=49152),
    Bridge(1, 'PROVIDER_RSTP_EDGE', 1000, 29, 2, 7, priority=53248),
    # Bridge(1, 'PROVIDER_MSTP', 1500, helloTime=3, result='Fail'),
    # Bridge(1, 'RSTP_RING', 1600, maxHops=21, result='Fail'),
    # Bridge(1, 'RSTP', 1000, 100, 23, 6, priority=53248, result='Fail'),
    # Bridge(1, 'IEEE', 100, 30, 1, 6, priority=4000, result='Fail'),
    # Bridge(2, 'IEEE', result='Fail')
)

def test_set_bridge(rest_interface_module, node_id):
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/bridgeconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
    for bridge in BRIDGE_DATA:
        bridge_config(rest_interface_module, node_id, bridge, method='POST')
        if bridge.result == 'Pass':
            bridge_config(rest_interface_module, node_id, bridge, method='DELETE')


