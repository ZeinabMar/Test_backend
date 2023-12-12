import pytest
import logging
import json
from config import *
from conftest import *

pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
logging.basicConfig(level=logging.DEBUG)

onu_type = namedtuple('onu_type', ['index', 'expected_result_Set', 'expected_result_Get', "result", "method"])                                       
onu_type.__new__.__defaults__ = (None, {}, {},None, None)



onu_type_Data = (
onu_type(1, {
    "name": "onu2","ethPortNumber": "2","potsPortNumber": "4","downQueueNumber": "1","cardNumber": "2",
    "onuId": 2,"nodeId": 11,"shelfId": 1,"slotId": 1,"defaultProfile": None,"inuse": None,"tcontNum": None,
    "gemPortNum": None,"upQueueNum": None,"servicePortNum": None,"hostNum": None,"wifiNumber": 0,},
                                                           {"name": ["onu2", "name"],
                                                            "onuId":[2, "onuId"],
                                                            "ethPortNumber": [2, "ethPortNumber"],
                                                            "potsPortNumber": [4, "potsPortNumber"],
                                                            "downQueueNumber": [1, "downQueueNumber"],
                                                            "cardNumber": [2, "cardNumber"]},result="Pass",method="ADD"),  
onu_type(2, {
    "name": "onu3","ethPortNumber": "2","potsPortNumber": "4","downQueueNumber": "1","cardNumber": "2",
    "onuId": 3,"nodeId": 11,"shelfId": 1,"slotId": 1,"defaultProfile": None,"inuse": None,"tcontNum": None,
    "gemPortNum": None,"upQueueNum": None,"servicePortNum": None,"hostNum": None,"wifiNumber": 0,},
                                                           {"name": ["onu3", "name"],
                                                            "onuId":[3, "onuId"],
                                                            "ethPortNumber": [2, "ethPortNumber"],
                                                            "potsPortNumber": [4, "potsPortNumber"],
                                                            "downQueueNumber": [1, "downQueueNumber"],
                                                            "cardNumber": [2, "cardNumber"]},result="Pass",method="ADD"), 
# onu_type(3, {
#     "name": "onu4","ethPortNumber": "2","potsPortNumber": "4","downQueueNumber": "1","cardNumber": "2",
#     "onuId": 1,"nodeId": 11,"shelfId": 1,"slotId": 1,"defaultProfile": None,"inuse": None,"tcontNum": None,
#     "gemPortNum": None,"upQueueNum": None,"servicePortNum": None,"hostNum": None,"wifiNumber": 0,},
#                                                            {"name": ["onu4", "name"],
#                                                             "onuId":[4, "onuId"],
#                                                             "ethPortNumber": [2, "ethPortNumber"],
#                                                             "potsPortNumber": [4, "potsPortNumber"],
#                                                             "downQueueNumber": [1, "downQueueNumber"],
#                                                             "cardNumber": [2, "cardNumber"]},result="Fail",method="ADD"),   #onuId should be uniqe                                                            

)
onu_type_Delete= (
    onu_type(1, {"onuId": 2,"nodeId": 11,"shelfId": 1,"slotId": 1,},result="Pass",method="DELETE"),  
    onu_type(2, {"onuId": 3,"nodeId": 11,"shelfId": 1,"slotId": 1,},result="Pass",method="DELETE"),  

)
def Onu_Type_Profile(rest_interface_module, node_id, onu_type_data=onu_type(), method='ADD'):
    method = onu_type_data.method
    logger.info(f'ONU TYPE PROFILE TEST DATA ------- > {onu_type_data.index}')
    expected_set = onu_type_data.expected_result_Set
    expected_set["nodeId"]= node_id
    expected_get = onu_type_data.expected_result_Get  

    logger.info(f"TRY TO {method} ONU TYPE PROFILE CONFIG ...")
    if method == 'ADD':
        url = "/api/gponconfig/onuProfile/add"
        response = rest_interface_module.post_request(url, expected_set) 
    else:  # method==DELETE   
        url = f"/api/gponconfig/onuProfile/delete/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["onuId"])
        response = rest_interface_module.delete_request(url)

    if onu_type_data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in ONU TYPE PROFILE {expected_set}'
        if response.status_code != 200:
            logger.error(response.message)
        if len(expected_get.keys()) !=0:
            logger.info(f' GETTING ONU TYPE PROFILE (after {method} method) ... ')
            read_data = rest_interface_module.get_request(f"/api/gponconfig/onuProfile/getall?nodeId="+str(expected_set["nodeId"])+"&shelfId="+str(expected_set["shelfId"])+"&slotId="+str(expected_set["slotId"]))
            input_data_getall = json.loads(read_data.text)
            input_data = find_in_getall(input_data_getall, "onuId", expected_get["onuId"][0])
            for key in expected_get.keys():
                logger.info(f"{method} IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
            logger.info(f'check is completed in {method} method')
    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in ONU TYPE PROFILE {expected_set}'
        if len(expected_get.keys()) !=0:
            logger.info(f' GETTING ONU TYPE PROFILE (after {method} method) ... ')
            read_data = rest_interface_module.get_request(f"/api/gponconfig/onuProfile/getall?nodeId="+str(expected_set["nodeId"])+"&shelfId="+str(expected_set["shelfId"])+"&slotId="+str(expected_set["slotId"]))
            input_data_getall = json.loads(read_data.text)
            input_data = find_in_getall(input_data_getall, "name", expected_get["namedba"][0])
            for key in expected_get.keys():
                logger.info(f"set steeep IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)




def test_Onu_Type_Profile(rest_interface_module, node_id):
    response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/onuProfile/getall?nodeId={node_id}&shelfId=1&slotId=1")
    for onu_t_p in onu_type_Data:
        Onu_Type_Profile(rest_interface_module, node_id, onu_t_p)
    for onu_t_p in onu_type_Delete:
        Onu_Type_Profile(rest_interface_module, node_id, onu_t_p)

    