import time
import pytest
import logging
from conftest import *
from config import *
from Switch.test_bridge_definition import test_set_bridge
from Switch.test_vlan import test_vlan_management
from Switch.test_Bridge_group_conf import test_switch_config
from Switch.test_Uplink_Port_L2_conf import test_Port_L2_config
from Switch.test_uplink_port_Vlan_conf import test_uplink_vlan_config
from Switch.test_Static_Route_conf import test_Static_Route_config
from Switch.test_Qos_management import test_Qos_Manage_config
from Switch.test_Qos_class_definition import test_Qos_Class_config
from Switch.test_Port_Qos_policy_conf import test_Port_Qos_Policy_config
from Switch.test_QinQ_registration_table_conf import test_QinQ_registration_table_config
from Switch.test_Port_L_3 import test_Port_L3_config
from Switch.test_Static_Route_conf import test_Static_Route_config
from Switch.test_Mapping import test_Mapping
from Switch.test_IGMP_Configuration import test_IGMP_Configuration
# from Switch.test_Bridge_Stp_conf import test_Bridge_Stp_config
# from Switch.test_Port_Stp_conf import test_Port_Stp_config
# from Switch.test_Bridge_Mstp_instance_conf import test_Bridge_Mstp_config
# from Switch.test_Port_Mstp_conf import test_Port_Mstp_config
# from Switch.test_Bridge_mstp_state_report import test_Bridge_Mstp_report
# from Switch.test_Bridge_stp_state_report import test_Bridge_Stp_report
# from Switch.test_Interface_Mstp_state_report import test_Port_Mstp_report
# from Switch.test_Interface_stp_state_report import test_interface_Stp_report
# from Switch.test_Port_QinQ_conf import test_Port_QinQ_config
# from Switch.test_Qos_policy_New_feature import test_Qos_Policy_config
# from Switch.test_Port_Mirror_conf import test_Port_Mirror_config



pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# def test_total(rest_interface_module,node_id):
#     test_set_bridge(rest_interface_module, node_id)
#     test_vlan_management(rest_interface_module, node_id)
#     test_switch_config(rest_interface_module, node_id)
#     test_Port_L2_config(rest_interface_module, node_id)
#     test_uplink_vlan_config(rest_interface_module, node_id)
    # test_Static_Route_config(rest_interface_module, node_id)
    # test_Mapping(rest_interface_module, node_id)
    # test_IGMP_Configuration(rest_interface_module, node_id)
    # test_Qos_Manage_config(rest_interface_module, node_id)
    # test_Qos_Class_config(rest_interface_module, node_id)
    # test_Qos_Policy_config(rest_interface_module, node_id)
    # test_Port_Qos_Policy_config(rest_interface_module, node_id)
    # test_QinQ_registration_table_config(rest_interface_module, node_id)
    # test_Port_QinQ_config(rest_interface_module, node_id)
    # test_Bridge_Stp_config(rest_interface_module, node_id)
    # test_Port_Stp_config(rest_interface_module, node_id)
    # test_Bridge_Mstp_config(rest_interface_module, node_id)
    # test_Port_Mstp_config(rest_interface_module, node_id)
    # test_Port_L3_config(rest_interface_module, node_id)
    # test_Port_Mirror_config(rest_interface_module, node_id)
    # test_Static_Route_config(rest_interface_module, node_id)
    # test_Bridge_Stp_report(rest_interface_module, node_id)
    # test_Bridge_Mstp_report(rest_interface_module, node_id)
    # test_Port_Mstp_report(rest_interface_module, node_id)
    # test_interface_Stp_report(rest_interface_module, node_id)



