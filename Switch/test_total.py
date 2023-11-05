import time
import pytest
import logging
from conftest import *
from Switch.test_bridge_definition import test_set_bridge


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_total(rest_interface_module,node_id):
    test_set_bridge(rest_interface_module, node_id)