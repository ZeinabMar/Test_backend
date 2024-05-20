import pytest
import logging
import json
from config import *
from conftest import *
from Pon.test_Pon_Initial_Information import Pon_Initial_Information
from Pon.test_tcont_profile import Tcont_Management
from Pon.test_dba_profile import DBA_Profile
from Pon.test_gem_profile import Gem_Management
from Pon.test_OLT_Service import OLT_Service
from Pon.test_ONU_remote_Service import ONU_remote_Service

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)


def test_Unconfig_remote(rest_interface_module, node_id):
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/rmonu/service/getall?nodeId={node_id}&shelfId=1&slotId=1&onuId=20&portId=1")
    ONU_remote_Service(rest_interface_module, node_id,remote_service(1, {"nodeId":None, "slotId":1,"shelfId":1, "rmServiceId": 1, "onuId": 20, "portId": 1},result="Pass",method="DELETE"))
    ONU_remote_Service(rest_interface_module, node_id,remote_service(1, {"nodeId":None, "slotId":1,"shelfId":1, "rmServiceId": 2, "onuId": 20, "portId": 1},result="Pass",method="DELETE"))
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/service/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=1&onuId=20")
    OLT_Service(rest_interface_module, node_id, service_profile(1, {"nodeId":None, "slotId":1,"shelfId":1, "servicePortId": 1, "onuId": 20, "portId": 1},result="Pass",method="DELETE"))
    OLT_Service(rest_interface_module, node_id, service_profile(1, {"nodeId":None, "slotId":1,"shelfId":1, "servicePortId": 2, "onuId": 20, "portId": 1},result="Pass",method="DELETE"))
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/gem/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=1&onuId=20")
    Gem_Management(rest_interface_module, node_id, gem_profile(1, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"1","name": "gem1", "onuId": 20, "portId": 1, "tcontId": 1},result="Pass",method="DELETE"))
    Gem_Management(rest_interface_module, node_id, gem_profile(1, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"2","name": "gem2", "onuId": 20, "portId": 1, "tcontId": 2},result="Pass",method="DELETE"))
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/tcont/getall?nodeId={node_id}&shelfId=1&slotId=1&portId=1&onuId=20")
    Tcont_Management(rest_interface_module, node_id, tcont(1, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 20, "portId": 1, "tcontId": 1},result="Pass",method="DELETE"))
    Tcont_Management(rest_interface_module, node_id, tcont(1, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 20, "portId": 1, "tcontId": 2},result="Pass",method="DELETE"))


    