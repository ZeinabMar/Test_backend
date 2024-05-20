import pytest
import logging
import json
from collections import namedtuple
import re
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


#****************************************************************************************************************************
Bridge_conf = namedtuple('Bridge_conf', ['bridgeId', 'bridgeProtocol', 'ageingTime', 'forwardTime', 'helloTime', 'maxAge',
                               'maxHops', 'priority', 'id', 'result', 'shelfId', 'slotId', 'nodeId'])
Bridge_conf.__new__.__defaults__ = (1, "IEEE_VLAN_BRIDGE", 100, 15, 2, 20, 20, 32768, 1, "Pass", 1, 1, None)

Bridge_conf_service =[
    Bridge_conf(1, "PROVIDER_MSTP", 100, 15, 2, 20, 20, 32768, 1, "Pass", 1, 1, None),
    Bridge_conf(1, "PROVIDER_MSTP_EDGE", 100, 15, 2, 20, 20, 32768, 1, "Pass", 1, 1, None),
    Bridge_conf(1, "PROVIDER_RSTP", 100, 15, 2, 20, 20, 32768, 1, "Pass", 1, 1, None),
    Bridge_conf(1, "PROVIDER_RSTP_EDGE", 100, 15, 2, 20, 20, 32768, 1, "Pass", 1, 1, None)
]

Bridge_conf_custom =[
    Bridge_conf(1, "IEEE_VLAN_BRIDGE", 100, 15, 2, 20, 20, 32768, 1, "Pass", 1, 1, None),
    Bridge_conf(1, "PROVIDER_MSTP_EDGE", 100, 15, 2, 20, 20, 32768, 1, "Pass", 1, 1, None),
    Bridge_conf(1, "PROVIDER_RSTP_EDGE", 100, 15, 2, 20, 20, 32768, 1, "Pass", 1, 1, None),
    Bridge_conf(1, "MSTP", 100, 15, 2, 20, 20, 32768, 1, "Pass", 1, 1, None),
    Bridge_conf(1, "MSTPRING", 100, 15, 2, 20, 20, 32768, 1, "Pass", 1, 1, None),
    Bridge_conf(1, "RPVSTP", 100, 15, 2, 20, 20, 32768, 1, "Pass", 1, 1, None),
    Bridge_conf(1, "RSTP", 100, 15, 2, 20, 20, 32768, 1, "Pass", 1, 1, None),
    Bridge_conf(1, "RSTP_RING", 100, 15, 2, 20, 20, 32768, 1, "Pass", 1, 1, None),
    Bridge_conf(1, "RSTP_VLAN_BRIDGE", 100, 15, 2, 20, 20, 32768, 1, "Pass", 1, 1, None),
    Bridge_conf(1, "RSTP_VLAN_BRIDGE_RING", 100, 15, 2, 20, 20, 32768, 1, "Pass", 1, 1, None)
]

Bridge_conf_s_c =[
    Bridge_conf(1, "PROVIDER_MSTP_EDGE", 100, 15, 2, 20, 20, 32768, 1, "Pass", 1, 1, None),
    Bridge_conf(1, "PROVIDER_RSTP_EDGE", 100, 15, 2, 20, 20, 32768, 1, "Pass", 1, 1, None)
]

Bridge_Mstp = [
    Bridge_conf(1, "PROVIDER_MSTP", 100, 15, 2, 20, 20, 32768, 1, "Pass", 1, 1, None),
    Bridge_conf(1, "PROVIDER_MSTP_EDGE", 100, 15, 2, 20, 20, 32768, 1, "Pass", 1, 1, None),
    Bridge_conf(1, "MSTPRING", 100, 15, 2, 20, 20, 32768, 1, "Pass", 1, 1, None),
    Bridge_conf(1, "MSTP", 100, 15, 2, 20, 20, 32768, 1, "Pass", 1, 1, None),
]

Bridge_Stp = [
    Bridge_conf(1, "PROVIDER_RSTP", 100, 15, 2, 20, 20, 32768, 1, "Pass", 1, 1, None),
    Bridge_conf(1, "PROVIDER_RSTP_EDGE", 100, 15, 2, 20, 20, 32768, 1, "Pass", 1, 1, None),
    Bridge_conf(1, "RPVSTP", 100, 15, 2, 20, 20, 32768, 1, "Pass", 1, 1, None),
    Bridge_conf(1, "RSTP", 100, 15, 2, 20, 20, 32768, 1, "Pass", 1, 1, None),
    Bridge_conf(1, "RSTP_RING", 100, 15, 2, 20, 20, 32768, 1, "Pass", 1, 1, None),
    Bridge_conf(1, "RSTP_VLAN_BRIDGE", 100, 15, 2, 20, 20, 32768, 1, "Pass", 1, 1, None),
]

#****************************************************************************************************************************
Vlan_conf = namedtuple('Vlan_conf', ['vlanId', 'vlanTypeId', 'vlanState', 'vlanBridgeId', 'result', 'shelfId', 'slotId', 'nodeId'])
Vlan_conf.__new__.__defaults__ = (100, 'CUSTOMER', 1, 1, 'Pass', 1, 1, None)

VLAN_DATA_conf_CUSTOM = [#VLAN_DATA_conf
     Vlan_conf(10, 'CUSTOMER'), Vlan_conf(11, 'CUSTOMER'), Vlan_conf(12, 'CUSTOMER')
    ,Vlan_conf(13, 'CUSTOMER'), Vlan_conf(14, 'CUSTOMER')]

VLAN_DATA_conf_service = [
     Vlan_conf(15, 'SERVICE_MULTIPOINT_MULTIPOINT'), Vlan_conf(16, 'SERVICE_POINT_POINT'), Vlan_conf(17, 'SERVICE_POINT_POINT'),
     Vlan_conf(18, 'SERVICE_ROOTED_MUTLIPOINT'), Vlan_conf(19, 'SERVICE_MULTIPOINT_MULTIPOINT'),Vlan_conf(20, 'SERVICE_MULTIPOINT_MULTIPOINT'),
     Vlan_conf(21, 'SERVICE_ROOTED_MUTLIPOINT'), Vlan_conf(22, 'SERVICE_MULTIPOINT_MULTIPOINT'),Vlan_conf(23, 'SERVICE_MULTIPOINT_MULTIPOINT')]

VLAN_DATA_conf_S_C = [
    Vlan_conf(10, 'CUSTOMER'), Vlan_conf(11, 'CUSTOMER'), 
    Vlan_conf(12, 'SERVICE_ROOTED_MUTLIPOINT'),Vlan_conf(13, 'SERVICE_POINT_POINT'),
    Vlan_conf(14, 'SERVICE_POINT_POINT'), Vlan_conf(15, 'SERVICE_POINT_POINT')]    


#****************************************************************************************************************************
Switch_conf = namedtuple('Switch_conf', ['ethIfIndex', 'index', 'bridgeIfSwitchPort', 'bridgeIfBridgeGroupId', 
                    'bridgeIfStp', 'result', 'shelfId', 'slotId', 'nodeId'])
Switch_conf.__new__.__defaults__ = (None, None, 1, 1, 1, "Pass", 1, 1, None)
Switch_conf_Data = (
            Switch_conf(None, 4),
            Switch_conf(None, 9))
#****************************************************************************************************************************
uplink_vlan_conf = namedtuple('uplink_vlan', ['ethIfIndex', 'index', 'vlanMode', 'pvId', 'taggedVlan', 
                    'taggedVlanClr', 'taggedVlanSet', 'untaggedVlan', 'result', 
                    'shelfId', 'slotId', 'nodeId'])
uplink_vlan_conf.__new__.__defaults__ = (None, None, "ACCESS",  -1, "" , "", "", -1, "Pass", 1, 1, None)
uplink_vlan_conf_DATA = (
    uplink_vlan_conf(1, 1, "ACCESS", 10),
    uplink_vlan_conf(2, 2, "TRUNK", -1, "", "", "10-14"),
    uplink_vlan_conf(3, 3, "HYBRID", 10, "", "", "10-14"),
    )
#****************************************************************************************************************************
Qos_Manage_conf = namedtuple('Qos_Manage_conf', ['qosIndex', 'qosState', 'shelfId', 'slotId', 'result', 'nodeId'])
Qos_Manage_conf.__new__.__defaults__ = (1, -1, 1, 1, "Pass", None)
#****************************************************************************************************************************
Qos_Class_conf = namedtuple('Qos_Class_conf', ['qosIndex', 'qosClassName','qosClassVlan', 'qosClassVlanClr',
                        'qosClassVlanSet' ,'shelfId', 'slotId', 'result', 'nodeId'])
Qos_Class_conf.__new__.__defaults__ = (1, "C", None, None, "", 1, 1, "Pass", None)
Qos_Class_conf_DATA = (
    Qos_Class_conf(1, "C", None, None, "10", 1, 1, "Pass", None),
    Qos_Class_conf(2, "B", None, None, "11-12", 1, 1, "Pass", None),
    Qos_Class_conf(1, "C"),
    Qos_Class_conf(2, "B"))
#****************************************************************************************************************************
# Qos_Policy_conf = namedtuple('Qos_Policy_conf', ['index','qosIndex', 'qosPolicyName', 'qosPolicyClassName',
#                         'qosPolicyPolicerBucket', 'qosPolicyPolicerCBS', 'qosPolicyPolicerCIR',
#                         'qosPolicyPolicerEBS', 'qosPolicyPolicerExceedAction','result' ,'shelfId', 
#                         'slotId', 'nodeId'])
# Qos_Policy_conf.__new__.__defaults__ = (None, None, None, None, None, None, None, None, None, "Pass", 1, 1, None)
# Qos_Policy_DATA_conf = (
#     Qos_Policy_conf(1, "1", "P", "C", "CBS", "1000", "1000", "2000", "DROP"),
#     Qos_Policy_conf(2, "2", "D", "B", "FULL", "1000", "1000", "2000","DROP"),
#     Qos_Policy_conf(3, 1),
#     Qos_Policy_conf(4, 2))
Qos_Policy_conf = namedtuple('Qos_Policy_conf', ['index', 'expected_result_Set', 'expected_result_Get', "result", "shelfId", "slotId", 'nodeId', "qosIndex"])                                       
Qos_Policy_conf.__new__.__defaults__ = (None, {}, {},None, 1, 1, None, None)
Qos_Policy_DATA_Config = (
    Qos_Policy_conf(1, {"nodeId":None,
                   "slotId":1,
                   "shelfId":1,
                   "qosIndex":1,
                   "qosPolicyClassName": "B",
                   "qosPolicyName": "policy1",
                   "qosPolicyPolicerAct": "DROP",
                   "qosPolicyPolicerCBS": 1000,
                   "qosPolicyPolicerCIR": 100,
                   "qosPolicyPolicerColor": "AWARE",
                   "qosPolicyPolicerCount": "BYTE_BASE",
                   "qosPolicyPolicerEBS":100,
                   "qosPolicyPolicerPIR": 2000,
                   "qosPolicyPolicerRate": "SINGLE_RATE"}, {"qosIndex": [1, "qosIndex"],
                                                            "PolicyName": ["policy1", "qosPolicyName"],
                                                            "ClassName": ["B", "qosPolicyClassName"],
                                                            "CBS": [1000, "qosPolicyPolicerCBS"],
                                                            "color": ["AWARE", "qosPolicyPolicerColor"],
                                                            "CIR": [100, "qosPolicyPolicerCIR"],
                                                            "EBS": [100, "qosPolicyPolicerEBS"],
                                                            "Act": ["DROP", "qosPolicyPolicerAct"],
                                                            "Rate": ["SINGLE_RATE", "qosPolicyPolicerRate"],
                                                            "count": ["BYTE_BASE", "qosPolicyPolicerCount"],
                                                            "PIR": [0, "qosPolicyPolicerPIR"],}, result="Pass", qosIndex=1),
    Qos_Policy_conf(2, {"nodeId":None,
                   "slotId":1,
                   "shelfId":1,
                   "qosIndex":2,
                   "qosPolicyClassName": "B",
                   "qosPolicyName": "policy2",
                   "qosPolicyPolicerAct": "DROP",
                   "qosPolicyPolicerCBS": 1000,
                   "qosPolicyPolicerCIR": 100,
                   "qosPolicyPolicerColor": "AWARE",
                   "qosPolicyPolicerCount": "BYTE_BASE",
                   "qosPolicyPolicerEBS":100,
                   "qosPolicyPolicerPIR": 2000,
                   "qosPolicyPolicerRate": "SINGLE_RATE"}, {"qosIndex": [2, "qosIndex"],
                                                            "PolicyName": ["policy2", "qosPolicyName"],
                                                            "ClassName": ["B", "qosPolicyClassName"],
                                                            "CBS": [1000, "qosPolicyPolicerCBS"],
                                                            "color": ["AWARE", "qosPolicyPolicerColor"],
                                                            "CIR": [100, "qosPolicyPolicerCIR"],
                                                            "EBS": [100, "qosPolicyPolicerEBS"],
                                                            "Act": ["DROP", "qosPolicyPolicerAct"],
                                                            "Rate": ["SINGLE_RATE", "qosPolicyPolicerRate"],
                                                            "count": ["BYTE_BASE", "qosPolicyPolicerCount"],
                                                            "PIR": [0, "qosPolicyPolicerPIR"],}, result="Pass", qosIndex=2),                                                        
                                                            )
Qos_Policy_Delete_Config = (
    Qos_Policy_conf(1, result="Pass", qosIndex=2),
    Qos_Policy_conf(2, result="Pass", qosIndex=1)
    )
#*****************************************************************************************************************************
Port_L2_conf = namedtuple('Port_L2_conf', [ "ethIfIndex", 'ethIfTxStatus','phyIfState', 'phyIfSpeed',
                                 'phyIfMtu', 'phyIfFlowControl', 'phyIfLoopback', 'phyIfDuplex', 
                                 'phyIfDesc', 'result', 'shelfId', 'slotId', 'nodeId'])
Port_L2_conf.__new__.__defaults__ = (None, 1, -1, "S10G", 1500, "NO", -1, "FULL", "", "Pass", 1, 1, None)    
#*****************************************************************************************************************************
Port_Stp_conf = namedtuple('Port_Stp_conf', ['stpIndex', 'stpIfStpAutoEdge','stpIfStpBpduFilter', 'stpIfStpBpduGuard',
                      'stpIfStpEdgePort', 'stpIfStpPortFast', 'stpIfStpRootGuard', 'result','shelfId', 'slotId', 'nodeId'])
Port_Stp_conf.__new__.__defaults__ =  (None, -1, "NO", "NO", -1, -1, -1, "Pass", 1, 1, None)
#*****************************************************************************************************************************
Port_Storm_conf = namedtuple('Port_Storm_conf', ['ethIfIndex', 'phyIfStormBroadcast', 'phyIfStormDLF', 
                        'phyIfStormMulticast', 'result', 'shelfId', 'slotId', 'nodeId'])
Port_Storm_conf.__new__.__defaults__ = (None, "-1", "-1", "-1", "Pass", 1, 1, None)
#*****************************************************************************************************************************
Port_Mstp_conf_Update = namedtuple('Port_Mstp_conf_Update', ['index','ifIndex', 'instanceIfIndex','mstpInstanceIfPathCost', 
                       'mstpInstanceIfPriority', 'result','shelfId', 'slotId', 'nodeId'])
Port_Mstp_conf_Update.__new__.__defaults__ = (None, None, -1, "NO", "NO", -1, -1, -1, "Pass", 1, 1, None)
Port_Mstp_conf_DATA_UPDATE = (
    Port_Mstp_conf_Update(1, None, -1, "ENABLE", "NO", 1, -1, -1, "Pass"),
)

Port_Mstp_conf_add = namedtuple('Port_Mstp_conf_add', ['index','ifIndex', 'instanceIfIndex', 'result','shelfId', 'slotId', 'nodeId'])
Port_Mstp_conf_add.__new__.__defaults__ = (None, None, None, "Pass", 1, 1, None)
Port_Mstp_conf_DATA_ADD = Port_Mstp_conf_add(1, 1, 5, "Pass", 1, 1, None)

#*****************************************************************************************************************************
Bridge_Mstp_conf = namedtuple('Bridge_Mstp_conf', ['index', 'instanceIndex', 'mstpInstanceBridgeId','mstpInstanceVlan', 
                       'mstpInstanceVlanClr','mstpInstanceVlanSet', 'result','shelfId', 'slotId', 'nodeId'])
Bridge_Mstp_conf.__new__.__defaults__ = (None, 1, "", "", "", "Pass", 1, 1, None)
Bridge_Mstp_DATA_conf = (
    Bridge_Mstp_conf(1, 5, 1, None, None, "10-12,17-19", "Pass", 1, 1, None),
    Bridge_Mstp_conf(2, 4, 1, None, None, "13-16", "Pass", 1, 1, None),
    )
Bridge_Mstp_DATA_conf_DELETE = (
    Bridge_Mstp_conf(1, 5),
    Bridge_Mstp_conf(2, 4),
)    
#*****************************************************************************************************************************
uplink_vlan_conf = namedtuple('uplink_vlan_conf', ['ethIfIndex', 'index', 'vlanMode', 'pvId', 'taggedVlan', 
                    'taggedVlanClr', 'taggedVlanSet', 'untaggedVlan', 'result', 
                    'shelfId', 'slotId', 'nodeId'])
uplink_vlan_conf.__new__.__defaults__ = (None, None, "ACCESS",  -1, "" , "", "", -1, "Pass", 1, 1, None)
#*****************************************************************************************************************************
Reg_QinQ_Table_conf = namedtuple('Reg_QinQ_Table_conf', ['index' ,'vlanId', 'vlanRegistrationName', 'vlanRegistrationBridgeId',
                       'vlanRegistrationCVlan', 'vlanRegistrationCVlanClr', 'vlanRegistrationCVlanSet', 'vlanRegistrationSVlan',
                       'vlanRegistrationSVlanSet', 'result', 'shelfId', 'slotId', 'nodeId'])
Reg_QinQ_Table_conf.__new__.__defaults__ = (None, 1, "__NO__", 1, "", "", "", "", "", "Pass", 1, 1, None)
Reg_QinQ_Table_conf_DATA = (
    Reg_QinQ_Table_conf(1, 1, "reg", 1, "", "", "10,11,12,13", "", "15,16,17,18", "Pass", 1, 1, None),#reg for all except access
    Reg_QinQ_Table_conf(1, 1, "reg", 1, "", "", "10", "", "15", "Pass", 1, 1, None))#reg for access

#*****************************************************************************************************************************
mapping = namedtuple('mapping', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
mapping.__new__.__defaults__ = (None, {}, {},None, None)

Mapping_Add = mapping(1, {"nodeId": None,"shelfId": 1,"slotId": 1, "ifIndex": 1, "vlanId": 10,"vlanTranslatedId": 11},{"ifIndex": [1, "ifIndex"],
                                                                                                         "vlanId": [10, "vlanId"],
                                                                                                         "vlanTranslatedId": [11, "vlanTranslatedId"]},result="Pass", method="ADD")

Mapping_Delete = mapping(1, {"nodeId": None,"shelfId": 1,"slotId": 1, "ifIndex": 1, "vlanId": 10,"vlanTranslatedId": 11},result="Pass", method="DELETE")
   
#*****************************************************************************************************************************
d_string ={"nodeId": 17,
            "shelfId": 1,
            "slotId": 1,
            "instanceIndex": 0,
            "mstpInstanceBridgeId": None,
            "mstpInstanceVlan": None,
            "mstpInstanceVlanClr": None,
            "mstpInstanceVlanSet": None,
            "deviceType": None,
            "errorCode": 0}
def set_and_clear_data(input_data=d_string):
    string_t = ""
    if input_data.find("-")!=-1 and input_data.find(",")!=-1:
        result = input_data.split(",")
        result= result.replace(" ", "")
        array_total_2 =[]
        array_total_1 =[]
        for element in result:
            if element != "":
                array_total_2.append(element)
                if element.find("-")!=-1:
                    result1 = list(map(int, re.findall('\d+', element)))
                    array = list(range(result1[0],result1[1]+1))
                    for d in array:
                        array_total_1.append(d)
                    array_total_2.remove(element) 
                    # for d in array_total_2:   
                    #     array_total_1.append(d)
                        

    elif input_data.find("-")!=-1 and input_data.find(",")==-1:
        result1 = list(map(int, re.findall('\d+', input_data)))
        array = list(range(result1[0],result1[1]+1))
        array_total_1 =[]
        array = list(range(result1[0],result1[1]+1))
        for d in array:
            array_total_1.append(d)
    elif input_data.find("-")==-1 and input_data.find(",")!=-1:  
        input_data= input_data.replace(" ", "")
        result = input_data.split(",")
        array_total_1 =[]
        for element in result:
            if element != "":
                array_total_1.append(int(float(element)))
    else:
        string_t = input_data
        return string_t

    for i in array_total_1:
        string_t = string_t +f"{i},"
    string_t = string_t[:-1:] 
    return string_t




#*************************************    PON SECTION   ******************************************************    

dba_profile = namedtuple('dba_profile', ['index', 'expected_result_Set', 'expected_result_Get', "result"])                                       
dba_profile.__new__.__defaults__ = (None, {}, {},None)

dba_profile_Data_Config = (
dba_profile(1, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":None,"name": "dba_type1", "dbaType": 1, "fixedBwValue": 32000, "assureBwValue": None, "maxBwValue": None},
                                                          {
                                                            "namedba": ["dba_type1", "name"],
                                                            "dbatype": [1, "dbaType"],
                                                            "fixedbwvalue": [32000, "fixedBwValue"],
                                                            "assurebwvalue": [32250, "assureBwValue"],
                                                            "maxbwvalue": [32500, "maxBwValue"]},result="Pass"),
                                                            
                                                            
dba_profile(2, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":2,"name": "dba_type2", "dbaType": 1, "fixedBwValue": 32000, "assureBwValue": None, "maxBwValue": None,}, 
                                                          {
                                                            "namedba": ["dba_type2", "name"],
                                                            "dbaType": [1, "dbaType"],
                                                            "fixedBwValue": [32000, "fixedBwValue"],
                                                            "assureBwValue": [32250, "assureBwValue"],
                                                            "maxBwValue": [32500, "maxBwValue"]},result="Pass"),
dba_profile(3, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":3,"name": "dba_type3", "dbaType": 3, "fixedBwValue": 250, "assureBwValue": 500, "maxBwValue": 750,}, 
                                                          {
                                                            "namedba": ["dba_type3", "name"],
                                                            "dbaType": [3, "dbaType"],
                                                            "fixedBwValue": [0, "fixedBwValue"],
                                                            "assureBwValue": [500, "assureBwValue"],
                                                            "maxBwValue": [750, "maxBwValue"]},result="Pass"),
 dba_profile(4, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":4,"name": "dba_type4", "dbaType": 4, "fixedBwValue": None, "assureBwValue": None, "maxBwValue": 50000}, 
                                                         {
                                                            "namedba": ["dba_type4", "name"],
                                                            "dbaType": [4, "dbaType"],
                                                            "fixedBwValue": [0, "fixedBwValue"],
                                                            "assureBwValue": [250, "assureBwValue"],
                                                            "maxBwValue": [50000, "maxBwValue"]},result="Pass"),                                                           
                                                             ) 
dba_profile_Data_Config_Delete = (
    dba_profile(1, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":1}, result="Pass"),
    dba_profile(2, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":2}, result="Pass"),
    dba_profile(3, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":3}, result="Pass"),
    dba_profile(4, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":4}, result="Pass"),
    )
#********************************************************************************************************
tcont = namedtuple('tcont', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
tcont.__new__.__defaults__ = (None, {}, {},None, None)

tcont_Data_Config = (
tcont(1, {"nodeId":None, "slotId":1,"shelfId":1,"bwProfileId":1,"bwProfileName": "dba_type1", "name": "tcont_valid8", "onuId": 1, "portId": 2, "tcontId": 8},
                                                           {
                                                            "bwProfileId": [1, "bwProfileId"],
                                                            "bwProfileName": ["dba_type1", "bwProfileName"],
                                                            "name": ["tcont_valid8", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [2, "portId"],
                                                            "tcontId": [8, "tcontId"]},result="Pass",method="ADD"),  
tcont(2, {"nodeId":None, "slotId":1,"shelfId":1,"bwProfileId":2,"bwProfileName": "dba_type2", "name": "tcont_valid6", "onuId": 1, "portId": 2, "tcontId": 6},
                                                           {
                                                            "bwProfileId": [2, "bwProfileId"],
                                                            "bwProfileName": ["dba_type2", "bwProfileName"],
                                                            "name": ["tcont_valid6", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [2, "portId"],
                                                            "tcontId": [6, "tcontId"]},result="Pass",method="ADD"),  
tcont(3, {"nodeId":None, "slotId":1,"shelfId":1,"bwProfileId":3,"bwProfileName": "dba_type3", "name": "tcont_valid4", "onuId": 1, "portId": 2, "tcontId":4},
                                                           {
                                                            "bwProfileId": [3, "bwProfileId"],
                                                            "bwProfileName": ["dba_type3", "bwProfileName"],
                                                            "name": ["tcont_valid4", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [2, "portId"],
                                                            "tcontId": [4, "tcontId"]},result="Pass",method="ADD"), 
 tcont(4, {"nodeId":None, "slotId":1,"shelfId":1,"bwProfileId":4,"bwProfileName": "dba_type4", "name": "tcont_valid2", "onuId": 1, "portId": 2, "tcontId": 2},
                                                           {
                                                            "bwProfileId": [4, "bwProfileId"],
                                                            "bwProfileName": ["dba_type4", "bwProfileName"],
                                                            "name": ["tcont_valid2", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [2, "portId"],
                                                            "tcontId": [2, "tcontId"]},result="Pass",method="ADD"),        
tcont(5, {"nodeId":None, "slotId":1,"shelfId":1,"bwProfileId":1,"bwProfileName": "dba_type1", "name": "tcont_valid8", "onuId": 1, "portId": 3, "tcontId": 8},
                                                           {
                                                            "bwProfileId": [1, "bwProfileId"],
                                                            "bwProfileName": ["dba_type1", "bwProfileName"],
                                                            "name": ["tcont_valid8", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [3, "portId"],
                                                            "tcontId": [8, "tcontId"]},result="Pass",method="ADD"),                                                                                                                                                                                                                                      
)

tcont_Data_Delete_Config = (
    tcont(1, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 1, "portId": 2, "tcontId": 2},result="Pass",method="DELETE"),    
    tcont(2, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 1, "portId": 2, "tcontId": 4},result="Pass",method="DELETE"),                                                                                                                                                                                
    tcont(3, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 1, "portId": 2, "tcontId": 6},result="Pass",method="DELETE"),                                                                                                                                                                                
    tcont(4, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 1, "portId": 2, "tcontId": 8},result="Pass",method="DELETE"),   
    tcont(5, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 1, "portId": 3, "tcontId": 8},result="Pass",method="DELETE"),                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
)

#********************************************************************************************************
gem_data_for_other_TCs=[
    {"gemId": "1", "name": "gem_test1", "onuId": 1, "portId": 1,"tcontId": 1, "tcontName": "tcont-test","result": "Pass"},
    {"gemId": "2", "name": "gem2", "onuId": 1, "portId": 1, "tcontId": 1, "tcontName": "tcont-test", "result": "Pass"}]
gem_profile = namedtuple('gem_profile', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
gem_profile.__new__.__defaults__ = (None, {}, {},None, None)

gem_profile_Data_Config = (
gem_profile(1, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"1","name": "gem_test1", "onuId": 1, "portId": 2, "tcontId": 8},
                                                           {
                                                            "gemid": [1, "gemId"],
                                                            "name": ["gem_test1", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [2, "portId"],
                                                            "tcontId": [8, "tcontId"]},result="Pass",method="ADD"), 
gem_profile(2, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"2","name": "gem_test2", "onuId": 1, "portId": 2, "tcontId": 6},
                                                           {
                                                            "gemid": [2, "gemId"],
                                                            "name": ["gem_test2", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [2, "portId"],
                                                            "tcontId": [6, "tcontId"]},result="Pass",method="ADD"),
gem_profile(3, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"1","name": "gem_test1", "onuId": 1, "portId": 3, "tcontId": 8},
                                                           {
                                                            "gemid": [1, "gemId"],
                                                            "name": ["gem_test1", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [3, "portId"],
                                                            "tcontId": [8, "tcontId"]},result="Pass",method="ADD"),
                                                            )
gem_profile_Data_Delete_Config= (
    gem_profile(1, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"1","name": "gem_test1", "onuId": 1, "portId": 2, "tcontId": 8},result="Pass",method="DELETE"), 
    gem_profile(2, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"2","name": "gem_test2", "onuId": 1, "portId": 2, "tcontId": 6},result="Pass",method="DELETE"), 
    gem_profile(3, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"1","name": "gem_test1", "onuId": 1, "portId": 3, "tcontId": 8},result="Pass",method="DELETE"), 
)

#******************************************************************************************************************************************
service_profile = namedtuple('service_profile', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
service_profile.__new__.__defaults__ = (None, {}, {},None, None)

service_profile_Data_Config = (
service_profile(1, {"nodeId":None, "slotId":1,"shelfId":1, "servicePortId": "1", "onuId": 1, "portId": 2, "gemId": 1, "userVlan": "10"},
                                                           {
                                                            "gemId": [1, "gemId"],
                                                            "servicePortId": [1, "servicePortId"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [2, "portId"],
                                                            "userVlan": [10, "userVlan"],},result="Pass",method="ADD"),  
service_profile(2, {"nodeId":None, "slotId":1,"shelfId":1, "servicePortId": "2", "onuId": 1, "portId": 2, "gemId": 1, "userVlan": "11"},
                                                           {
                                                            "gemId": [1, "gemId"],
                                                            "servicePortId": [2, "servicePortId"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [2, "portId"],
                                                            "userVlan": [11, "userVlan"],},result="Pass",method="ADD"),                                                             
service_profile(3, {"nodeId":None, "slotId":1,"shelfId":1, "servicePortId": "1", "onuId": 1, "portId": 3, "gemId": 1, "userVlan": "10"},
                                                           {
                                                            "gemId": [1, "gemId"],
                                                            "servicePortId": [1, "servicePortId"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [3, "portId"],
                                                            "userVlan": [10, "userVlan"],},result="Pass",method="ADD"),   
)

service_profile_Data_Delete_Config = (
    service_profile(1, {"nodeId":None, "slotId":1,"shelfId":1, "servicePortId": 1, "onuId": 1, "portId": 2},result="Pass",method="DELETE"),  
    service_profile(2, {"nodeId":None, "slotId":1,"shelfId":1, "servicePortId": 2, "onuId": 1, "portId": 2},result="Pass",method="DELETE"),  
    service_profile(3, {"nodeId":None, "slotId":1,"shelfId":1, "servicePortId": 1, "onuId": 1, "portId": 3},result="Pass",method="DELETE"),  
)
#****************************************************************************************************************************
remote_service = namedtuple('remote_service_profile', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
remote_service.__new__.__defaults__ = (None, {}, {},None, None)
remote_service_profile_Data = (
remote_service(1, {
    "nodeId": None,"shelfId": 1,"slotId": 1,"portId": 2,"onuId": 1, "rmServiceId": "1",
    "onuPortType": "VEIP","onuPortId": 0,"vlanMode": "ACCESS","gemId": 1,"pvId": "10","priority": "3",}, {"rmServiceId": [1, "rmServiceId"],
                                                                                                "onuPortType": ["VEIP", "onuPortType"],
                                                                                                "onuPortId": [0, "onuPortId"],
                                                                                                "onuId": [1, "onuId"],
                                                                                                "portId": [2, "portId"],
                                                                                                "gemId": [1, "gemId"],
                                                                                                "vlanMode": ["ACCESS", "vlanMode"],
                                                                                                "pvId": [10, "pvId"],
                                                                                                "priority": [3, "priority"],},result="Pass",method="ADD"),
)
#****************************************************************************************************************************
Onu_Service_Profile = namedtuple('Onu_Service_Profile', ['index', 'expected_result_Set', 'expected_result_Get', "result"])                                       
Onu_Service_Profile.__new__.__defaults__ = (None, {}, {},None)

Onu_Service_Profile_Data_Config = (
    Onu_Service_Profile(1, {
    "nodeId": None,"shelfId": 1,"slotId": 1,"onuServiceProfileId": "1","onuServiceProfileName": None,"onuTypeProfileName": "Default"},
    {"onuserviceId": [1, "onuServiceProfileId"],"onuServiceProfileName": [None, "onuServiceProfileName"],"onuTypeProfileName": ["Default", "onuTypeProfileName"]},result="Pass"),  
Onu_Service_Profile(2, {
    "nodeId": None,"shelfId": 1,"slotId": 1,"onuServiceProfileId": "2","onuServiceProfileName": None,"onuTypeProfileName": "Default"},
    {"onuserviceId": [2, "onuServiceProfileId"], "onuServiceProfileName": [None, "onuServiceProfileName"], "onuTypeProfileName": ["Default", "onuTypeProfileName"]},result="Pass"),              
)
Onu_Service_Profile_Delete_Config = (
    Onu_Service_Profile(1, {"nodeId":None, "slotId":1,"shelfId":1,"onuServiceProfileId":"1"}, result="Pass"),
    Onu_Service_Profile(2, {"nodeId":None, "slotId":1,"shelfId":1,"onuServiceProfileId":"2"}, result="Pass"),
)
#****************************************************************************************************************************
Tcont_service_profile = namedtuple('Tcont_service_profile', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
Tcont_service_profile.__new__.__defaults__ = (None, {}, {},None, None)

Tcont_service_profile_Data_Config = (
Tcont_service_profile(1, {
    "id": None,"tcontId": "1","nodeId": None,"shelfId": 1,"slotId": 1,"onuId": 1,"name": "test_tcont1",
    "bwProfileName": "dba_type1","bwProfileId": 1,"bwProfileShow": "dba_type1(1)",}, {"name": ["test_tcont1", "name"],
                                                                                                "bwProfileName": ["dba_type1", "bwProfileName"],
                                                                                                "bwProfileId": [1, "bwProfileId"],
                                                                                                "onuId": [1, "onuId"]},result="Pass",method="ADD"),
Tcont_service_profile(2, {
    "id": None,"tcontId": "1","nodeId": None,"shelfId": 1,"slotId": 1,"onuId": 2,"name": "test_tcont1",
    "bwProfileName": "dba_type1","bwProfileId": 1,"bwProfileShow": "dba_type1(1)",}, {"name": ["test_tcont1", "name"],
                                                                                                "bwProfileName": ["dba_type1", "bwProfileName"],
                                                                                                "bwProfileId": [1, "bwProfileId"],
                                                                                                "onuId": [2, "onuId"]},result="Pass",method="ADD"),

)  

Tcont_service_profile_Delete_Config = (
    Tcont_service_profile(1, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 1, "tcontId": 1},result="Pass",method="DELETE"), 
    Tcont_service_profile(1, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 2, "tcontId": 1},result="Pass",method="DELETE"), 
)

#****************************************************************************************************************************

Gem_service_profile = namedtuple('Gem_service_profile', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
Gem_service_profile.__new__.__defaults__ = (None, {}, {},None, None)

Gem_service_profile_Data_Config = (
Gem_service_profile(1, { "gemId": "1", "tcontId": 1,"tcontName": "", "nodeId": None, "shelfId": 1,
                         "slotId": 1,"onuId": 1, "name": "test_gem1",}, {"tcontId": [1, "tcontId"],
                                                                         "name": ["test_gem1", "name"],
                                                                         "onuId": [1, "onuId"],
                                                                         "gemId": [1, "gemId"]},result="Pass",method="ADD"),
Gem_service_profile(2, { "gemId": "1", "tcontId": 1,"tcontName": "", "nodeId": None, "shelfId": 1,
                         "slotId": 1,"onuId": 2, "name": "test_gem1",}, {"tcontId": [1, "tcontId"],
                                                                         "name": ["test_gem1", "name"],
                                                                         "onuId": [2, "onuId"],
                                                                         "gemId": [1, "gemId"]},result="Pass",method="ADD"),
Gem_service_profile(3, { "gemId": "2", "tcontId": 1,"tcontName": "", "nodeId": None, "shelfId": 1,
                         "slotId": 1,"onuId": 2, "name": "test_gem2",}, {"tcontId": [1, "tcontId"],
                                                                         "name": ["test_gem2", "name"],
                                                                         "onuId": [2, "onuId"],
                                                                         "gemId": [2, "gemId"]},result="Pass",method="ADD"),

)

Gem_service_profile_Delete_Config = (
    Gem_service_profile(1, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 1, "gemId": 1},result="Pass",method="DELETE"), 
    Gem_service_profile(2, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 2, "gemId": 1},result="Pass",method="DELETE"), 
    Gem_service_profile(2, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 2, "gemId": 2},result="Pass",method="DELETE"), 

)
#****************************************************************************************************************************

olt_service_profile = namedtuple('olt_service_profile', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
olt_service_profile.__new__.__defaults__ = (None, {}, {},None, None)

olt_service_profile_Data_Config = (
# olt_service_profile(1, {"servicePortId": "1","nodeId": None,"shelfId": 1, "slotId": 1, "portShowName": "PON ",
#                         "onuId": 1,"gemId": 1,"vlan": 0,"svlan": 0,"userVlan": "10","innerVlan": 0,
#                         "vlanPriority": 0,"svlanPriority": 0,"vlanPriorityAction": "1","svlanPriorityAction": "1",
#                         "cosQueueProfileId": 0,"queue": 0,"queueSelectMode": 0,"upLinkC2CId": 0,"downLinkC2CId": 0,}, {"servicePortId": [1, "servicePortId"],
#                                                                                                                        "userVlan": [10, "userVlan"],
#                                                                                                                        "onuId": [1, "onuId"],
#                                                                                                                        "gemId": [1, "gemId"]},result="Pass",method="ADD"),

olt_service_profile(2, {"servicePortId": "1","nodeId": None,"shelfId": 1, "slotId": 1, "portShowName": "PON ",
                        "onuId": 2,"gemId": 1,"vlan": 0,"svlan": 0,"userVlan": "10","innerVlan": 0,
                        "vlanPriority": 0,"svlanPriority": 0,"vlanPriorityAction": "1","svlanPriorityAction": "1",
                        "cosQueueProfileId": 0,"queue": 0,"queueSelectMode": 0,"upLinkC2CId": 0,"downLinkC2CId": 0,}, {"servicePortId": [1, "servicePortId"],
                                                                                                                       "userVlan": [10, "userVlan"],
                                                                                                                       "onuId": [2, "onuId"],
                                                                                                                       "gemId": [1, "gemId"]},result="Pass",method="ADD"),
olt_service_profile(3, {"servicePortId": "2","nodeId": None,"shelfId": 1, "slotId": 1, "portShowName": "PON ",
                        "onuId": 2,"gemId": 2,"vlan": 0,"svlan": 0,"userVlan": "11","innerVlan": 0,
                        "vlanPriority": 0,"svlanPriority": 0,"vlanPriorityAction": "1","svlanPriorityAction": "1",
                        "cosQueueProfileId": 0,"queue": 0,"queueSelectMode": 0,"upLinkC2CId": 0,"downLinkC2CId": 0,}, {"servicePortId": [2, "servicePortId"],
                                                                                                                       "userVlan": [11, "userVlan"],
                                                                                                                       "onuId": [2, "onuId"],
                                                                                                                       "gemId": [2, "gemId"]},result="Pass",method="ADD"),
)  

olt_service_profile_Delete_Config = (
    olt_service_profile(1, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 1, "servicePortId": 1},result="Pass",method="DELETE"), 
    olt_service_profile(1, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 2, "servicePortId": 2},result="Pass",method="DELETE"), 
    olt_service_profile(2, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 2, "servicePortId": 1},result="Pass",method="DELETE"), 
)
#*****************************************************************************
remote_service_profile = namedtuple('remote_service_profile', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
remote_service_profile.__new__.__defaults__ = (None, {}, {},None, None)

remote_service_profile_Data_Config = (
# remote_service_profile(1, {"nodeId": None,"shelfId": 1, "slotId": 1,"onuId": 1, "rmServiceId": "1","onuPortType": "VEIP",
#                            "onuPortId": 0,"vlanMode": "ACCESS","gemId": 1,"pvId": "10","priority": "1",}, {"rmServiceId": [1, "rmServiceId"],
#                                                                                                            "onuPortType": ["VEIP", "onuPortType"],
#                                                                                                            "vlanMode": ["ACCESS", "vlanMode"],
#                                                                                                            "priority": [1, "priority"],
#                                                                                                            "pvId": [10, "pvId"],
#                                                                                                            "onuId": [1, "onuId"],
#                                                                                                            "gemId": [1, "gemId"]},result="Pass",method="ADD"),

remote_service_profile(2, {"nodeId": None,"shelfId": 1, "slotId": 1,"onuId": 2, "rmServiceId": "1","onuPortType": "ETH_UNI",
                           "onuPortId": 0,"vlanMode": "TRUNK", "vlanList":"10", "gemId": 1,"pvId": None,"priority": "1",}, {"rmServiceId": [1, "rmServiceId"],
                                                                                                           "onuPortType": ["ETH_UNI", "onuPortType"],
                                                                                                           "vlanMode": ["TRUNK", "vlanMode"],
                                                                                                           "vlanList": [10, "vlanList"],
                                                                                                           "priority": [0, "priority"],
                                                                                                           "pvId": [0, "pvId"],
                                                                                                           "onuId": [2, "onuId"],
                                                                                                           "gemId": [1, "gemId"]},result="Pass",method="ADD"),
remote_service_profile(3, {"nodeId": None,"shelfId": 1, "slotId": 1,"onuId": 2, "rmServiceId": "2","onuPortType": "ETH_UNI",
                           "onuPortId": 0,"vlanMode": "TRUNK", "vlanList":"11", "gemId": 2,"pvId": None,"priority": "1",}, {"rmServiceId": [2, "rmServiceId"],
                                                                                                           "onuPortType": ["ETH_UNI", "onuPortType"],
                                                                                                           "vlanMode": ["TRUNK", "vlanMode"],
                                                                                                           "vlanList": [11, "vlanList"],
                                                                                                           "priority": [0, "priority"],
                                                                                                           "pvId": [0, "pvId"],
                                                                                                           "onuId": [2, "onuId"],
                                                                                                           "gemId": [2, "gemId"]},result="Pass",method="ADD"),
)  

remote_service_profile_Delete_Config = (
    remote_service_profile(1, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 1, "rmServiceId": 1},result="Pass",method="DELETE"), 
    remote_service_profile(2, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 2, "rmServiceId": 2},result="Pass",method="DELETE"), 
    remote_service_profile(3, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 2, "rmServiceId": 1},result="Pass",method="DELETE"), 
)
#*********************************************************************************
pon_init_info = namedtuple('pon_init_info', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
pon_init_info.__new__.__defaults__ = (None, {}, {},None, None)
  


pon_init_info_Enable_Multicast = pon_init_info(1, {"nodeId": None,"shelfId": 1,"slotId": 1,"portId": 2,"ifIndex": 2,"adminState": "DISABLE",
    "ponServiceEnable5100": "DISABLE","ponOnuAutoDiscovery": "ENABLE","ifModuleState5100": "DISABLED",
    "sfpModuleState5100": "DISABLED",   "ponMulticastState5100": 1,
    "operationalState": None,"scbPort": None,"modulePresent": 4,
    "scbMaxBw": None,"autoLearn": "ENABLE","operationalStateStr": "act_working","modulePresentStr": "Disabled"},{
                                                                                                            "portId": [2, "portId"],
                                                                                                            "ifIndex": [2, "ifIndex"],
                                                                                                            "adminState": ["DISABLE", "adminState"],
                                                                                                            "ponServiceEnable5100": ["DISABLE", "ponServiceEnable5100"],
                                                                                                            "ponOnuAutoDiscovery": ["ENABLE", "ponOnuAutoDiscovery"],
                                                                                                            "sfpModuleState5100": ["DISABLED", "sfpModuleState5100"],
                                                                                                            "ifModuleState5100": ["DISABLED", "ifModuleState5100"],
                                                                                                            "ponMulticastState5100": [1, "ponMulticastState5100"],
                                                                                                            "autoLearn": ["ENABLE", "autoLearn"],
                                                                                                            "operationalStateStr": ["inactive", "operationalStateStr"],
                                                                                                            "modulePresentStr": ["Disabled", "modulePresentStr"],},result="Pass",method="UPDATE"),                                                          
pon_init_info_Disable_Multicast = pon_init_info(1, {"nodeId": None,"shelfId": 1,"slotId": 1,"portId": 2,"ifIndex": 2,"adminState": "DISABLE",
    "ponServiceEnable5100": "DISABLE","ponOnuAutoDiscovery": "ENABLE","ifModuleState5100": "DISABLED",
    "sfpModuleState5100": "DISABLED",   "ponMulticastState5100": 0,
    "operationalState": None,"scbPort": None,"modulePresent": 4,
    "scbMaxBw": None,"autoLearn": "ENABLE","operationalStateStr": "act_working","modulePresentStr": "Disabled"},{
                                                                                                            "portId": [2, "portId"],
                                                                                                            "ifIndex": [2, "ifIndex"],
                                                                                                            "adminState": ["DISABLE", "adminState"],
                                                                                                            "ponServiceEnable5100": ["DISABLE", "ponServiceEnable5100"],
                                                                                                            "ponOnuAutoDiscovery": ["ENABLE", "ponOnuAutoDiscovery"],
                                                                                                            "sfpModuleState5100": ["DISABLED", "sfpModuleState5100"],
                                                                                                            "ifModuleState5100": ["DISABLED", "ifModuleState5100"],
                                                                                                            "ponMulticastState5100": [0, "ponMulticastState5100"],
                                                                                                            "autoLearn": ["ENABLE", "autoLearn"],
                                                                                                            "operationalStateStr": ["inactive", "operationalStateStr"],
                                                                                                            "modulePresentStr": ["Disabled", "modulePresentStr"],},result="Pass",method="UPDATE")                                                         

pon_init_info_no_shutdown = pon_init_info(3, {"nodeId": None,"shelfId": 1,"slotId": 1,"portId": 2,"ifIndex": 2,"adminState": "ENABLE",
    "ponServiceEnable5100": "ENABLE","ponOnuAutoDiscovery": "ENABLE","ifModuleState5100": "DISABLED",
    "sfpModuleState5100": "DISABLED", "ponMulticastState5100": 0,"operationalState": None,"scbPort": None,"modulePresent": 4,
    "scbMaxBw": None,"autoLearn": "ENABLE","operationalStateStr": "act_working","modulePresentStr": "Disabled"},{
                                                                                                            "portId": [2, "portId"],
                                                                                                            "ifIndex": [2, "ifIndex"],
                                                                                                            "adminState": ["ENABLE", "adminState"],
                                                                                                            "ponServiceEnable5100": ["ENABLE", "ponServiceEnable5100"],
                                                                                                            "ponOnuAutoDiscovery": ["ENABLE", "ponOnuAutoDiscovery"],
                                                                                                            "sfpModuleState5100": ["ENABLED", "sfpModuleState5100"],
                                                                                                            "ifModuleState5100": ["ENABLED", "ifModuleState5100"],
                                                                                                            "ponMulticastState5100": [0, "ponMulticastState5100"],
                                                                                                            "autoLearn": ["ENABLE", "autoLearn"],
                                                                                                            "operationalStateStr": ["act_working", "operationalStateStr"],
                                                                                                            "modulePresentStr": ["Enabled", "modulePresentStr"],},result="Pass",method="UPDATE")                                                          

pon_init_info_shutdown = pon_init_info(1, {"nodeId": None,"shelfId": 1,"slotId": 1,"portId": 2,"ifIndex": 2,"adminState": "DISABLE",
    "ponServiceEnable5100": "DISABLE","ponOnuAutoDiscovery": "ENABLE","ifModuleState5100": "DISABLED",
    "sfpModuleState5100": "DISABLED",   "ponMulticastState5100": 0,"operationalState": None,"scbPort": None,"modulePresent": 4,
    "scbMaxBw": None,"autoLearn": "ENABLE","operationalStateStr": "act_working","modulePresentStr": "Disabled"},{
                                                                                                            "portId": [2, "portId"],
                                                                                                            "ifIndex": [2, "ifIndex"],
                                                                                                            "adminState": ["DISABLE", "adminState"],
                                                                                                            "ponServiceEnable5100": ["DISABLE", "ponServiceEnable5100"],
                                                                                                            "ponOnuAutoDiscovery": ["ENABLE", "ponOnuAutoDiscovery"],
                                                                                                            "sfpModuleState5100": ["DISABLED", "sfpModuleState5100"],
                                                                                                            "ifModuleState5100": ["DISABLED", "ifModuleState5100"],
                                                                                                            "ponMulticastState5100": [0, "ponMulticastState5100"],
                                                                                                            "autoLearn": ["ENABLE", "autoLearn"],
                                                                                                            "operationalStateStr": ["inactive", "operationalStateStr"],
                                                                                                            "modulePresentStr": ["Disabled", "modulePresentStr"],},result="Pass",method="UPDATE")                                                         
#*********************************************************************************************************************************

pon_protection = namedtuple('pon_protection', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
pon_protection.__new__.__defaults__ = (None, {}, {},None, None)

Pon_Protection_Add = pon_protection(1, {"nodeId": 11,"shelfId": 1,"slotId": 1,"groupIndex": 1,"groupName": "group1","workingPort": 2,
                        "protectionPort": 3,"activePort": 2,"groupState": 1,"groupSwitchOver": "W2P"}, {"groupIndex": [1, "groupIndex"],
                                                                                                        "groupName": ["group1", "groupName"],
                                                                                                        "workingPort": [2, "workingPort"],
                                                                                                        "protectionPort" :[3,"protectionPort"],
                                                                                                        "activePort" :[2,"activePort"],
                                                                                                        "groupState" :[1,"groupState"],
                                                                                                        "groupSwitchOver" :["W2P","groupSwitchOver"],    
                                                                                                        "gemId": [1, "gemId"]},result="Pass",method="ADD")
  

Pon_Protection_Delete = pon_protection(1, {"nodeId": 11,"shelfId": 1,"slotId": 1,"groupIndex": 1}, result="Pass",method="DELETE")
#*********************************************************************************************************************************
dict_Serial_Mapping_Vlan = {"UTEL20FD749E":111, "HWTC20b3c380":112,"ESGP0C005730":113, "UTEL20FC5178":114,
                            "HWTCF448E19E":115, "UTEL20FC4D18":116, "UTEL20FD827E":117,"HWTC5A93CF3F":118,
                            "ELTX74004b9c":119, "HWTC20B3DAF0":220, "HWTC20F3C478":221,"ELTX7400A540":222,
                            "HWTC1A74B09C":223, "HWTCA3A8E09C":224, "HWTCA67EDEA4":225,"HWTC96610DA3":226,
                            "HWTCD2099E7C":227, "UTEL20FC5410":228, "HWTC20B3E9E8":229,"HWTCA4C5349C":330,
                            "HWTC41D47EAC":331, "HWTC7758307C":332, "HWTC20B3CC30":333,"HWTC20B3E9D8":334,
                            "ELTX6C0016E8":335, "ELTX6C001AF0":336, "ELTX7400d898":337,"ELTX740082f0":338,
                            "HWTC8f30f67c":800, "UTEL20fc4ce0":12, "HWTC50ac3392":11, "HWTC9c828f95":700, 
                            "HWTC20f3ce08":700, "HWTC20b3cc48": 700, "HWTC20f3ce08":700,"HWTC20b3cb18":700}
mac = {"HWTC50ac3392":"AC:F9:70:25:B2:93",
       "HWTC20f3ce08": "00:80:16:93:1A:39"}
#"HWTC20f3ce08":250 for utel ont 192.168.1.1
           