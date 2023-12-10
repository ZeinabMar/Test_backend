import pytest
import logging
import json
from conftest import *
from config import *
from Switch.bridge_funcs import bridge_config
from Switch.test_QinQ_registration_table_conf import QinQ_registration_table_config
from Switch.test_Bridge_group_conf import switch_config
from Switch.test_vlan import vlan_config
from Switch.test_uplink_port_Vlan_conf import uplink_vlan_config
# from pytest-check import check


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


Port_QinQ = namedtuple('Port_QinQ', ['index' ,'ethIfIndex', 'qinQIfPvId', 'qinQRegistrationIfName',
                       'qinQIfTaggedVlan', 'qinQIfTaggedVlanSet', 'qinQIfTaggedVlanClr', 'qinQIfEgressTag',
                       'qinQIfMode', 'qinQIfTranslationSrcVlan', 'qinQIfTranslationSrcVlanSet',
                       'qinQIfTranslationSrcVlanClr', 'qinQIfTranslationDesVlan', 'qinQIfTranslationDesVlanSet',
                       'vlanMode', 'result', 'shelfId', 'slotId', 'nodeId'])
Port_QinQ.__new__.__defaults__ = (None, None, -1, "", "", "", "", -1, "STAGGED_SERVICE_INTERFACE", "", "", "", "", "", "", "Pass", 1, 1, None)


Port_QinQ_DATA_Registration_ACCESS = (
    # Port_QinQ(1, None, "10", "reg", "", "13", "", -1, "CTAGGED_SERVICE_INTERFACE", "", "", "", "", "", "", "Fail"),
    Port_QinQ(1, None, "13", "reg", "", "", "", -1, "CTAGGED_SERVICE_INTERFACE", "", "", "", "", "", "", "Fail"),
    Port_QinQ(2, None, "10", "reg", "", "", "", -1, "CTAGGED_SERVICE_INTERFACE", "", "", "", "", "", "", "Pass"),
    # Port_QinQ(3, None, "10", "reg", "", "", "", -1, "CTAGGED_SERVICE_INTERFACE", "", "20", "", "", "", "22", "Fail"),# //
    Port_QinQ(3, None, 10, "__NO__", "", "", "", -1, "CTAGGED_SERVICE_INTERFACE", "", "", "", "", "", "", "Pass"),
    Port_QinQ(4, None, -1, "", "", "", "", -1, "CTAGGED_SERVICE_INTERFACE", "", "", "", "", "", "", "Pass"),
)

Port_QinQ_DATA_Registration_TRUNK = (
    Port_QinQ(1, None, "10", "reg", "", "", "", -1, "CTAGGED_SERVICE_INTERFACE", "", "", "", "", "", "", "Fail"),
    Port_QinQ(2, None, -1, "reg", "", "10-13", "", -1, "CTAGGED_SERVICE_INTERFACE", "", "", "", "", "", "", "Pass"),
    # Port_QinQ(3, None, "13", "reg", "10-13", "", "", -1, "CTAGGED_SERVICE_INTERFACE", "", "", "", "", "", "", "Fail"), #not to be shown any failed
    # Port_QinQ(4, None, -1, "reg", "10-13", "", "", -1, "CTAGGED_SERVICE_INTERFACE", "", "15", "", "", "", "", "Fail"), #not to be shown any failed
    Port_QinQ(5, None, -1, "__NO__", "10-13", "", "", -1, "CTAGGED_SERVICE_INTERFACE", "", "", "", "", "", "", "Pass"),
    Port_QinQ(6, None, -1, "", "10-13", "", "10-13", -1, "CTAGGED_SERVICE_INTERFACE", "", "", "", "", "", "", "Pass"),
)

Port_QinQ_DATA_Registration_HYBRID = (
    # Port_QinQ(1, None, "13", "reg", "", "10-13", "", -1, "CTAGGED_SERVICE_INTERFACE", "", "", "", "", "", "", "Fail"),
    Port_QinQ(2, None, "13", "reg", "", "10-13", "", -1, "CTAGGED_SERVICE_INTERFACE", "", "", "", "", "", "", "Pass"),
    Port_QinQ(3, None, "13", "reg", "10-13", "14", "", -1, "CTAGGED_SERVICE_INTERFACE", "", "", "", "", "", "", "Pass"),
    # Port_QinQ(4, None, "13", "reg", "10-14", "", "", -1, "CTAGGED_SERVICE_INTERFACE", "", "15", "", "", "", "", "Fali"),
    Port_QinQ(5, None, "10-13", "reg", "10-14", "", "11", -1, "CTAGGED_SERVICE_INTERFACE", "", "", "", "", "", "", "Fail"),
    Port_QinQ(6, None, "13", "reg", "10-14", "", "14", -1, "CTAGGED_SERVICE_INTERFACE", "", "", "", "", "", "", "Pass"),
    Port_QinQ(7, None, "13", "__NO__", "10-13", "", "", -1, "CTAGGED_SERVICE_INTERFACE", "", "", "", "", "", "", "Pass"),
    Port_QinQ(8, None, -1, "", "10-13", "", "10-13", -1, "CTAGGED_SERVICE_INTERFACE", "", "", "", "", "", "", "Fail"),
    Port_QinQ(8, None, -1, "", "10-13", "", "10-13", -1, "CTAGGED_SERVICE_INTERFACE", "", "", "", "", "", "", "Fail"),
)


# Port_QinQ_DATA_Trans_Edge = (

# #     Port_QinQ(1, None, -1, "", "", "", "", -1, "STAGGED_SERVICE_INTERFACE", "", "15", "", "", "", "", "Fail"),
# #     Port_QinQ(2, None, -1, "", "", "", "", -1, "STAGGED_SERVICE_INTERFACE", "", "", "", "", "16", "", "Fail"),
# #     Port_QinQ(3, None, -1, "", "", "", "", -1, "STAGGED_SERVICE_INTERFACE", "", "10", "", "", "", "", "Fail"),
# # #***************************************************************************************************************************************
# #     Port_QinQ(4, None, -1, "", "", "15-16", "", -1, "STAGGED_SERVICE_INTERFACE", "", "", "", "", "", "", "Pass"),
# #     Port_QinQ(5, None, -1, "", "15-16", "10", "", -1, "STAGGED_SERVICE_INTERFACE", "", "", "", "", "", "", "Fail"),
#     # Port_QinQ(5, None, "10", "", "15-16", "", "", -1, "STAGGED_SERVICE_INTERFACE", "", "", "", "", "", "", "Fail"),
#     # Port_QinQ(5, None, -1, "reg", "15-16", "", "", -1, "STAGGED_SERVICE_INTERFACE", "", "", "", "", "", "", "Fail"),
# # #***************************************************************************************************************************************
# #     Port_QinQ(6, None, -1, "", "", "15-16", "", -1, "STAGGED_SERVICE_INTERFACE", "", "15", "", "", "", "", "Fail"),
# #     Port_QinQ(7, None, -1, "", "", "15-16", "", -1, "STAGGED_SERVICE_INTERFACE", "", "", "", "", "16", "", "Fail"),
# # #***************************************************************************************************************************************
# #     Port_QinQ(8, None, -1, "", "15-16", "", "", -1, "STAGGED_SERVICE_INTERFACE", "", "15", "", "", "16", "", "Pass"),
# #**************************************************************************************************************************************
#     # Port_QinQ(9, None, -1, "", "", "15-16", "", -1, "STAGGED_SERVICE_INTERFACE", "", "", "", "", "16", "", "Fail"),
#     # Port_QinQ(10, None, -1, "", "15-16", "", "15-16", -1, "STAGGED_SERVICE_INTERFACE", "15", "", "", "16", "", "", "Pass"),
#     Port_QinQ(11, None, -1, "", "", "15-16", "", -1, "STAGGED_SERVICE_INTERFACE", "15", "", "", "16", "", "", "Pass"),
# #***************************************************************************************************************************************
#     Port_QinQ(12, None, -1, "", "15-16", "17-23", "", -1, "STAGGED_SERVICE_INTERFACE", "15", "", "", "16", "", "", "Pass"),
#     Port_QinQ(13, None, -1, "", "15,16,17,18,19,20,21,22,23", "", "", -1, "STAGGED_SERVICE_INTERFACE", "15", "17,19", "", "16", "18,20", "", "Pass"),
#     Port_QinQ(14, None, -1, "", "15,16,17,18,19,20,21,22,23", "", "15-16", -1, "STAGGED_SERVICE_INTERFACE", "15,17,19", "", "", "16,18,20", "", "", "Pass"),
#     Port_QinQ(15, None, -1, "", "17,18,19,20,21,22,23", "", "", -1, "STAGGED_SERVICE_INTERFACE", "17,19", "21", "", "18,20", "16", "", "Fail"),
#     Port_QinQ(15, None, -1, "", "17,18,19,20,21,22,23", "", "", -1, "STAGGED_SERVICE_INTERFACE", "17,19", "21", "", "18,20", "22", "", "Pass"),
#     Port_QinQ(16, None, -1, "", "17,18,19,20,21,22,23", "", "", -1, "STAGGED_SERVICE_INTERFACE", "17,19,21", "23", "", "18,20,22", "21", "", "Pass"),
# #***************************************************************************************************************************************
#     Port_QinQ(17, None, -1, "", "17,18,19,20,21,22,23", "10", "", -1, "STAGGED_SERVICE_INTERFACE", "17,19,21,23", "", "", "18,20,22,21", "", "", "Fail"),
# #***************************************************************************************************************************************
#     Port_QinQ(18, None, -1, "", "17,18,19,20,21,22,23", "", "", -1, "STAGGED_SERVICE_INTERFACE", "17,19,21,23", "", "17,19,21,23", "18,20,22,21", "", "", "Pass"),
#     Port_QinQ(19, None, -1, "", "17,18,19,20,21,22,23", "", "17,18,19,20,21,22,23", -1, "STAGGED_SERVICE_INTERFACE", "", "", "", "", "", "", "Pass"),
# )

Port_QinQ_DATA_Trans = (

    Port_QinQ(1, None, -1, "", "", "", "", -1, "STAGGED_SERVICE_INTERFACE", "", "15", "", "", "", "", "Fail"),
    Port_QinQ(2, None, -1, "", "", "", "", -1, "STAGGED_SERVICE_INTERFACE", "", "", "", "", "16", "", "Fail"),
    Port_QinQ(3, None, -1, "", "", "", "", -1, "STAGGED_SERVICE_INTERFACE", "", "10", "", "", "", "", "Fail"),
# #***************************************************************************************************************************************
    Port_QinQ(4, None, -1, "", "", "15-16", "", -1, "STAGGED_SERVICE_INTERFACE", "", "", "", "", "", "", "Pass"),
# #***************************************************************************************************************************************
    Port_QinQ(6, None, -1, "", "", "15-16", "", -1, "STAGGED_SERVICE_INTERFACE", "", "15", "", "", "", "", "Fail"),
    Port_QinQ(7, None, -1, "", "", "15-16", "", -1, "STAGGED_SERVICE_INTERFACE", "", "", "", "", "16", "", "Fail"),
#***************************************************************************************************************************************
    Port_QinQ(8, None, -1, "", "15-16", "", "", -1, "STAGGED_SERVICE_INTERFACE", "", "15", "", "", "16", "", "Pass"),
#**************************************************************************************************************************************
    Port_QinQ(10, None, -1, "", "15-16", "", "15-16", -1, "STAGGED_SERVICE_INTERFACE", "15", "", "", "16", "", "", "Pass"),
    Port_QinQ(11, None, -1, "", "", "15-16", "", -1, "STAGGED_SERVICE_INTERFACE", "15", "", "", "16", "", "", "Pass"),
# #***************************************************************************************************************************************
    Port_QinQ(12, None, -1, "", "15-16", "17-23", "", -1, "STAGGED_SERVICE_INTERFACE", "15", "", "", "16", "", "", "Pass"),
    Port_QinQ(13, None, -1, "", "15,16,17,18,19,20,21,22,23", "", "", -1, "STAGGED_SERVICE_INTERFACE", "15", "17,19", "", "16", "18,20", "", "Pass"),#error
    Port_QinQ(15, None, -1, "", "15,16,17,18,19,20,21,22,23", "", "", -1, "STAGGED_SERVICE_INTERFACE", "15,17,19", "21", "", "16,18,20", "16", "", "Fail"),
    Port_QinQ(16, None, -1, "", "15,16,17,18,19,20,21,22,23", "", "", -1, "STAGGED_SERVICE_INTERFACE", "15,17,19", "22", "", "16,18,20", "19", "", "Pass"),#error
# #***************************************************************************************************************************************
# #***************************************************************************************************************************************
    Port_QinQ(17, None, -1, "", "15,16,17,18,19,20,21,22,23", "", "", -1, "STAGGED_SERVICE_INTERFACE", "15,17,19,22", "", "15,17,19,22", "16,18,20,19", "", "", "Pass"),
    Port_QinQ(18, None, -1, "", "15,16,17,18,19,20,21,22,23", "", "15,16,17,18,19,20,21,22,23", -1, "STAGGED_SERVICE_INTERFACE", "", "", "", "", "", "", "Pass"),
)

up_link_mode_teory_1 = ("CUSTOMER_NETWORK","PROVIDER_NETWORK")
up_link_mode_teory_2 = ("CUSTOMER_EDGE_HYBRID","CUSTOMER_EDGE_TRUNK", "CUSTOMER_EDGE_ACCESS") 

def Port_QinQ_config(rest_interface_module, node_id, Port_QinQ_data=Port_QinQ(), method='POST', theory_number=1):
    data = Port_QinQ_data._replace(nodeId=node_id)

    read_data_previous = rest_interface_module.get_request(f"/api/gponconfig/sp5100/portqinqconfig/get/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.ethIfIndex}")
    previous_output_data = json.loads(read_data_previous.text)

    logger.info(f"TRY TO {method} Port_Qos_Policy CONFIG ...")
    if method == 'POST':  
        url = "/api/gponconfig/sp5100/portqinqconfig/update"
        response = rest_interface_module.post_request(url, data._asdict()) 

    if data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in Port_QinQ_Port config {data._asdict}'
        if response.status_code != 200:
            logger.error(response.message)
        logger.info(f' GETTING Port_QinQ_config (after {method} method) ... ')
        read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/portqinqconfig/get/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.ethIfIndex}")
        input_data = json.loads(read_data.text)
        logger.info(f'data after read input_data {input_data}')
        #*********************************************************
        if method == 'POST': 
            if theory_number == 1:
                if len(data.qinQIfTaggedVlanSet)!=0 :
                    counter1 = 0
                    st1 = set_and_clear_data(str(data.qinQIfTaggedVlanSet))
                    for item in st1:
                        if set_and_clear_data(str(input_data["qinQIfTaggedVlan"])).find(item) != -1:
                            counter1 = counter1 +1
                    assert (input_data["ethIfIndex"] == data.ethIfIndex and
                            input_data["qinQIfPvId"] == -1 and 
                            counter1 == len(st1) and 
                            len(input_data["qinQIfTranslationSrcVlanSet"]) == 0 and
                            len(input_data["qinQIfTranslationDesVlanSet"]) == 0 and
                            input_data["vlanMode"] == data.vlanMode and
                            input_data["qinQIfMode"] == data.qinQIfMode),f'IN Everythig is ok Bridge_Mstp config(after {method} with clear action'
                
                elif len(data.qinQIfTranslationSrcVlanSet)!=0 and len(data.qinQIfTranslationDesVlanSet)!=0:
                    counter1 = 0
                    counter2 = 0
                    counter3 = 0 
                    st1 = set_and_clear_data(str(data.qinQIfTranslationDesVlanSet))
                    for item in st1:
                        if set_and_clear_data(str(input_data["qinQIfTranslationDesVlan"])).find(item) != -1:
                            counter1 = counter1 +1
                    st2 = set_and_clear_data(str(data.qinQIfTranslationSrcVlanSet))
                    for item in st2:
                        if set_and_clear_data(str(input_data["qinQIfTranslationSrcVlan"])).find(item) != -1:
                            counter2 = counter2+1
                    assert (input_data["ethIfIndex"] == data.ethIfIndex and
                            input_data["qinQIfPvId"] == -1 and 
                            input_data["vlanMode"] == data.vlanMode and
                            input_data["qinQIfMode"] == data.qinQIfMode and
                            counter1 == len(st1) and
                            counter2 == len(st2) and
                            len(input_data["qinQIfTranslationSrcVlanClr"]) == 0),f'IN Everythig is ok Bridge_Mstp config(after {method} with set action'
                
                elif len(data.qinQIfTranslationSrcVlanClr)!= 0 :
                    st1 = set_and_clear_data(str(data.qinQIfTranslationSrcVlanClr))
                    st1 = re.findall('\d+', st1)
                    st2 = set_and_clear_data(str(input_data["qinQIfTranslationSrcVlan"]))
                    st2 = re.findall('\d+', st2)

                    for item in st1:
                        assert not(item in st2)
                    assert (input_data["ethIfIndex"] == data.ethIfIndex and
                            input_data["qinQIfPvId"] == -1 and 
                            input_data["vlanMode"] == data.vlanMode and
                            input_data["qinQIfMode"] == data.qinQIfMode and
                            len(input_data["qinQIfTaggedVlanClr"]) == 0),f'IN Everythig is ok Bridge_Mstp config(after {method} with set action'
                
                elif len(data.qinQIfTaggedVlanClr)!= 0 :
                    st1 = set_and_clear_data(str(data.qinQIfTaggedVlanClr))
                    st1 = re.findall('\d+', st1)
                    st2 = set_and_clear_data(str(input_data["qinQIfTaggedVlan"]))
                    st2 = re.findall('\d+', st2)
                    # for item in st1:
                    #     if set_and_clear_data(str(data.qinQIfTranslationSrcVlan)).find(item) == -1:
                    #         counter1 = counter1 +1
                    # for item in st1:
                    #     if set_and_clear_data(str(data.qinQIfTranslationDesVlan)).find(item) == -1:
                    #         counter2 = counter2 +1
                    # for item in st1:
                    #     if set_and_clear_data(str(input_data["qinQIfTranslationSrcVlan"])).find(item) == -1:
                    #         counter3 = counter3 +1        
                    for item in st1:
                        assert not(item in st2)
                    assert (input_data["ethIfIndex"] == data.ethIfIndex and
                            input_data["qinQIfPvId"] == -1 and 
                            input_data["vlanMode"] == data.vlanMode and
                            input_data["qinQIfMode"] == data.qinQIfMode ),f'IN Everythig is ok Bridge_Mstp config(after {method} with set action'

                logger.info(f'every thing ok after Bridge_Mstp config(after {method} ')

            elif theory_number == 2:

                if data.vlanMode == "CUSTOMER_EDGE_ACCESS":
                    # st1 = set_and_clear_data(str(data.qinQIfPvId))
                    # st1 = re.findall('\d+', st1)
                    # st2 = set_and_clear_data(str(input_data["qinQIfPvId"]))
                    # st2 = re.findall('\d+', st2)
                    # for i in range(len(st1)):
                    #     assert st1[i] in st2

                    assert (input_data["ethIfIndex"] == data.ethIfIndex and
                            input_data["vlanMode"] == data.vlanMode and
                            len(str(input_data["qinQIfTaggedVlanSet"])) == 0 and
                            len(str(input_data["qinQIfTaggedVlan"])) == 0 and
                            # input_data["qinQIfMode"] == data.qinQIfMode and
                            len(str(input_data["qinQIfTaggedVlanClr"])) == 0 and
                            len(str(input_data["qinQIfTranslationSrcVlanSet"])) == 0 and 
                            len(str(input_data["qinQIfTranslationSrcVlanClr"])) == 0 and 
                            len(str(input_data["qinQIfTranslationSrcVlan"])) == 0 and 
                            len(str(input_data["qinQIfTranslationDesVlanSet"])) == 0 and 
                            len(str(input_data["qinQIfTranslationDesVlan"])) == 0),f'IN Everythig is ok Bridge_Mstp config(after {method}'

                elif data.vlanMode == "CUSTOMER_EDGE_TRUNK":
                    if len(data.qinQIfTaggedVlanSet)!=0:
                         st1 = set_and_clear_data(str(data.qinQIfTaggedVlanSet))
                         st1 = re.findall('\d+', st1)
                         st2 = set_and_clear_data(str(input_data["qinQIfTaggedVlan"]))
                         st2 = re.findall('\d+', st2)
                         for i in range(len(st1)):
                            assert st1[i] in st2
                         assert (input_data["qinQIfPvId"] == -1 and
                                input_data["vlanMode"] == data.vlanMode and 
                                input_data["qinQIfMode"] == data.qinQIfMode and 
                                len(str(input_data["qinQIfTranslationSrcVlanSet"])) == 0 and 
                                len(str(input_data["qinQIfTranslationSrcVlanClr"])) == 0 and 
                                len(str(input_data["qinQIfTranslationSrcVlan"])) == 0 and
                                len(str(input_data["qinQIfTranslationDesVlanSet"])) == 0 and 
                                len(str(input_data["qinQIfTranslationDesVlan"])) == 0),f'IN Everythig is ok Reg_QinQ_Table(after {method} with clear action'
                    
                    if len(data.qinQIfTaggedVlanClr)!=0:
                        counter1 = 0 
                        st_clr = set_and_clear_data(str(data.qinQIfTaggedVlanClr))
                        st_clr = re.findall('\d+', st_clr)
                        for item in st_clr:
                            if set_and_clear_data(str(input_data["qinQIfTaggedVlanClr"])).find(item) == -1:
                                counter1 = counter1 +1  
                        assert (input_data["qinQIfPvId"] == -1 and
                                input_data["vlanMode"] == data.vlanMode and 
                                input_data["qinQIfMode"] == data.qinQIfMode and 
                                counter1 == len(st_clr) and
                                len(str(input_data["qinQIfTaggedVlanSet"])) == 0 and 
                                len(str(input_data["qinQIfTranslationSrcVlanSet"])) == 0 and 
                                len(str(input_data["qinQIfTranslationSrcVlanClr"])) == 0 and 
                                len(str(input_data["qinQIfTranslationSrcVlan"])) == 0 and 
                                len(str(input_data["qinQIfTranslationDesVlanSet"])) == 0 and 
                                len(str(input_data["qinQIfTranslationDesVlan"])) == 0),f'IN Everythig is ok Reg_QinQ_Table(after {method} with clear action'        

                elif data.vlanMode == "CUSTOMER_EDGE_HYBRID":
                    if len(data.qinQIfTaggedVlanSet)!=0:
                        st1 = set_and_clear_data(str(data.qinQIfTaggedVlanSet))
                        st1 = re.findall('\d+', st1)
                        st2 = set_and_clear_data(str(input_data["qinQIfTaggedVlan"]))
                        st2 = re.findall('\d+', st2)
                        for i in range(len(st1)):
                            assert st1[i] in st2
                        assert (input_data["vlanMode"] == data.vlanMode and 
                            input_data["qinQIfMode"] == data.qinQIfMode and 
                            len(str(input_data["qinQIfTranslationSrcVlanSet"])) == 0 and 
                            len(str(input_data["qinQIfTranslationSrcVlanClr"])) == 0 and 
                            len(str(input_data["qinQIfTranslationSrcVlan"])) == 0 and 
                            len(str(input_data["qinQIfTranslationDesVlanSet"])) == 0 and 
                            len(str(input_data["qinQIfTranslationDesVlan"])) == 0),f'IN Everythig is ok Reg_QinQ_Table(after {method} with clear action'
                    if  data.qinQIfPvId == -1 :
                            assert  input_data["qinQIfPvId"] == -1
                    else :
                        st1 = set_and_clear_data(str(data.qinQIfPvId))
                        st1 = re.findall('\d+', st1)
                        st2 = set_and_clear_data(str(input_data["qinQIfPvId"]))
                        st2 = re.findall('\d+', st2)
                        for i in range(len(st1)):
                            assert st1[i] in st2

                    if len(data.qinQIfTaggedVlanClr)!=0:
                        counter1 = 0 
                        st_clr = set_and_clear_data(str(data.qinQIfTaggedVlanClr))
                        st_clr = re.findall('\d+', st_clr)
                        for item in st_clr:
                            if set_and_clear_data(str(input_data["qinQIfTaggedVlanClr"])).find(item) == -1:
                                counter1 = counter1 +1  
                        assert (input_data["vlanMode"] == data.vlanMode and 
                                input_data["qinQIfMode"] == data.qinQIfMode and 
                                counter1 == len(st_clr) and
                                len(str(input_data["qinQIfTaggedVlanSet"])) == 0 and 
                                len(str(input_data["qinQIfTranslationSrcVlanSet"])) == 0 and 
                                len(str(input_data["qinQIfTranslationSrcVlanClr"])) == 0 and 
                                len(str(input_data["qinQIfTranslationSrcVlan"])) == 0 and 
                                len(str(input_data["qinQIfTranslationDesVlanSet"])) == 0 and 
                                len(str(input_data["qinQIfTranslationDesVlan"])) == 0),f'IN Everythig is ok Reg_QinQ_Table(after {method} with clear action'        
    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in Port_QinQ_config config {data._asdict}'


def test_Port_QinQ_config(rest_interface_module, node_id):
    theory=1

    #theory1 Translation
    if theory==1:
        for bridge in Bridge_conf_service:
            response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/bridgeconfig/getall?nodeId=11&shelfId=1&slotId=1")
            bridge_config(rest_interface_module, node_id, bridge, method='POST')

            response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/vlan/getall?nodeId=11&shelfId=1&slotId=1")
            for vlan in VLAN_DATA_conf_service:
                vlan_config(rest_interface_module, node_id, vlan, method='POST')   
            if bridge.bridgeProtocol == "PROVIDER_MSTP_EDGE" or bridge.bridgeProtocol == "PROVIDER_RSTP_EDGE":
                response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/vlan/getall?nodeId=11&shelfId=1&slotId=1")
                for vlan in VLAN_DATA_conf_CUSTOM:
                    vlan_config(rest_interface_module, node_id, vlan, method='POST')   

            for uplinkmode in up_link_mode_teory_1:   
                for port_bridge_group in range(2,3):
                    response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/bridgegroupconfig/getall?nodeId=11&shelfId=1&slotId=1")
                    switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port_bridge_group,index=4), method='POST') 
                    if uplinkmode == "CUSTOMER_NETWORK":
                        response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/portvlan/getall?nodeId=11&shelfId=1&slotId=1")
                        uplink_vlan_config(rest_interface_module, node_id, uplink_vlan_conf(port_bridge_group, None, "CUSTOMER_NETWORK", -1, "" , "", "", -1, "Pass"), method='POST')
                        if bridge.bridgeProtocol == "PROVIDER_MSTP_EDGE" or bridge.bridgeProtocol == "PROVIDER_RSTP_EDGE":
                            for qinq in Port_QinQ_DATA_Trans_Edge:
                                response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/portqinqconfig/getall?nodeId=11&shelfId=1&slotId=1")
                                Port_QinQ_config(rest_interface_module, node_id, qinq._replace(ethIfIndex=port_bridge_group, vlanMode="CUSTOMER_NETWORK"), method='POST', theory_number=1)
                        else:
                            for qinq in Port_QinQ_DATA_Trans:
                                response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/portqinqconfig/getall?nodeId=11&shelfId=1&slotId=1")
                                Port_QinQ_config(rest_interface_module, node_id, qinq._replace(ethIfIndex=port_bridge_group, vlanMode="CUSTOMER_NETWORK"), method='POST', theory_number=1)

                    if uplinkmode == "PROVIDER_NETWORK":
                        response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/portvlan/getall?nodeId=11&shelfId=1&slotId=1")
                        uplink_vlan_config(rest_interface_module, node_id, uplink_vlan_conf(port_bridge_group, None, "PROVIDER_NETWORK", -1, "" , "", "", -1, "Pass"), method='POST')
                        if bridge.bridgeProtocol == "PROVIDER_MSTP_EDGE" or bridge.bridgeProtocol == "PROVIDER_RSTP_EDGE":
                            for qinq in Port_QinQ_DATA_Trans_Edge:
                                response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/portqinqconfig/getall?nodeId=11&shelfId=1&slotId=1")
                                Port_QinQ_config(rest_interface_module, node_id, qinq._replace(ethIfIndex=port_bridge_group, vlanMode="PROVIDER_NETWORK"), method='POST', theory_number=1)
                        else:
                            for qinq in Port_QinQ_DATA_Trans:
                                response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/portqinqconfig/getall?nodeId=11&shelfId=1&slotId=1")
                                Port_QinQ_config(rest_interface_module, node_id, qinq._replace(ethIfIndex=port_bridge_group, vlanMode="PROVIDER_NETWORK"), method='POST', theory_number=1)
                    response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/bridgegroupconfig/getall?nodeId=11&shelfId=1&slotId=1")
                    switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port_bridge_group,index=9), method='DELETE')  

            response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/bridgegroupconfig/getall?nodeId=11&shelfId=1&slotId=1")
            for vlan in VLAN_DATA_conf_CUSTOM:
                vlan_config(rest_interface_module, node_id, vlan, method='DELETE')   
            for vlan in VLAN_DATA_conf_service:
                vlan_config(rest_interface_module, node_id, vlan, method='DELETE')   
            bridge_config(rest_interface_module, node_id, bridge(), method='DELETE')    
    theory = 2
    #theory2 Registration                    
    if theory==2:
        for bridge in Bridge_conf_s_c:
            response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/bridgeconfig/getall?nodeId=11&shelfId=1&slotId=1")
            bridge_config(rest_interface_module, node_id, bridge, method='POST')
            response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/vlan/getall?nodeId=11&shelfId=1&slotId=1")
            for vlan in VLAN_DATA_conf_service:
                vlan_config(rest_interface_module, node_id, vlan, method='POST')   
            response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/vlan/getall?nodeId=11&shelfId=1&slotId=1")
            for vlan in VLAN_DATA_conf_CUSTOM:
                vlan_config(rest_interface_module, node_id, vlan, method='POST')   
            for uplinkmode in up_link_mode_teory_2:  
                if uplinkmode ==  "CUSTOMER_EDGE_ACCESS":
                    response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/qinqregistration/getall?nodeId=11&shelfId=1&slotId=1")     
                    QinQ_registration_table_config(rest_interface_module, node_id, Reg_QinQ_Table_conf_DATA[1], method='ADD') 
                else :
                    response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/qinqregistration/getall?nodeId=11&shelfId=1&slotId=1")     
                    QinQ_registration_table_config(rest_interface_module, node_id, Reg_QinQ_Table_conf_DATA[0], method='ADD')  

                for port_bridge_group in range(1,2):
                    response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/bridgegroupconfig/getall?nodeId=17&shelfId=1&slotId=1")
                    switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port_bridge_group,index=4), method='POST') 
                    if uplinkmode == "CUSTOMER_EDGE_ACCESS":
                        response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/portvlan/getall?nodeId=17&shelfId=1&slotId=1")
                        uplink_vlan_config(rest_interface_module, node_id, uplink_vlan_conf(port_bridge_group, None, "CUSTOMER_EDGE_ACCESS", -1, "" , "", "", -1, "Pass"), method='POST')
                        for qinq in Port_QinQ_DATA_Registration_ACCESS:
                            response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/portqinqconfig/getall?nodeId=11&shelfId=1&slotId=1")
                            Port_QinQ_config(rest_interface_module, node_id, qinq._replace(ethIfIndex=port_bridge_group, vlanMode="CUSTOMER_EDGE_ACCESS"), method='POST', theory_number=2)

                    elif uplinkmode == "CUSTOMER_EDGE_TRUNK":
                        response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/portvlan/getall?nodeId=17&shelfId=1&slotId=1")
                        uplink_vlan_config(rest_interface_module, node_id, uplink_vlan_conf(port_bridge_group, None, "CUSTOMER_EDGE_TRUNK", -1, "" , "", "", -1, "Pass"), method='POST')
                        for qinq in Port_QinQ_DATA_Registration_TRUNK:
                            response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/portqinqconfig/getall?nodeId=11&shelfId=1&slotId=1")
                            Port_QinQ_config(rest_interface_module, node_id, qinq._replace(ethIfIndex=port_bridge_group, vlanMode="CUSTOMER_EDGE_TRUNK"), method='POST', theory_number=2)

                    elif uplinkmode == "CUSTOMER_EDGE_HYBRID":
                        response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/portvlan/getall?nodeId=17&shelfId=1&slotId=1")
                        uplink_vlan_config(rest_interface_module, node_id, uplink_vlan_conf(port_bridge_group, None, "CUSTOMER_EDGE_HYBRID", -1, "" , "", "", -1, "Pass"), method='POST')
                        for qinq in Port_QinQ_DATA_Registration_HYBRID:
                            response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/portqinqconfig/getall?nodeId=11&shelfId=1&slotId=1")
                            Port_QinQ_config(rest_interface_module, node_id, qinq._replace(ethIfIndex=port_bridge_group, vlanMode="CUSTOMER_EDGE_HYBRID"), method='POST', theory_number=2)

                    elif uplinkmode == "PROVIDER_NETWORK":
                        response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/portvlan/getall?nodeId=17&shelfId=1&slotId=1")
                        uplink_vlan_config(rest_interface_module, node_id, uplink_vlan_conf(port_bridge_group, None, "PROVIDER_NETWORK", -1, "" , "", "", -1, "Pass"), method='POST')
                        response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/portqinqconfig/getall?nodeId=11&shelfId=1&slotId=1")
                        Port_QinQ_config(rest_interface_module, node_id, Port_QinQ(3, port_bridge_group, -1, "", "", "15-16", "", -1, "PROVIDER_NETWORK", "", "", "", "", "", "", "Fail"), method='POST', theory_number=2)

                    
                    response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/bridgegroupconfig/getall?nodeId=17&shelfId=1&slotId=1")
                    switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port_bridge_group,index=9), method='DELETE') 
                    response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/qinqregistration/getall?nodeId=11&shelfId=1&slotId=1")     
                    QinQ_registration_table_config(rest_interface_module, node_id, Reg_QinQ_Table_conf(None, 1, "reg"), method='DELETE') 

            response = getall_and_update_condition(rest_interface_module,"/api/gponconfig/sp5100/vlan/getall?nodeId=11&shelfId=1&slotId=1")
            for vlan in VLAN_DATA_conf_CUSTOM:
                vlan_config(rest_interface_module, node_id, vlan, method='DELETE')   
            for vlan in VLAN_DATA_conf_service:
                vlan_config(rest_interface_module, node_id, vlan, method='DELETE')   
            bridge_config(rest_interface_module, node_id, bridge, method='DELETE')        

    #**************************************************************************************************************




