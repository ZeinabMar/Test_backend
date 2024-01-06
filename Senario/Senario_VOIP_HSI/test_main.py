from test_Smoke import test_Smoke
from test_VOIP_HSI import test_VOIP_HSI
from config import *
from conftest import *
import pytest
import logging
import json

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

PORT_TotalNumberOnusInThisPort= {2:1,3:1}
def test_main(rest_interface_module, node_id):
    Vlan_From_Serial_Of_ONUs = test_Smoke(rest_interface_module, node_id, PORT_TotalNumberOnusInThisPort)
    test_VOIP_HSI(rest_interface_module, node_id, Vlan_From_Serial_Of_ONUs)