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
    uplink_vlan_conf(2, 2, "TRUNK", -1, "", "", "10-12"),
    uplink_vlan_conf(3, 4, "HYBRID", 10, "", "", "10-12"),
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
Port_Mstp_conf = namedtuple('Port_Mstp_conf', ['index','ifIndex', 'instanceIfIndex','mstpInstanceIfPathCost', 
                       'mstpInstanceIfPriority', 'result','shelfId', 'slotId', 'nodeId'])
Port_Mstp_conf.__new__.__defaults__ = (None, None, -1, "NO", "NO", -1, -1, -1, "Pass", 1, 1, None)
Port_Mstp_conf_DATA = (
    Port_Mstp_conf(1, None, -1, "ENABLE", "NO", 1, -1, -1, "Pass"),
)
#*****************************************************************************************************************************
Bridge_Mstp_conf = namedtuple('Bridge_Mstp_conf', ['index', 'instanceIndex', 'mstpInstanceBridgeId','mstpInstanceVlan', 
                       'mstpInstanceVlanClr','mstpInstanceVlanSet', 'result','shelfId', 'slotId', 'nodeId'])
Bridge_Mstp_conf.__new__.__defaults__ = (None, 1, "", "", "", "Pass", 1, 1, None)
Bridge_Mstp_DATA_conf = (
    Bridge_Mstp_conf(1, 5, 1, None, None, "10-12,17-19", "Pass", 1, 1, None),
    Bridge_Mstp_conf(2, 5))
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
dba_profile.__new__.__defaults__ = (None, {}, [],None)
dba_profile_Data_Config = (
dba_profile(1, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":None,"name": "dba1_type1", "dbaType": 1, "fixedBwValue": 32000, "assureBwValue": None, "maxBwValue": None},
                                                          [{
                                                            "namedba": ["dba1_type1", "name"],
                                                            "dbatype": [1, "dbaType"],
                                                            "fixedbwvalue": [32000, "fixedBwValue"],
                                                            "assurebwvalue": [32250, "assureBwValue"],
                                                            "maxbwvalue": [32500, "maxBwValue"]}],result="Pass"),
                                                            
                                                            
# dba_profile(2, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":None,"name": "dba2_type2", "dbaType": 2, "fixedBwValue": None, "assureBwValue": 128000, "maxBwValue": None},
#                                                            [{
#                                                             "namedba": ["dba1_type1", "name"],
#                                                             "dbatype": [1, "dbaType"],
#                                                             "fixedbwvalue": [32000, "fixedBwValue"],
#                                                             "assurebwvalue": [32250, "assureBwValue"],
#                                                             "maxbwvalue": [32500, "maxBwValue"]}
#                                                             ,{
#                                                             "namedba": ["dba2_type2", "name"],
#                                                             "dbatype": [1, "dbaType"],
#                                                             "fixedbwvalue": [None, "fixedBwValue"],
#                                                             "assurebwvalue": [128000, "assureBwValue"],
#                                                             "maxbwvalue": [None, "maxBwValue"]}],result="Pass"), 
# dba_profile(3, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":None,"name": "dba3_type3", "dbaType": 3, "fixedBwValue": 250, "assureBwValue": 500, "maxBwValue": 1000},
#                                                            [{
#                                                             "namedba": ["dba1_type1", "name"],
#                                                             "dbatype": [1, "dbaType"],
#                                                             "fixedbwvalue": [32000, "fixedBwValue"],
#                                                             "assurebwvalue": [32250, "assureBwValue"],
#                                                             "maxbwvalue": [32500, "maxBwValue"]}
#                                                             ,{
#                                                             "namedba": ["dba2_type2", "name"],
#                                                             "dbatype": [1, "dbaType"],
#                                                             "fixedbwvalue": [None, "fixedBwValue"],
#                                                             "assurebwvalue": [128000, "assureBwValue"],
#                                                             "maxbwvalue": [None, "maxBwValue"]}
#                                                             ,{
#                                                             "namedba": ["dba3_type3", "name"],
#                                                             "dbatype": [3, "dbaType"],
#                                                             "fixedbwvalue": [250, "fixedBwValue"],
#                                                             "assurebwvalue": [250, "assureBwValue"],
#                                                             "maxbwvalue": [250, "maxBwValue"]}],result="Pass"),                                                            
                                                            
                                                            
                                                             ) 
dba_profile_Data_Config_Delete = (
dba_profile(1, {"nodeId":None, "slotId":1,"shelfId":1,"dbaId":1},{"message": ["", "message"],},result="Pass"),)
#********************************************************************************************************
tcont = namedtuple('tcont', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
tcont.__new__.__defaults__ = (None, {}, {},None, None)

tcont_Data_Config = (
tcont(1, {"nodeId":None, "slotId":1,"shelfId":1,"bwProfileId":1,"bwProfileName": "dba1_type1", "name": "tcont_valid8", "onuId": 1, "portId": 1, "tcontId": 8},
                                                           {
                                                            "bwProfileId": [1, "bwProfileId"],
                                                            "bwProfileName": ["dba1_type1", "bwProfileName"],
                                                            "name": ["tcont_valid8", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [1, "portId"],
                                                            "tcontId": [8, "tcontId"]},result="Pass",method="ADD"),  
tcont(2, {"nodeId":None, "slotId":1,"shelfId":1,"bwProfileId":2,"bwProfileName": "dba2_type2", "name": "tcont_valid6", "onuId": 1, "portId": 1, "tcontId": 6},
                                                           {
                                                            "bwProfileId": [2, "bwProfileId"],
                                                            "bwProfileName": ["dba2_type2", "bwProfileName"],
                                                            "name": ["tcont_valid6", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [1, "portId"],
                                                            "tcontId": [6, "tcontId"]},result="Pass",method="ADD"),  
tcont(3, {"nodeId":None, "slotId":1,"shelfId":1,"bwProfileId":3,"bwProfileName": "dba3_type3", "name": "tcont_valid4", "onuId": 1, "portId": 1, "tcontId":4},
                                                           {
                                                            "bwProfileId": [3, "bwProfileId"],
                                                            "bwProfileName": ["dba3_type3", "bwProfileName"],
                                                            "name": ["tcont_valid4", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [1, "portId"],
                                                            "tcontId": [4, "tcontId"]},result="Pass",method="ADD"), 
 tcont(4, {"nodeId":None, "slotId":1,"shelfId":1,"bwProfileId":4,"bwProfileName": "dba4_type4", "name": "tcont_valid2", "onuId": 1, "portId": 1, "tcontId": 2},
                                                           {
                                                            "bwProfileId": [4, "bwProfileId"],
                                                            "bwProfileName": ["dba4_type4", "bwProfileName"],
                                                            "name": ["tcont_valid2", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [1, "portId"],
                                                            "tcontId": [2, "tcontId"]},result="Pass",method="ADD"),                                                                                                                                                                                
)

tcont_Data_Delete_Config = (
    tcont(1, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 1, "portId": 1, "tcontId": 2},result="Pass",method="DELETE"),    
    tcont(2, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 1, "portId": 1, "tcontId": 4},result="Pass",method="DELETE"),                                                                                                                                                                                
    tcont(3, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 1, "portId": 1, "tcontId": 6},result="Pass",method="DELETE"),                                                                                                                                                                                
    tcont(4, {"nodeId":None, "slotId":1,"shelfId":1, "onuId": 1, "portId": 1, "tcontId": 8},result="Pass",method="DELETE"),                                                                                                                                                                                                                                                                                                                                                            
)

#********************************************************************************************************
gem_data_for_other_TCs=[
    {"gemId": "1", "name": "gem_test1", "onuId": 1, "portId": 1,"tcontId": 1, "tcontName": "tcont-test","result": "Pass"},
    {"gemId": "2", "name": "gem2", "onuId": 1, "portId": 1, "tcontId": 1, "tcontName": "tcont-test", "result": "Pass"}]
gem_profile = namedtuple('gem_profile', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
gem_profile.__new__.__defaults__ = (None, {}, {},None, None)

gem_profile_Data_Config = (
gem_profile(1, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"1","name": "gem_test1", "onuId": 1, "portId": 1, "tcontId": 8},
                                                           {
                                                            "gemid": [1, "gemId"],
                                                            "name": ["gem_test1", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [1, "portId"],
                                                            "tcontId": [8, "tcontId"]},result="Pass",method="ADD"), 
gem_profile(2, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"2","name": "gem_test2", "onuId": 1, "portId": 1, "tcontId": 6},
                                                           {
                                                            "gemid": [2, "gemId"],
                                                            "name": ["gem_test2", "name"],
                                                            "onuId": [1, "onuId"],
                                                            "portId": [1, "portId"],
                                                            "tcontId": [6, "tcontId"]},result="Pass",method="ADD"),)
gem_profile_Data_Delete_Config= (
    gem_profile(1, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"1","name": "gem1", "onuId": 1, "portId": 1, "tcontId": 8},result="Pass",method="DELETE"), 
    gem_profile(2, {"nodeId":None, "slotId":1,"shelfId":1,"gemId":"2","name": "gem2", "onuId": 1, "portId": 1, "tcontId": 6},result="Pass",method="DELETE"), 
)

