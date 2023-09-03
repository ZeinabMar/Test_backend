import pytest
import logging
import json
from config import *
from Switch.bridge_funcs import bridge_config
from Switch.test_vlan import vlan_config
from Switch.test_Bridge_group_conf import switch_config
# from pytest-check import check


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


uplink_vlan = namedtuple('uplink_vlan', ['ethIfIndex', 'index', 'vlanMode', 'pvId', 'taggedVlan', 
                    'taggedVlanClr', 'taggedVlanSet', 'untaggedVlan', 'result', 
                    'shelfId', 'slotId', 'nodeId'])
uplink_vlan.__new__.__defaults__ = (None, None, "ACCESS",  -1, "" , "", "", -1, "Pass", 1, 1, None)
uplink_vlan_DATA = (
    uplink_vlan(None, 1, "ACCESS", 10),
    uplink_vlan(None, 2, "TRUNK", -1, "", "", "10"),
    uplink_vlan(None, 3, "TRUNK", -1, "10-12", "10"),
    uplink_vlan(None, 4, "HYBRID", 10, "", "", "10-12"),
    uplink_vlan(None, 5, "HYBRID", 10, "10-12", "10"),
    uplink_vlan(None, 6, "ACCESS", -1, "10-12", "10", "10-12", -1, "Fail"),
    uplink_vlan(None, 7, "TRUNK", 11, "10-12", "10", "10-12", -1, "Fail"),
    uplink_vlan(None, 8, "HYBRID", 12, "", "10", "10-12", -1, "Fail")
    )

def uplink_vlan_config(rest_interface_module, node_id, UPLINK_VLAN_data=uplink_vlan(), method='POST'):
    data = UPLINK_VLAN_data._replace(nodeId=node_id)
    logger.info(f"TRY TO {method} UPLINK_VLAN CONFIG ...")
    if method == 'POST':
        url = "/api/gponconfig/sp5100/portvlan/update"
        response = rest_interface_module.post_request(url, data._asdict())
    else:  # method==DELETE
        logger.info(f'hoooo {data}')
        data = data._replace(nodeId=node_id,pvId=-1,taggedVlanClr=data.taggedVlanSet)
        data = data._replace(taggedVlanSet="")
        logger.info(f'hiiiiii {data}')
        url = "/api/gponconfig/sp5100/portvlan/update"
        response = rest_interface_module.post_request(url, data._asdict())

        
    if data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in UPLINK_VLAN config {data._asdict}'
        if response.status_code != 200:
            logger.error(response.message)
        logger.info(f' GETTING UPLINK_VLAN-config (after {method} method) ... ')
        read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/portvlan/get/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.ethIfIndex}")
        input_data = json.loads(read_data.text)

        if method == 'POST':
            if(data.vlanMode=="ACCESS"):
                assert (str(input_data["ethIfIndex"]) == str(data.ethIfIndex) and
                        str(input_data["vlanMode"])=="ACCESS" and 
                        str(input_data["pvId"]) == str(data.pvId),
                        f'IN {data.ethIfIndex} exist ERROR FOR UPLINK_VLAN config(after {method}')
                logger.info(f'{data.ethIfIndex} every thing ok after UPLINK_VLAN in ACCESS VLAN MODE config(after {method} ')

            if(data.vlanMode=="TRUNK"):
                if data.index == 2:
                    assert (str(input_data["ethIfIndex"]) == str(data.ethIfIndex) and 
                            str(input_data["taggedVlan"]) == str(data.taggedVlanSet)
                            ,f'IN {data.ethIfIndex} exist ERROR FOR UPLINK_VLAN config(after {method}')
                if data.index == 3:            
                    assert (str(input_data["ethIfIndex"]) == str(data.ethIfIndex) and 
                            str(input_data["taggedVlan"]).find(str(data.taggedVlanClr)) == -1
                            ,f'IN {data.ethIfIndex} exist ERROR FOR UPLINK_VLAN config(after {method}')

            if(data.vlanMode=="HYBRID"):
                if data.index == 4:
                    assert (str(input_data["ethIfIndex"]) == str(data.ethIfIndex) and
                    str(input_data["pvId"]) == str(data.pvId) and
                    str(input_data["taggedVlan"]) == str(data.taggedVlanSet) and
                    str(input_data["taggedVlanClr"]) == str(data.taggedVlanClr) and
                    str(input_data["taggedVlanSet"]) == "" ,
                    f'IN {data.ethIfIndex} exist ERROR FOR UPLINK_VLAN config(after {method}')
                if data.index == 5:
                    assert (str(input_data["ethIfIndex"]) == str(data.ethIfIndex) and
                    str(input_data["pvId"]) == str(data.pvId) and
                    str(input_data["taggedVlanSet"]) == "" and
                    str(input_data["taggedVlan"]).find(str(data.taggedVlanClr)) == -1
                    ,f'IN {data.ethIfIndex} exist ERROR FOR UPLINK_VLAN config(after {method}')
                    
        else:  # method==DELETE
            # check.equal(str(input_data[0]["ethIfIndex"]) ,None ,f'IN {data.ethIfIndex} Everythig is ok switch config(after {method}')
            assert ( input_data["pvId"] == -1 and
                    str(input_data["taggedVlan"]) == "" and
                    str(input_data["taggedVlanClr"]) == "" and
                    str(input_data["taggedVlanSet"]) == ""
                    ,f'GET ERROR in UPLINK_VLAN config (after {method})')
    else:
        assert response.status_code in range(400, 505), f'{method} ERROR in UPLINK_VLAN config {data._asdict}'



def test_uplink_vlan_config(rest_interface_module, node_id):
    bridge_config(rest_interface_module, node_id, Bridge_conf(), method='POST')
    # ****************************************************************************************************************************
    for vlan in VLAN_DATA_conf_CUSTOM:
        vlan_config(rest_interface_module, node_id, vlan, method='POST')  
    #**********************************************************************************************************************
    for port in range(4,5):
        switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port, index=4), method='POST')
        for up_vlan in uplink_vlan_DATA:
            if up_vlan.index == 1:
                uplink_vlan_config(rest_interface_module, node_id, up_vlan._replace(ethIfIndex=port), method='POST') 
                uplink_vlan_config(rest_interface_module, node_id, up_vlan._replace(ethIfIndex=port), method='DELETE')   
                switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port, index=9), method='DELETE')
                switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port, index=4), method='POST')
            elif up_vlan.index == 2 or 3:
                uplink_vlan_config(rest_interface_module, node_id, up_vlan._replace(ethIfIndex=port), method='POST') 
                if up_vlan.index == 3:
                    uplink_vlan_config(rest_interface_module, node_id, up_vlan._replace(ethIfIndex=port), method='DELETE')   
                    switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port, index=9), method='DELETE')
                    switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port, index=4), method='POST')
            elif up_vlan.index == 4 or 5:
                uplink_vlan_config(rest_interface_module, node_id, up_vlan._replace(ethIfIndex=port), method='POST') 
                if up_vlan.index == 5:
                    uplink_vlan_config(rest_interface_module, node_id, up_vlan._replace(ethIfIndex=port), method='DELETE')   
                    switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port, index=9), method='DELETE')
                    switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port, index=4), method='POST')
            else:
                uplink_vlan_config(rest_interface_module, node_id, up_vlan._replace(ethIfIndex=port), method='POST') 
                uplink_vlan_config(rest_interface_module, node_id, up_vlan._replace(ethIfIndex=port), method='DELETE')  
                switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port, index=9), method='DELETE')
                switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port, index=4), method='POST')
            
    switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port,index=9), method='POST')
    #*********************************************************************************************************************  
    for vlan in VLAN_DATA_conf_CUSTOM:
        vlan_config(rest_interface_module, node_id, vlan, method='DELETE')
    #****************************************************************************************************************************
    bridge_config(rest_interface_module, node_id, Bridge_conf(), method='DELETE')
         



