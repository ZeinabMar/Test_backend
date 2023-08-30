import pytest
import logging
import json
from config import *
from Switch.bridge_funcs import bridge_config
from Switch.test_Bridge_group_conf import switch_config
from Switch.test_vlan import vlan_config
from Switch.test_uplink_port_Vlan_conf import uplink_vlan_config
# from pytest-check import check


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

Reg_QinQ_Table = namedtuple('Reg_QinQ_Table', ['index' ,'vlanId', 'vlanRegistrationName', 'vlanRegistrationBridgeId',
                       'vlanRegistrationCVlan', 'vlanRegistrationCVlanClr', 'vlanRegistrationCVlanSet', 'vlanRegistrationSVlan',
                       'vlanRegistrationSVlanSet', 'result', 'shelfId', 'slotId', 'nodeId'])
Reg_QinQ_Table.__new__.__defaults__ = (None, 1, "__NO__", 1, "", "", "", "", "", "Pass", 1, 1, None)

Reg_QinQ_Table_1_Data = (
    Reg_QinQ_Table(1, 1, "reg", 1, "", "10,11", "", "", "15,16", "Fail", 1, 1, None),#clr before set
    Reg_QinQ_Table(2, 1, "reg", 1, "", "", "10,11", "", "15,16", "Pass", 1, 1, None),
    Reg_QinQ_Table(3, 1, "reg", 1, "10,11", "", "10", "15,16", "16", "Fail", 1, 1, None),
    Reg_QinQ_Table(4, 1, "reg", 1, "10,11", "", "12", "15,16", "16", "Pass", 1, 1, None),
    Reg_QinQ_Table(5, 1, "reg", 1, "10,11,12", "", "17", "15,16,16", "18", "Fail", 1, 1, None),# set two svlan 
    Reg_QinQ_Table(6, 1, "reg", 1, "10,11,12", "", "13", "15,16,16", "14", "Fail", 1, 1, None),# set two cvlan 
    Reg_QinQ_Table(7, 1, "reg", 1, "10,11,12", "12", "", "15,16,16", "", "Pass", 1, 1, None),
    Reg_QinQ_Table(8, 1, "reg", 1, "10,11", "", "12", "15,16", "15", "Pass", 1, 1, None),
    Reg_QinQ_Table(9, 1, "reg", 1, "10,11,12", "10,11,12", "", "15,16,15", "", "Pass", 1, 1, None)
)

Reg_QinQ_Table_2_Data = (
    Reg_QinQ_Table(1, 2, "reg2", 1, "", "10,11", "", "", "15,16", "Fail", 1, 1, None),#clr before set
    Reg_QinQ_Table(2, 2, "reg2", 1, "", "", "10,11", "", "15,16", "Pass", 1, 1, None),
    Reg_QinQ_Table(3, 2, "reg2", 1, "10,11", "", "10", "15,16", "16", "Fail", 1, 1, None),
    Reg_QinQ_Table(4, 2, "reg2", 1, "10,11", "", "12", "15,16", "16", "Pass", 1, 1, None),
    Reg_QinQ_Table(5, 2, "reg2", 1, "10,11,12", "", "17", "15,16,16", "18", "Fail", 1, 1, None),# set two svlan 
    Reg_QinQ_Table(6, 2, "reg2", 1, "10,11,12", "", "13", "15,16,16", "14", "Fail", 1, 1, None),# set two cvlan 
    Reg_QinQ_Table(7, 2, "reg2", 1, "10,11,12", "12", "", "15,16,16", "", "Pass", 1, 1, None),
    Reg_QinQ_Table(8, 2, "reg2", 1, "10,11", "", "12", "15,16", "15", "Pass", 1, 1, None),
    Reg_QinQ_Table(9, 2, "reg2", 1, "10,11,12", "10,11,12", "", "15,16,15", "", "Pass", 1, 1, None)
)


def QinQ_registration_table_config(rest_interface_module, node_id, Reg_QinQ_Table_data=Reg_QinQ_Table(), method='POST', index=None):
    data = Reg_QinQ_Table_data._replace(nodeId=node_id)
    logger.info(f"TRY TO {method} Reg_QinQ_Table CONFIG ...")

    if method == "ADD":
        url = "/api/gponconfig/sp5100/qinqregistration/add"
        response = rest_interface_module.post_request(url, data._asdict())  

    elif method == 'Post':  
        url = "/api/gponconfig/sp5100/qinqregistration/update"
        response = rest_interface_module.post_request(url, data._asdict()) 

    elif method == "DELETE":
        url = f"/api/gponconfig/sp5100/qinqregistration/delete/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.vlanId}"
        response = rest_interface_module.delete_request(url)

    if data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in Reg_QinQ_Table config {data._asdict}'
        if response.status_code != 200:
            logger.error(response.message)
        logger.info(f' GETTING Reg_QinQ_Table (after {method} method) ... ')
        read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/qinqregistration/get/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.vlanId}")
        input_data = json.loads(read_data.text)
        logger.info(f'data after read input_data {input_data}')
        #*********************************************************
        if method == 'Post' or method == "ADD": 
            if len(data.vlanRegistrationCVlanSet)!=0 and len(data.vlanRegistrationSVlanSet)!=0:
                st1c = set_and_clear_data(str(data.vlanRegistrationCVlanSet))
                st1c = re.findall('\d+', st1c)
                st2c = set_and_clear_data(str(input_data["vlanRegistrationCVlan"]))
                st2c = re.findall('\d+', st2c)
                for i in range(len(st1c)):
                    assert st1c[i] in st2c

                st1s = set_and_clear_data(str(data.vlanRegistrationCVlanSet))
                st1s = re.findall('\d+', st1s)
                st2s = set_and_clear_data(str(input_data["vlanRegistrationCVlan"]))
                st2s = re.findall('\d+', st2s)

                for i in range(len(st1s)):
                    assert st1s[i] in st2s

                for index in range(len(st1c)):
                    assert st2c.index(st1c[index]) == st2s.index(st1s[index])
                
                assert (input_data["vlanId"] == data.vlanId and
                        str(input_data["vlanRegistrationName"]) == str(data.vlanRegistrationName) and 
                        len(input_data["vlanRegistrationCVlanClr"]) == 0 ),f'IN Everythig is ok Reg_QinQ_Table(after {method} with clear action'

                if index == 2 :
                    data_previous = input_data

                if index == 4:
                    pre = set_and_clear_data(str(data_previous["vlanRegistrationCVlan"]))[st1[len-1]]
                    pre = re.findall('\d+', pre)
                    now = set_and_clear_data(str(input_data["vlanRegistrationCVlan"]))
                    now = re.findall('\d+', now)
                    assert (pre[len(pre)-1] in now == False) ,f'dont earase previous cvlan (after {method} with clear action'
                    
            elif len(data.vlanRegistrationCVlanClr)!= 0 :
                counter1 = 0 
                stc_clr = set_and_clear_data(str(data.vlanRegistrationCVlanClr))
                stc_clr = re.findall('\d+', stc_clr)

                stc_set_p = set_and_clear_data(str(data_previous["vlanRegistrationCVlan"]))
                stc_set_p = re.findall('\d+', stc_set_p)

                sts_set_p = set_and_clear_data(str(data_previous["vlanRegistrationSVlan"]))
                sts_set_p = re.findall('\d+', sts_set_p)


                for item in stc_clr:
                    if set_and_clear_data(str(input_data["vlanRegistrationCVlan"])).find(item) == -1:
                        counter1 = counter1 +1    
                slan = []
                for i in len(stc_clr):
                    for j in len(stc_set_p):
                        if stc_clr[i] == stc_set_p[j]:
                            svlan.append(sts_set_p[j])

                assert (input_data["vlanId"] == data.vlanId and
                        str(input_data["vlanRegistrationName"]) == str(data.vlanRegistrationName) and 
                        len(input_data["vlanRegistrationCVlanSet"] == 0 and
                        counter1 == len(stc_clr))),f'IN Everythig is ok Reg_QinQ_Table(after {method} with set action'
                for index in len(svlan):
                    assert (set_and_clear_data(str(input_data["vlanRegistrationSVlan"])).find(str(svlan[index])) == -1),f'IN cleaning cvlan(after {method} with set action'
            logger.info(f'every thing ok after Bridge_Mstp config(after {method} ')
    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in Port_QinQ_config config {data._asdict}'


def test_QinQ_registration_table_config(rest_interface_module, node_id):

    
    for bridge in Bridge_conf_s_c:
        bridge_config(rest_interface_module, node_id, bridge, method='POST')

        for vlan in VLAN_DATA_conf_service:
            vlan_config(rest_interface_module, node_id, vlan, method='POST')   
        for vlan in VLAN_DATA_conf_CUSTOM:
            vlan_config(rest_interface_module, node_id, vlan, method='POST')   


        # QinQ_registration_table_config(rest_interface_module, node_id, Reg_QinQ_Table_1_Data[0], method='ADD')    
        QinQ_registration_table_config(rest_interface_module, node_id, Reg_QinQ_Table_1_Data[1], method='ADD') 
        # QinQ_registration_table_config(rest_interface_module, node_id, Reg_QinQ_Table_1_Data[2], method='Post') 
        # QinQ_registration_table_config(rest_interface_module, node_id, Reg_QinQ_Table_1_Data[3], method='Post') 
        # QinQ_registration_table_config(rest_interface_module, node_id, Reg_QinQ_Table_1_Data[4], method='Post') 
        # QinQ_registration_table_config(rest_interface_module, node_id, Reg_QinQ_Table_1_Data[5], method='Post') 
        # QinQ_registration_table_config(rest_interface_module, node_id, Reg_QinQ_Table_1_Data[6], method='Post')
        # QinQ_registration_table_config(rest_interface_module, node_id, Reg_QinQ_Table_1_Data[7], method='Post')
        # QinQ_registration_table_config(rest_interface_module, node_id, Reg_QinQ_Table_1_Data[8], method='Post')


        # QinQ_registration_table_config(rest_interface_module, node_id, Reg_QinQ_Table_2_Data[0], method='ADD') 
        # QinQ_registration_table_config(rest_interface_module, node_id, Reg_QinQ_Table_2_Data[1], method='ADD') 
        # QinQ_registration_table_config(rest_interface_module, node_id, Reg_QinQ_Table_2_Data[2], method='Post') 
        # QinQ_registration_table_config(rest_interface_module, node_id, Reg_QinQ_Table_2_Data[3], method='Post') 
        # QinQ_registration_table_config(rest_interface_module, node_id, Reg_QinQ_Table_2_Data[4], method='Post') 
        # QinQ_registration_table_config(rest_interface_module, node_id, Reg_QinQ_Table_2_Data[5], method='Post') 
        # QinQ_registration_table_config(rest_interface_module, node_id, Reg_QinQ_Table_2_Data[6], method='Post') 
        # QinQ_registration_table_config(rest_interface_module, node_id, Reg_QinQ_Table_2_Data[7], method='Post') 
        # QinQ_registration_table_config(rest_interface_module, node_id, Reg_QinQ_Table_2_Data[8], method='Post') 

        # QinQ_registration_table_config(rest_interface_module, node_id, Reg_QinQ_Table(None, 1, "reg"), method='DELETE') 
        # QinQ_registration_table_config(rest_interface_module, node_id, Reg_QinQ_Table(None, 2, "reg2"), method='DELETE') 

        # for vlan in VLAN_DATA_conf_CUSTOM:
        #     vlan_config(rest_interface_module, node_id, vlan, method='DELETE')   
        # for vlan in VLAN_DATA_conf_service:
        #     vlan_config(rest_interface_module, node_id, vlan, method='DELETE')   
        # bridge_config(rest_interface_module, node_id, bridge, method='DELETE')    





    #**************************************************************************************************************




