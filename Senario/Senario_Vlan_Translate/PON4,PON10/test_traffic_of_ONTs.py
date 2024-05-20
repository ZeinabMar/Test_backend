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

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.ssh_dev("server_olt_1"), pytest.mark.rest_dev("olt_nms")]
# pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.ssh_dev("shelf_olt")]

List_Of_ONTs_On_PON10 = [
    '192.168.15.141'
]

List_Of_ONTs_On_PON4 = [
    '192.168.15.141'
]

def test_traffic_of_ONTs(ssh_interface_module, rest_interface_module):
    for ONT in List_Of_ONTs_On_PON10:
        result = ssh_interface_module.exec(f"ping -c 10 {ONT}", timeout=10)
        logger.info(f"result in {ONT} is : {result}")
        assert result != None
        for line in result:
            assert line != "Request timed out" or line != "Unreachable"
    for ONT in List_Of_ONTs_On_PON4:
        result = ssh_interface_module.exec(f"ping -c 10 {ONT}", timeout=10)
        logger.info(f"result in {ONT} is : {result}")
        assert result != None
        for line in result:
            assert line != "Request timed out" or line != "Unreachable"        
    # ssh_interface_module