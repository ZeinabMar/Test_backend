import pytest
import logging
import json
from config import *
from conftest import *
from Switch.test_Qos_class_definition import Qos_Class_config
from Switch.test_Qos_management import Qos_Manage_config
from Switch.test_vlan import vlan_config
from Switch.bridge_funcs import bridge_config


# from pytest-check import check

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Qos_Policy = namedtuple('Qos_Policy', ['index','qosIndex', 'qosPolicyName', 'qosPolicyClassName',
#                         'qosPolicyPolicerBucket', 'qosPolicyPolicerCBS', 'qosPolicyPolicerCIR',
#                         'qosPolicyPolicerEBS', 'qosPolicyPolicerExceedAction','result' ,'shelfId', 
#                         'slotId', 'nodeId'])
# Qos_Policy.__new__.__defaults__ = (None, None, None, None , None, None, None, None, None, "Pass", 1, 1, None)
# Qos_Policy_DATA = (
#     Qos_Policy(1, "1", "P", "C", "CBS", "1000", "1000", "2000", "DROP"),
#     Qos_Policy(2, "2", "D", "B", "CBS", "1000", "1000", "2000","DROP"),
#     Qos_Policy(3, "2", "G", "B", "CBS", "1000", "1000", "2000","DROP", "Fail"),
#     # Qos_Policy(4, 1, "C", "P", "CBS", 200, 1000,2000 ,"DROP"),
#     # Qos_Policy(5, 1, "C", "P", "FULL", 1000, 1000,2000 ,"DROP"),
#     Qos_Policy(6, 1),
#     Qos_Policy(7, 2))

Qos_Policy = namedtuple('Qos_Policy', ['index', 'expected_result_Set', 'expected_result_Get', "result", "shelfId", "slotId", 'nodeId', "qosIndex"])                                       
Qos_Policy.__new__.__defaults__ = (None, {}, {},None, 1, 1, None, None)

Qos_Policy_DATA_1 = (
    Qos_Policy(1, {"nodeId":None,
                   "slotId":1,
                   "shelfId":1,
                   "qosIndex":1,
                   "qosPolicyClassName": "C",
                   "qosPolicyName": "policy",
                   "qosPolicyPolicerAct": "DROP",
                   "qosPolicyPolicerCBS": 1000,
                   "qosPolicyPolicerCIR": 100,
                   "qosPolicyPolicerColor": "AWARE",
                   "qosPolicyPolicerCount": "BYTE_BASE",
                   "qosPolicyPolicerEBS":100,
                   "qosPolicyPolicerPIR": 2000,
                   "qosPolicyPolicerRate": "SINGLE_RATE"}, {"qosIndex": [1, "qosIndex"],
                                                            "PolicyName": ["policy", "qosPolicyName"],
                                                            "ClassName": ["C", "qosPolicyClassName"],
                                                            "CBS": [1000, "qosPolicyPolicerCBS"],
                                                            "color": ["AWARE", "qosPolicyPolicerColor"],
                                                            "CIR": [100, "qosPolicyPolicerCIR"],
                                                            "EBS": [100, "qosPolicyPolicerEBS"],
                                                            "Act": ["DROP", "qosPolicyPolicerAct"],
                                                            "Rate": ["SINGLE_RATE", "qosPolicyPolicerRate"],
                                                            "count": ["BYTE_BASE", "qosPolicyPolicerCount"],
                                                            "PIR": [0, "qosPolicyPolicerPIR"],}, result="Pass", qosIndex=1),

Qos_Policy(2, {"nodeId":None,
                   "slotId":1,
                   "shelfId":1,
                    "qosIndex":1,
                   "qosPolicyClassName": "C",
                   "qosPolicyName": "policy",
                   "qosPolicyMode": "ALLOW",}, {"qosIndex": [1, "qosIndex"],
                                                            "PolicyName": ["policy", "qosPolicyName"],
                                                            "ClassName": ["C", "qosPolicyClassName"],
                                                            "CBS": [1000, "qosPolicyPolicerCBS"],
                                                            "color": ["AWARE", "qosPolicyPolicerColor"],
                                                            "CIR": [100, "qosPolicyPolicerCIR"],
                                                            "EBS": [100, "qosPolicyPolicerEBS"],
                                                            "Act": ["DROP", "qosPolicyPolicerAct"],
                                                            "Rate": ["SINGLE_RATE", "qosPolicyPolicerRate"],
                                                            "count": ["BYTE_BASE", "qosPolicyPolicerCount"],
                                                            "mode": ["ALLOW", "qosPolicyMode"],
                                                            "PIR": [0, "qosPolicyPolicerPIR"],}, result="Pass", qosIndex=1),
Qos_Policy(3, {"nodeId":None,
                   "slotId":1,
                   "shelfId":1,
                    "qosIndex":1,
                   "qosPolicyClassName": "C",
                   "qosPolicyName": "policy",
                    "qosPolicySetType": "COS",
                    "qosPolicySetValue": 4,
                    "qosPolicySetVlanPriority": 2,}, {"qosIndex": [1, "qosIndex"],
                                                            "PolicyName": ["policy", "qosPolicyName"],
                                                            "ClassName": ["C", "qosPolicyClassName"],
                                                            "CBS": [1000, "qosPolicyPolicerCBS"],
                                                            "color": ["AWARE", "qosPolicyPolicerColor"],
                                                            "CIR": [100, "qosPolicyPolicerCIR"],
                                                            "EBS": [100, "qosPolicyPolicerEBS"],
                                                            "Act": ["DROP", "qosPolicyPolicerAct"],
                                                            "Rate": ["SINGLE_RATE", "qosPolicyPolicerRate"],
                                                            "count": ["BYTE_BASE", "qosPolicyPolicerCount"],
                                                            "mode": ["ALLOW", "qosPolicyMode"],
                                                            "type": ["COS", "qosPolicySetType"],
                                                            "value": [4, "qosPolicySetValue"],
                                                            "priority": [-1, "qosPolicySetVlanPriority"],}, result="Pass", qosIndex=1),

    Qos_Policy(4, {"nodeId":None,
                   "slotId":1,
                   "shelfId":1,
                    "qosIndex":1,
                   "qosPolicyClassName": "C",
                   "qosPolicyName": "policy",
                    "qosPolicySetType": "IP_DSCP",
                    "qosPolicySetValue": 65}, {"qosIndex": [1, "qosIndex"],
                                                            "PolicyName": ["policy", "qosPolicyName"],
                                                            "ClassName": ["C", "qosPolicyClassName"],
                                                            "CBS": [1000, "qosPolicyPolicerCBS"],
                                                            "color": ["AWARE", "qosPolicyPolicerColor"],
                                                            "CIR": [100, "qosPolicyPolicerCIR"],
                                                            "EBS": [100, "qosPolicyPolicerEBS"],
                                                            "Act": ["DROP", "qosPolicyPolicerAct"],
                                                            "Rate": ["SINGLE_RATE", "qosPolicyPolicerRate"],
                                                            "count": ["BYTE_BASE", "qosPolicyPolicerCount"],
                                                            "mode": ["ALLOW", "qosPolicyMode"],
                                                            "type": ["COS", "qosPolicySetType"],
                                                            "value": [4, "qosPolicySetValue"],}, result="Fail", qosIndex=1),   
        Qos_Policy(5, {"nodeId":None,
                   "slotId":1,
                   "shelfId":1,
                    "qosIndex":1,
                   "qosPolicyClassName": "C",
                   "qosPolicyName": "policy",
                    "qosPolicySetType": "IP_DSCP",
                    "qosPolicySetValue": 62,
                    "qosPolicySetVlanPriority": 2,}, {"qosIndex": [1, "qosIndex"],
                                                            "PolicyName": ["policy", "qosPolicyName"],
                                                            "ClassName": ["C", "qosPolicyClassName"],
                                                            "CBS": [1000, "qosPolicyPolicerCBS"],
                                                            "color": ["AWARE", "qosPolicyPolicerColor"],
                                                            "CIR": [100, "qosPolicyPolicerCIR"],
                                                            "EBS": [100, "qosPolicyPolicerEBS"],
                                                            "Act": ["DROP", "qosPolicyPolicerAct"],
                                                            "Rate": ["SINGLE_RATE", "qosPolicyPolicerRate"],
                                                            "count": ["BYTE_BASE", "qosPolicyPolicerCount"],
                                                            "mode": ["ALLOW", "qosPolicyMode"],
                                                            "type": ["IP_DSCP", "qosPolicySetType"],
                                                            "value": [62, "qosPolicySetValue"],
                                                            "priority": [-1, "qosPolicySetValue"],}, result="Pass", qosIndex=1),                                                               
    Qos_Policy(6, {"nodeId":None,
                   "slotId":1,
                   "shelfId":1,
                   "qosIndex":1,
                   "qosPolicyClassName": "C",
                   "qosPolicyName": "policy",
                   "qosPolicySetType": "IP_PRECEDENCE",
                   "qosPolicySetValue": 25}, {"qosIndex": [1, "qosIndex"],
                                                            "PolicyName": ["policy", "qosPolicyName"],
                                                            "ClassName": ["C", "qosPolicyClassName"],
                                                            "CBS": [1000, "qosPolicyPolicerCBS"],
                                                            "color": ["AWARE", "qosPolicyPolicerColor"],
                                                            "CIR": [100, "qosPolicyPolicerCIR"],
                                                            "EBS": [100, "qosPolicyPolicerEBS"],
                                                            "Act": ["DROP", "qosPolicyPolicerAct"],
                                                            "Rate": ["SINGLE_RATE", "qosPolicyPolicerRate"],
                                                            "count": ["BYTE_BASE", "qosPolicyPolicerCount"],
                                                            "mode": ["ALLOW", "qosPolicyMode"],
                                                            "type": ["COS", "qosPolicySetType"],
                                                            "value": [4, "qosPolicySetValue"],}, result="fail", qosIndex=1),    
Qos_Policy(7, {"nodeId":None,
                   "slotId":1,
                   "shelfId":1,
                   "qosIndex":1,
                   "qosPolicyClassName": "C",
                   "qosPolicyName": "policy",
                   "qosPolicySetType": "IP_PRECEDENCE",
                   "qosPolicySetValue": 5,
                   "qosPolicySetVlanPriority": 2,}, {"qosIndex": [1, "qosIndex"],
                                                            "PolicyName": ["policy", "qosPolicyName"],
                                                            "ClassName": ["C", "qosPolicyClassName"],
                                                            "CBS": [1000, "qosPolicyPolicerCBS"],
                                                            "color": ["AWARE", "qosPolicyPolicerColor"],
                                                            "CIR": [100, "qosPolicyPolicerCIR"],
                                                            "EBS": [100, "qosPolicyPolicerEBS"],
                                                            "Act": ["DROP", "qosPolicyPolicerAct"],
                                                            "Rate": ["SINGLE_RATE", "qosPolicyPolicerRate"],
                                                            "count": ["BYTE_BASE", "qosPolicyPolicerCount"],
                                                            "mode": ["ALLOW", "qosPolicyMode"],
                                                            "type": ["IP_PRECEDENCE", "qosPolicySetType"],
                                                            "value": [5, "qosPolicySetValue"],
                                                            "Priority": [-1, "qosPolicySetVlanPriority"],}, result="Pass", qosIndex=1),    


   Qos_Policy(8, {"nodeId":None,
                   "slotId":1,
                   "shelfId":1,
                   "qosIndex":1,
                   "qosPolicyClassName": "C",
                   "qosPolicyName": "policy",
                   "qosPolicySetType": "REDIRECT_TO_PORT",
                   "qosPolicySetValue": 26,
                   "qosPolicySetVlanPriority": 2,}, {"qosIndex": [1, "qosIndex"],
                                                            "PolicyName": ["policy", "qosPolicyName"],
                                                            "ClassName": ["C", "qosPolicyClassName"],
                                                            "CBS": [1000, "qosPolicyPolicerCBS"],
                                                            "color": ["AWARE", "qosPolicyPolicerColor"],
                                                            "CIR": [100, "qosPolicyPolicerCIR"],
                                                            "EBS": [100, "qosPolicyPolicerEBS"],
                                                            "Act": ["DROP", "qosPolicyPolicerAct"],
                                                            "Rate": ["SINGLE_RATE", "qosPolicyPolicerRate"],
                                                            "count": ["BYTE_BASE", "qosPolicyPolicerCount"],
                                                            "mode": ["ALLOW", "qosPolicyMode"],
                                                            "type": ["COS", "qosPolicySetType"],
                                                            "value": [4, "qosPolicySetValue"],
                                                            "Priority": [-1, "qosPolicySetVlanPriority"]}, result="fail", qosIndex=1),  

Qos_Policy(9, {"nodeId":None,
                   "slotId":1,
                   "shelfId":1,
                   "qosIndex":1,
                   "qosPolicyClassName": "C",
                   "qosPolicyName": "policy",
                   "qosPolicyPolicerAct": "COS_TRANSMIT",
                   "qosPolicyPolicerActValue": 4,
                   "qosPolicyPolicerCBS": 1000,
                   "qosPolicyPolicerCIR": 100,
                   "qosPolicyPolicerColor": "AWARE",
                   "qosPolicyPolicerCount": "BYTE_BASE",
                   "qosPolicyPolicerEBS":100,
                   "qosPolicyPolicerPIR": 2000,
                   "qosPolicyPolicerRate": "TWO_RATE",
                   "qosPolicySetType": "REDIRECT_TO_PORT",
                   "qosPolicySetValue": 20,
                   "qosPolicySetVlanPriority": 2,
                   }, {"qosIndex": [1, "qosIndex"],
                                                            "PolicyName": ["policy", "qosPolicyName"],
                                                            "ClassName": ["C", "qosPolicyClassName"],
                                                            "CBS": [1000, "qosPolicyPolicerCBS"],
                                                            "color": ["AWARE", "qosPolicyPolicerColor"],
                                                            "CIR": [100, "qosPolicyPolicerCIR"],
                                                            "EBS": [100, "qosPolicyPolicerEBS"],
                                                            "Act": ["COS_TRANSMIT", "qosPolicyPolicerAct"],
                                                            "actvalue": [4, "qosPolicyPolicerActValue"],
                                                            "Rate": ["SINGLE_RATE", "qosPolicyPolicerRate"],
                                                            "PIR": [2000, "qosPolicyPolicerPIR"],
                                                            "count": ["BYTE_BASE", "qosPolicyPolicerCount"],
                                                            "mode": ["ALLOW", "qosPolicyMode"],
                                                            "type": ["REDIRECT_TO_PORT", "qosPolicySetType"],
                                                            "value": [20, "qosPolicySetValue"],
                                                            "Priority": [-1, "qosPolicySetVlanPriority"]
                                                            }, result="Pass", qosIndex=1),  

   Qos_Policy(10, {"nodeId":None,
                   "slotId":1,
                   "shelfId":1,
                   "qosIndex":1,
                   "qosPolicyClassName": "C",
                   "qosPolicyName": "policy",
                   "qosPolicySetType": "MIRROR_TO_PORT",
                   "qosPolicySetValue": 24,
                   "qosPolicySetVlanPriority": 2,}, {"qosIndex": [1, "qosIndex"],
                                                            "PolicyName": ["policy", "qosPolicyName"],
                                                            "ClassName": ["C", "qosPolicyClassName"],
                                                            "CBS": [1000, "qosPolicyPolicerCBS"],
                                                            "color": ["AWARE", "qosPolicyPolicerColor"],
                                                            "CIR": [100, "qosPolicyPolicerCIR"],
                                                            "EBS": [100, "qosPolicyPolicerEBS"],
                                                            "Act": ["DROP", "qosPolicyPolicerAct"],
                                                            "Rate": ["SINGLE_RATE", "qosPolicyPolicerRate"],
                                                            "count": ["BYTE_BASE", "qosPolicyPolicerCount"],
                                                            "mode": ["ALLOW", "qosPolicyMode"],
                                                            "type": ["MIRROR_TO_PORT", "qosPolicySetType"],
                                                            "value": [24, "qosPolicySetValue"],
                                                            "priority": [-1, "qosPolicySetVlanPriority"]}, result="Pass", qosIndex=1), 
Qos_Policy(11, {"nodeId":None,
                   "slotId":1,
                   "shelfId":1,
                   "qosIndex":1,
                   "qosPolicyClassName": "C",
                   "qosPolicyName": "policy",
                   "qosPolicySetType": "VLAN",
                   "qosPolicySetValue": 24,
                   "qosPolicySetVlanPriority": 2,}, {"qosIndex": [1, "qosIndex"],
                                                            "PolicyName": ["policy", "qosPolicyName"],
                                                            "ClassName": ["C", "qosPolicyClassName"],
                                                            "CBS": [1000, "qosPolicyPolicerCBS"],
                                                            "color": ["AWARE", "qosPolicyPolicerColor"],
                                                            "CIR": [100, "qosPolicyPolicerCIR"],
                                                            "EBS": [100, "qosPolicyPolicerEBS"],
                                                            "Act": ["DROP", "qosPolicyPolicerAct"],
                                                            "Rate": ["SINGLE_RATE", "qosPolicyPolicerRate"],
                                                            "count": ["BYTE_BASE", "qosPolicyPolicerCount"],
                                                            "mode": ["ALLOW", "qosPolicyMode"],
                                                            "type": ["VLAN", "qosPolicySetType"],
                                                            "value": [24, "qosPolicySetValue"],
                                                            "priority": [2, "qosPolicySetVlanPriority"],}, result="Pass", qosIndex=1), 
    
)
Qos_Policy_DATA_2 = (

    Qos_Policy(12, {"nodeId":None,
                   "slotId":1,
                   "shelfId":1,
                    "qosIndex":2,
                   "qosPolicyClassName": "B",
                   "qosPolicyName": "policy",
                   "qosPolicyMode": "ALLOW",}, result="Fail", qosIndex=2),

    Qos_Policy(13, {"nodeId":None,
                   "slotId":1,
                   "shelfId":1,
                   "qosIndex":2,
                   "qosPolicyClassName": "C",
                   "qosPolicyName": "policy1",
                   "qosPolicyMode": "ALLOW",}, result="Fail", qosIndex=2),   

    Qos_Policy(14, {"nodeId":None,
                   "slotId":1,
                   "shelfId":1,
                   "qosIndex":2,
                   "qosPolicyClassName": "B",
                   "qosPolicyName": "policy1",
                   "qosPolicyPolicerAct": "COS_TRANSMIT",
                   "qosPolicyPolicerActValue": 2,
                   "qosPolicyPolicerCBS": 1000,
                   "qosPolicyPolicerCIR": 100,
                   "qosPolicyPolicerColor": "BLIND",
                   "qosPolicyPolicerCount": "PACKET_BASE",
                   "qosPolicyPolicerEBS":100,
                   "qosPolicyPolicerPIR": 2000,
                   "qosPolicyPolicerRate": "TWO_RATE",
                   "qosPolicySetType": "COS",
                   "qosPolicySetValue": 2,
                   "qosPolicyMode": "ALLOW"}, {"qosIndex": [2, "qosIndex"],
                                                            "PolicyName": ["policy1", "qosPolicyName"],
                                                            "ClassName": ["B", "qosPolicyClassName"],
                                                            "CBS": [1000, "qosPolicyPolicerCBS"],
                                                            "color": ["BLIND", "qosPolicyPolicerColor"],
                                                            "CIR": [100, "qosPolicyPolicerCIR"],
                                                            "EBS": [100, "qosPolicyPolicerEBS"],
                                                            "Act": ["COS_TRANSMIT", "qosPolicyPolicerAct"],
                                                            "value": [2, "qosPolicyPolicerActValue"],
                                                            "pir": [2000, "qosPolicyPolicerPIR"],
                                                            "Rate": ["TWO_RATE", "qosPolicyPolicerRate"],
                                                            "count": ["PACKET_BASE", "qosPolicyPolicerCount"],
                                                            "type": ["COS", "qosPolicySetType"],
                                                            "value": [2, "qosPolicySetValue"],
                                                            "mode": ["ALLOW", "qosPolicyMode"]}, result="Pass", qosIndex=2),)
Qos_Policy_Delete = (
    Qos_Policy(12, result="Pass", qosIndex=2),
    Qos_Policy(12, result="Pass", qosIndex=1)
    )


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





def test_Qos_Policy_config(rest_interface_module, node_id):

    bridge_config(rest_interface_module, node_id, Bridge_conf(1, 'PROVIDER_MSTP_EDGE', 100, 30, maxAge=6, maxHops=1, priority=12288), method='POST')
    for vlan in VLAN_DATA_conf_S_C:
        vlan_config(rest_interface_module, node_id, vlan, method='POST')  
    # **************************************************************************************************************
    Qos_Manage_config(rest_interface_module, node_id, Qos_Manage_conf()._replace(qosState=1),method='POST')
    #*******************************************************************************************************
    Qos_Class_config(rest_interface_module, node_id, Qos_Class_conf_DATA[0], method='add')
    Qos_Class_config(rest_interface_module, node_id, Qos_Class_conf_DATA[1], method='add')
    # *************************************************************************************************
    for policy in Qos_Policy_DATA_1:
        if policy.index == 1:
            Qos_Policy_config(rest_interface_module, node_id, policy, method='add')
        else:
            Qos_Policy_config(rest_interface_module, node_id, policy, method='update')

    Qos_Policy_config(rest_interface_module, node_id, Qos_Policy_DATA_2[0], method='add')
    Qos_Policy_config(rest_interface_module, node_id, Qos_Policy_DATA_2[1], method='add')
    Qos_Policy_config(rest_interface_module, node_id, Qos_Policy_DATA_2[2], method='add')

    for policy in Qos_Policy_Delete:
        Qos_Policy_config(rest_interface_module, node_id, policy, method='Delete')

    Qos_Policy_config(rest_interface_module, node_id, Qos_Policy_DATA[1], method='add')
    Qos_Policy_config(rest_interface_module, node_id, Qos_Policy_DATA[2], method='add')
    Qos_Policy_config(rest_interface_module, node_id, Qos_Policy_DATA[2], method='update')
    Qos_Policy_config(rest_interface_module, node_id, Qos_Policy_DATA[3], method='update')
    Qos_Policy_config(rest_interface_module, node_id, Qos_Policy_DATA[4], method='add')
    Qos_Policy_config(rest_interface_module, node_id, Qos_Policy_DATA[3], method='delete')
    Qos_Policy_config(rest_interface_module, node_id, Qos_Policy_DATA[4], method='delete')
    #*************************************************************************************************
    Qos_Class_config(rest_interface_module, node_id, Qos_Class_conf_DATA[2], method='DELETE')
    Qos_Class_config(rest_interface_module, node_id, Qos_Class_conf_DATA[3], method='DELETE')
    #********************************************************************************************************
    Qos_Manage_config(rest_interface_module, node_id, Qos_Manage_conf(),method='POST')
    #**************************************************************************************************************
    for vlan in VLAN_DATA_conf_S_C:
            vlan_config(rest_interface_module, node_id, vlan, method='DELETE')
    bridge_config(rest_interface_module, node_id, Bridge_conf(1, 'PROVIDER_MSTP_EDGE', 100, 30, maxAge=6, maxHops=1, priority=12288), method='DELETE')

