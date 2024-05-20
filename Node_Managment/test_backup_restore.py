import pytest
import logging
import json
from config import *
from conftest import *
from Switch.test_vlan import vlan_config
from Switch.bridge_funcs import bridge_config

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


backup = namedtuple('backup', ['index', 'expected_result_Set', 'expected_result_Get', "result", "shelfId", "slotId", 'nodeId'])                                       
backup.__new__.__defaults__ = (None, {}, {},None, 1, 1, None, None)

Back_up_Data = (
    backup(1, {   "nodeId": 11,
                      "shelfId": 1,
                      "slotId": 1,
                      "fileMgmtFtpMode": "CONFIG",
                      "fileMgmtFtpDirection": "PUT",
                      "fileMgmtFtpHost": "192.168.1.65",
                      "fileMgmtFtpFileName": "",
                      "fileMgmtFtpUserName": "root",
                      "fileMgmtFtpPassword": "1",
                      "fileMgmtFtpPort": "21",
                      "deviceType": 0,
                      "errorCode": 0}, result="Pass"),)


def test_back_up_restore(rest_interface_module, node_id):
    bridge_config(rest_interface_module, node_id, Bridge_conf(1, 'PROVIDER_MSTP_EDGE', 100, 30, maxAge=6, maxHops=1, priority=12288), method='POST')
    for vlan in VLAN_DATA_conf_S_C:
        vlan_config(rest_interface_module, node_id, vlan, method='POST')  
    back_up(rest_interface_module, node_id, backup, method='PUT')    

