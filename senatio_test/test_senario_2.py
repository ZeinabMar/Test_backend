import pytest
import logging
import json
import data.mibs
from lib.restlib import rest_interface_module as rest_interface
from collections import namedtuple
from test_switch.bridge_funcs import *
from test_switch.test_Bridge_group_conf import switch_config
from test_switch.test_Bridge_Stp_conf import Bridge_Stp_config
from test_switch.test_Port_Stp_conf import Port_Stp_config
from test_switch.test_Uplink_Port_L2_conf import Port_L2_config
from config import *


pytestmark = [pytest.mark.env_name("olt"), pytest.mark.rest_dev("nms")]
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_senario_1(rest_interface, node_id):
    
    # bridge_config(rest_interface, node_id, Bridge_conf(1, "IEEE", 1200, 22, 5, 10, None, 4096, 1, "Pass", 1, 1, None), method='POST')
    Bridge_Stp_config(rest_interface, node_id,)
    #InterfaceGponOlt1
    # Port_L2_config(rest_interface, node_id, Port_L2_conf(9, 1, -1, "S1G", 1850, "BOTH", None, "FULL", "InterfaceGponOlt1", "Pass", 1, 1, None), method='POST')
    # switch_config(rest_interface, node_id, Switch_conf(9, 4, 1, 1, 1), method='POST')       
    # Port_Stp_config(rest_interface, node_id, Port_Stp_conf(9, 1, "NO", "NO", 1, -1, -1, "Pass", 1, 1, None), method='POST')
    # Port_Storm_config(rest_interface, node_id/, Port_Storm_conf(9, "58", "12", "89", "Pass", 1, 1, None), method='POST')

