import pytest
import logging
import json
from config import *
from Switch.test_vlan import vlan_config
from Switch.bridge_funcs import bridge_config
from Switch.test_Bridge_group_conf import switch_config
import re
# from pytest-check import check


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

Bridge_Mstp = namedtuple('Bridge_Mstp', ['index','instanceIndex', 'mstpInstanceBridgeId','mstpInstanceVlan', 
                       'mstpInstanceVlanClr','mstpInstanceVlanSet', 'result','shelfId', 'slotId', 'nodeId'])
Bridge_Mstp.__new__.__defaults__ = (None, None, 1, "", "", "", "Pass", 1, 1, None)
Bridge_Mstp_DATA = (
    Bridge_Mstp(1, 5, 1, None, None, "10-12", "Pass", 1, 1, None),
    Bridge_Mstp(2, 4, 1, None, None, "19", "Pass", 1, 1, None),
    Bridge_Mstp(3, 5, 1, "10,11,12", "", "19", "Fail", 1, 1, None),
    Bridge_Mstp(4, 5, 1, "10,11,12", "", "17", "Pass", 1, 1, None),
    Bridge_Mstp(5, 5, 1, "10,11,12,17", "10", "", "Pass", 1, 1, None),
    Bridge_Mstp(6, 5),
    Bridge_Mstp(7, 4)
)
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

def Bridge_Mstp_config(rest_interface_module, node_id, Bridge_Mstp_data=Bridge_Mstp(), method='POST'):
    data = Bridge_Mstp_data._replace(nodeId=node_id)
    logger.info(f"TRY TO {method} Bridge_Mstp CONFIG ...")
    if method == 'add':
        url = "/api/gponconfig/sp5100/bridgemstpinstanceconfig/add"
        response = rest_interface_module.post_request(url, data._asdict()) 
    elif method == 'POST':  
        url = "/api/gponconfig/sp5100/bridgemstpinstanceconfig/update"
        response = rest_interface_module.post_request(url, data._asdict()) 
    else:  # method==DELETE
        url = f"/api/gponconfig/sp5100/bridgemstpinstanceconfig/delete/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.instanceIndex}"
        response = rest_interface_module.delete_request(url)


    if data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in Bridge_Mstp config {data._asdict}'
        if response.status_code != 200:
            logger.error(response.message)
        logger.info(f' GETTING Bridge_Mstp-config (after {method} method) ... ')

        read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/bridgemstpinstanceconfig/get/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.instanceIndex}")
        input_data = json.loads(read_data.text)
        logger.info(f'data after read input_data {input_data}')
        #*********************************************************
        if method == 'add':
            string_t = set_and_clear_data(data.mstpInstanceVlanSet)
            assert (input_data["instanceIndex"]==data.instanceIndex and
                    input_data["mstpInstanceBridgeId"] == 1 and 
                    input_data["mstpInstanceVlan"].find(str(string_t))!=-1),f'IN Everythig is ok Bridge_Mstp config(after {method}'
            logger.info(f'every thing ok after Bridge_Mstp config(after {method} ')

        elif method == 'POST':
            if len(data.mstpInstanceVlanClr)!=0:
                string_t = set_and_clear_data(data.mstpInstanceVlanClr)
                assert (input_data["instanceIndex"]==data.instanceIndex and
                        input_data["mstpInstanceBridgeId"] == 1 and 
                        str(input_data["mstpInstanceVlan"]).find(str(string_t)) == -1),f'IN Everythig is ok Bridge_Mstp config(after {method,string_t} with clear action'
            elif len(data.mstpInstanceVlanSet)!=0:
                string_t = set_and_clear_data(data.mstpInstanceVlanSet)
                assert (input_data["instanceIndex"]==data.instanceIndex and
                        input_data["mstpInstanceBridgeId"] == 1 and 
                        str(input_data["mstpInstanceVlan"]).find(str(string_t)) != -1),f'IN Everythig is ok Bridge_Mstp config(after {method} with set action'
            
            logger.info(f'every thing ok after Bridge_Mstp config(after {method} ')
        else:  # method==DELETE
            assert (input_data["instanceIndex"]==data.instanceIndex and
                    input_data["mstpInstanceBridgeId"] == None and 
                    input_data["mstpInstanceVlan"] == None and
                    input_data["mstpInstanceVlanSet"] == None and
                    input_data["mstpInstanceVlanClr"] == None ),f'GET ERROR in Bridge_Mstp config (after {method})'
    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in Bridge_Mstp config {data._asdict}'


def test_Bridge_Mstp_config(rest_interface_module, node_id):

    bridge_config(rest_interface_module, node_id, Bridge_conf(1, 'PROVIDER_MSTP_EDGE', 100, 30, maxAge=6, maxHops=1, priority=12288), method='POST')
    # ***************************************************************************
    for vlan in VLAN_DATA_conf_service:
        vlan_config(rest_interface_module, node_id, vlan, method='POST')  
    for vlan in VLAN_DATA_conf_CUSTOM:
        vlan_config(rest_interface_module, node_id, vlan, method='POST')   
    #******************************************************************    
    Bridge_Mstp_config(rest_interface_module, node_id, Bridge_Mstp_DATA[0], method='add')
    Bridge_Mstp_config(rest_interface_module, node_id, Bridge_Mstp_DATA[1], method='add')
    Bridge_Mstp_config(rest_interface_module, node_id, Bridge_Mstp_DATA[2], method='POST')
    Bridge_Mstp_config(rest_interface_module, node_id, Bridge_Mstp_DATA[3], method='POST')
    Bridge_Mstp_config(rest_interface_module, node_id, Bridge_Mstp_DATA[4], method='POST')
    Bridge_Mstp_config(rest_interface_module, node_id, Bridge_Mstp_DATA[5], method='DELETE')
    Bridge_Mstp_config(rest_interface_module, node_id, Bridge_Mstp_DATA[6], method='DELETE')
    # ******************************************************************
    for vlan in VLAN_DATA_conf_service:
        vlan_config(rest_interface_module, node_id, vlan, method='DELETE')  
    for vlan in VLAN_DATA_conf_CUSTOM:
        vlan_config(rest_interface_module, node_id, vlan, method='DELETE')   
    #*****************************************************************************
    bridge_config(rest_interface_module, node_id, Bridge_conf(1, 'PROVIDER_MSTP_EDGE', 100, 30, maxAge=6, maxHops=1, priority=12288), method='DELETE')






