# import pytest
# import logging
# import json
# from config import *
# from conftest import *
# from Switch.test_Qos_class_definition import Qos_Class_config
# from Switch.test_Qos_management import Qos_Manage_config
# from Switch.test_vlan import vlan_config
# from Switch.bridge_funcs import bridge_config
# from Switch.test_Bridge_group_conf import switch_config


# # from pytest-check import check

# pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)


# Vlan_Map = namedtuple('Vlan_Map', ['index', 'expected_result_Set', 'expected_result_Get', "result", "shelfId", "slotId", 'nodeId', "ifIndex"])                                       
# Vlan_Map.__new__.__defaults__ = (None, {}, [],None, 1, 1, None, None)

# Vlan_Map_Data = (
#     Vlan_Map(1, {"nodeId":None,
#                    "slotId":1,
#                    "shelfId":1,
#                    "ifIndex":1,
#                    "vlanId":10 ,
#                    "vlanTranslatedId":11,}, [{"vlanid": [10, "vlanId"],
#                                             "vlantranslatedid": [11, "vlanTranslatedId"],}], result="Pass"),
#     Vlan_Map(2, {"nodeId":None,
#                    "slotId":1,
#                    "shelfId":1,
#                    "ifIndex":1,
#                    "vlanId":11 ,
#                    "vlanTranslatedId":10,}, [{"vlanid": [10, "vlanId"],
#                                             "vlantranslatedid": [11, "vlanTranslatedId"],},{"vlanid": [11, "vlanId"],
#                                             "vlantranslatedid": [10, "vlanTranslatedId"],}], result="Pass"),
# )

# def Vlan_Map_config(rest_interface_module, node_id, Vlan_Map_data=Vlan_Map(),port=None, method='POST'):
#     logger.info(f'VLAN MAPPING TEST DATA ------- > {Vlan_Map_data.index}')
#     data = Vlan_Map_data._replace(nodeId=node_id)
#     expected_set = data.expected_result_Set
#     expected_set["nodeId"]= int(node_id)
#     expected_set["ifIndex"]= port
#     expected_get = data.expected_result_Get  
   
#     logger.info(f"TRY TO {method} Vlan_Map CONFIG ...")
#     if method == 'add':
#         url = "/api/gponconfig/sp5100/vlan/mapping/add"
#         response = rest_interface_module.post_request(url, expected_set) 
#     else:  # method==DELETE
#         url = f"/api/gponconfig/sp5100/vlan/mapping/delete/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"])+"/"+str(expected_set["ifIndex"])+"/"+str(expected_set["vlanId"])+"/"+str(expected_set["vlanTranslatedId"])
#         response = rest_interface_module.delete_request(url)

#     if data.result == "Pass":
#         assert response.status_code == 200, f'{method} ERROR in VLAN MAPPING config {expected_set}'
#         if response.status_code != 200:
#             logger.error(response.message)
#         logger.info(f' GETTING VLAN MAPPING (after {method} method) ... ')
#         read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/vlan/mapping/getall/"+str(expected_set["nodeId"])+"/"+str(expected_set["shelfId"])+"/"+str(expected_set["slotId"]))
#         for i in range(len(read_data)):
#             input_data = json.loads(read_data[i].text)
#         #**********************************************************************
#             if method == 'add' & "delete": 
#                 for key in expected_get[i].keys():
#                     logger.info(f"set steeep IN {expected_get[key]}")
#                     check_set_value(rest_interface_module, expected_get[i][key][0], expected_get[i][key][1],input_data)
#                 logger.info('set is completed.')

#     else:
#         assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in Qos_Policy config {data._asdict}'
#         if len(expected_get) !=0:
#             for i in range(len(read_data)):
#                 input_data = json.loads(read_data[i].text)
#         #**********************************************************************
#                 for key in expected_get[i].keys():
#                     logger.info(f"set steeep IN {expected_get[key]}")
#                     check_set_value(rest_interface_module, expected_get[i][key][0], expected_get[i][key][1],input_data)
#                 logger.info('set is completed.')





# def test_Vlan_Map_config(rest_interface_module, node_id):

#     # bridge_config(rest_interface_module, node_id, Bridge_conf(1, 'PROVIDER_MSTP_EDGE', 100, 30, maxAge=6, maxHops=1, priority=12288), method='POST')
#     # for vlan in VLAN_DATA_conf_S_C:
#     #     vlan_config(rest_interface_module, node_id, vlan, method='POST')  
#     # **************************************************************************************************************
#     for port in range(1,2):
#         switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port,index=4), method='POST') 
#         for vlan_map in Vlan_Map_Data:
#             Vlan_Map_config(rest_interface_module, node_id, vlan_map, port, method='add')

#     # #**************************************************************************************************************
#     # for vlan in VLAN_DATA_conf_S_C:
#     #         vlan_config(rest_interface_module, node_id, vlan, method='DELETE')
#     # bridge_config(rest_interface_module, node_id, Bridge_conf(1, 'PROVIDER_MSTP_EDGE', 100, 30, maxAge=6, maxHops=1, priority=12288), method='DELETE')

