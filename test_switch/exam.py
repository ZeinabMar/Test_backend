import pytest
import logging
import json
# import data.mibs
# from lib.restlib import rest_interface_module as rest_interface
# from config import *
# from test_switch.test_vlan import vlan_config
# from test_switch.bridge_funcs import bridge_config
# from test_switch.test_Bridge_group_conf import switch_config
import re

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
key=""
def set_and_clear_data(input_data=d_string):
    string_t = ""
    if input_data.find("-")!=-1 and input_data.find(",")!=-1:
        result = input_data.split(",")
        array_total_2 =[]
        array_total_1 =[]
        for element in result:
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
        result = input_data.split(",")
        array_total_1 =[]
        for element in result:
            array_total_1.append(int(float(element)))
    else:
        string_t = input_data
        return string_t

    for i in array_total_1:
        string_t = string_t +f"{i},"
    string_t = string_t[:-1:] 
    return string_t

string_t = set_and_clear_data("10-12,17-19")
string_t = re.findall('\d+', string_t)
print(string_t[0])
# print((lis[0]))