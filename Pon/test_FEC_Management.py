import pytest
import logging
import json
from config import *
from conftest import *
from Pon.test_Pon_Initial_Information import Pon_Initial_Information


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)

fec_management = namedtuple('fec_management', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
fec_management.__new__.__defaults__ = (None, {}, {},None, None)


fec_management_Data_Pon = (
fec_management(1, { "nodeId": None, "shelfId": 1,  "slotId": 1, "portId": 2,  "ifIndex": 2, 
                    "adminState": None, "dsFec": "ENABLE",},{
                                                              "portId": [2, "portId"],
                                                              "ifIndex": [2, "ifIndex"],
                                                              "dsFec": ["ENABLE", "dsFec"],},result="Pass",method="UPDATE"),  
fec_management(2, { "nodeId": None, "shelfId": 1,  "slotId": 1, "portId": 2,  "ifIndex": 2, 
                    "adminState": None, "dsFec": "DISABLE",},{
                                                              "portId": [2, "portId"],
                                                              "ifIndex": [2, "ifIndex"],
                                                              "dsFec": ["DISABLE", "dsFec"],},result="Pass",method="UPDATE"),                                                                                                                       
)


fec_management_Data_Onu = (
fec_management(1, { "nodeId": None, "shelfId": 1,  "slotId": 1, "portId": 2,  "onuId": 1, 
                    "upstreamFec": "ENABLE"},{"portId": [2, "portId"],
                                                              "onuId": [1, "onuId"],
                                                              "upstreamFec": ["ENABLE", "upstreamFec"],},result="Pass",method="UPDATE"),
fec_management(2, { "nodeId": None, "shelfId": 1,  "slotId": 1, "portId": 2,  "onuId": 1, 
                    "upstreamFec": "DISABLE"},{"portId": [2, "portId"],
                                                              "onuId": [1, "onuId"],
                                                              "upstreamFec": ["DISABLE", "upstreamFec"],},result="Pass",method="UPDATE"),                                                                                                                         
)

def FEC_Management(rest_interface_module, node_id, fec_management_data=fec_management(), method='UPDATE', Operator = "Pon"):
    method = fec_management_data.method
    logger.info(f'FEC_Management TEST DATA ------- > {fec_management_data.index}')
    expected_set = fec_management_data.expected_result_Set
    expected_set["nodeId"]= node_id
    expected_get = fec_management_data.expected_result_Get  

    logger.info(f"TRY TO {method} FEC_Management in {Operator} ...")
    if method == "UPDATE":
        if Operator == "Pon":
            url = "/api/gponconfig/pon/savefec"
        else: 
            url = "/api/gponconfig/onu/savefec"   
        response = rest_interface_module.post_request(url, expected_set)     
    
    if fec_management_data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in FEC_Management in {Operator} config {expected_set}'
        if response.status_code != 200:
            logger.error(response.message)

        if len(expected_get.keys()) !=0: 
            logger.info(f' GETTING FEC_Management in {Operator} (after {method} method) ... ')
            if Operator == "Pon":
                read_data = rest_interface_module.get_request(f"/api/gponconfig/pon/getfec/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["ifIndex"]))
            else:    
                read_data = rest_interface_module.get_request(f"/api/gponconfig/onu/getfec/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"]))
            input_data = json.loads(read_data.text)
            #**********************************************************************
            for key in expected_get.keys():
                logger.info(f"{method} IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
            logger.info(f'check {Operator} is completed in {method} method')

    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in FEC_Management in {Operator} {tcont_data._asdict}'
        if len(expected_get.keys()) !=0:
            logger.info(f' GETTING FEC_Management in {Operator} (after {method} method) ... ')
            if Operator == "Pon":
                read_data = rest_interface_module.get_request(f"/api/gponconfig/pon/getfec/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["ifIndex"]))
            else:    
                read_data = rest_interface_module.get_request(f"/api/gponconfig/onu/getfec/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["portId"])+"/"+str(expected_set["onuId"]))
            input_data = json.loads(read_data.text)
            #**********************************************************************
            for key in expected_get.keys():
                logger.info(f"{method} IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)




def test_FEC_Management(rest_interface_module, node_id):
    # Pon_Initial_Information(rest_interface_module, node_id, pon_init_info_shutdown, method='UPDATE')       
    for fec_pon in fec_management_Data_Pon:
        FEC_Management(rest_interface_module, node_id, fec_pon, method='UPDATE', Operator= "Pon")       
    for fec_onu in fec_management_Data_Onu:
        FEC_Management(rest_interface_module, node_id, fec_onu, method='UPDATE', Operator= "Onu")  
    # Pon_Initial_Information(rest_interface_module, node_id, pon_init_info_no_shutdown, method='UPDATE')       
             