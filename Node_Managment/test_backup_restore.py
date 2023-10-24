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
                      "fileMgmtFtpPassword": "AccessAdmin",
                      "fileMgmtFtpPort": "21",
                      "deviceType": 0,
                      "errorCode": 0}, result="Pass"),)




def Qos_Policy_config(rest_interface_module, node_id, Qos_Policy_data=Qos_Policy(), method='POST'):
    logger.info(f'BRIDGE MSTP INSTANCE TEST DATA ------- > {Qos_Policy_data.index}')
    data = Qos_Policy_data._replace(nodeId=node_id)
    expected_set = data.expected_result_Set
    expected_set["nodeId"]= int(node_id)
    expected_get = data.expected_result_Get  
   
    logger.info(f"TRY TO {method} Qos_Policy CONFIG ...")
    if method == 'add':
        url = "/api/gponconfig/sp5100/qospolicyconfig/add"
        response = rest_interface_module.post_request(url, expected_set) 
    elif method == 'update':  
        url = "/api/gponconfig/sp5100/qospolicyconfig/update"
        response = rest_interface_module.post_request(url, expected_set) 
    else:  # method==DELETE
        url = f"/api/gponconfig/sp5100/qospolicyconfig/delete/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.qosIndex}"
        response = rest_interface_module.delete_request(url)

    if data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in Qos_Policy config {expected_set}'
        if response.status_code != 200:
            logger.error(response.message)
        logger.info(f' GETTING Qos_Policy-config (after {method} method) ... ')
        read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/qospolicyconfig/get/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.qosIndex}")
        input_data = json.loads(read_data.text)
        #**********************************************************************
        if method == 'add' or method == 'update': 
            for key in expected_get.keys():
                logger.info(f"set steeep IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
            logger.info('set is completed.')

    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in Qos_Policy config {data._asdict}'
        if len(expected_get.keys()) !=0:
            read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/qospolicyconfig/get/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.qosIndex}")
            input_data = json.loads(read_data.text)
            for key in expected_get.keys():
                logger.info(f"set steeep IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)





def test_back_up_restore(rest_interface_module, node_id):
    bridge_config(rest_interface_module, node_id, Bridge_conf(1, 'PROVIDER_MSTP_EDGE', 100, 30, maxAge=6, maxHops=1, priority=12288), method='POST')
    for vlan in VLAN_DATA_conf_S_C:
        vlan_config(rest_interface_module, node_id, vlan, method='POST')  
    back_up(rest_interface_module, node_id, backup, method='PUT')    

