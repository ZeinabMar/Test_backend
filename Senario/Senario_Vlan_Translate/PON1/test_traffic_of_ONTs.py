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

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.ssh_dev(["server_olt_1","server_olt_2"]), pytest.mark.rest_dev("olt_nms")]
# pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.ssh_dev("shelf_olt")]

List_Of_ONTs_On_PON11_SIB_SERVER_1 = [
    "172.20.14.14",
    "172.20.15.15",
    "172.20.18.18",
    "172.20.20.20",
    "172.20.21.21",
]

List_Of_ONTs_On_PON11_SIB_SERVER_2 = [
    "172.20.23.23",
    "172.20.24.24",
    "172.20.25.25",
    "172.20.26.26",
    "172.20.27.27",
    "172.20.28.28",
]

def test_traffic_of_ONTs(ssh_interface_module, rest_interface_module):
    for ONT in List_Of_ONTs_On_PON11_SIB_SERVER_1:
        result = ssh_interface_module[0].exec(f"ping -c 10 {ONT}", timeout=10)
        logger.info(f"result in {ONT} is : {result}")
        assert result != None
        for line in result:
            assert line != "Request timed out" or line != "Unreachable"
    # ssh_interface_module
    for ONT in List_Of_ONTs_On_PON11_SIB_SERVER_2:
        result = ssh_interface_module[1].exec(f"ping -c 10 {ONT}", timeout=10)
        logger.info(f"result in {ONT} is : {result}")
        assert result != None
        for line in result:
            assert line != "Request timed out" or line != "Unreachable"