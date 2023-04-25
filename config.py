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
Qos_Policy_conf = namedtuple('Qos_Policy_conf', ['index','qosIndex', 'qosPolicyName', 'qosPolicyClassName',
                        'qosPolicyPolicerBucket', 'qosPolicyPolicerCBS', 'qosPolicyPolicerCIR',
                        'qosPolicyPolicerEBS', 'qosPolicyPolicerExceedAction','result' ,'shelfId', 
                        'slotId', 'nodeId'])
Qos_Policy_conf.__new__.__defaults__ = (None, None, None, None, None, None, None, None, None, "Pass", 1, 1, None)
Qos_Policy_DATA_conf = (
    Qos_Policy_conf(1, "1", "P", "C", "CBS", "1000", "1000", "2000", "DROP"),
    Qos_Policy_conf(2, "2", "D", "B", "FULL", "1000", "1000", "2000","DROP"),
    Qos_Policy_conf(3, 1),
    Qos_Policy_conf(4, 2))

#*****************************************************************************************************************************
Port_L2_conf = namedtuple('Port_L2_conf', [ "ethIfIndex", 'ethIfTxStatus','phyIfState', 'phyIfSpeed',
                                 'phyIfMtu', 'phyIfFlowControl', 'phyIfLoopback', 'phyIfDuplex', 
                                 'phyIfDesc', 'result', 'shelfId', 'slotId', 'nodeId'])
Port_L2_conf.__new__.__defaults__ = (None, 1, -1, "S10G", 1500, "NO", -1, "FULL", "", "Pass", 1, 1, None)    
#*****************************************************************************************************************************
Port_Stp_conf = namedtuple('Port_Stp_conf', ['stpIndex', 'stpIfStpAutoEdge','stpIfStpBpduFilter', 'stpIfStpBpduGuard',
                      'stpIfStpEdgePort', 'stpIfStpPortFast', 'stpIfStpRootGuard', 'result','shelfId', 'slotId', 'nodeId'])
Port_Stp_conf.__new__.__defaults__ = (None, -1, "NO", "NO", -1, -1, -1, "Pass", 1, 1, None)
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