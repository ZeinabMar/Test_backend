import pytest
import logging
import json
from config import *
from conftest import *
from Pon.test_Pon_Initial_Information import Pon_Initial_Information
from Pon.test_onu_auto_learn import read_only_Onu_State,read_only_Onu_SN
from Switch.test_vlan import vlan_config
from copy_log_system import copy_log_to_server
from pytest_sina_framework import ssh_interface_module

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.ssh_dev("server_olt")]
# pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.ssh_dev("shelf_olt")]

List_Of_ONTs_On_PON10 = [
    '192.168.15.141'
]

List_Of_ONTs_On_PON4 = [
    '192.168.15.141'
]

def test_traffic_of_ONTs(ssh_interface_module):
    result = ssh_interface_module.exec(f"sudo python3 Reciver.py", timeout=10)
    logger.info(f"result is : {result}")
    assert result != None
    assert result.find("recieving is ok")