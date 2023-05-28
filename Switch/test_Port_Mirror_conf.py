import pytest
import logging
import json
from config import *
from Switch.bridge_funcs import bridge_config
from Switch.test_Bridge_group_conf import switch_config
# from pytest-check import check


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("nms")]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

Port_Mirror = namedtuple('Port_Mirror', ["index" ,'ethIfIndex', 'mirrorDirection','phyIfMirrorBoth',
                         'phyIfMirrorRx', 'phyIfMirrorTx', 'result','shelfId', 'slotId', 'nodeId'])
Port_Mirror.__new__.__defaults__ = (None, None, -1, -1, -1, "Pass", 1, 1, None)

Port_Mirror_DATA = [
    Port_Mirror(1, 2, )
]



def Port_Mirror_config(rest_interface_module, node_id, Port_Mirror_data=Port_Mirror(), method='POST'):
    data = Port_Mirror_data._replace(nodeId=node_id)
    logger.info(f"TRY TO {method} Port_Mirror CONFIG ...")

    if data.ethIfIndex != -1 and data.ethIfIndex != data.phyIfMirrorBoth and data.ethIfIndex != data.phyIfMirrorRx and data.ethIfIndex != data.phyIfMirrorTx:
        if method == 'POST' or method == 'DELETE':  
            url = "/api/gponconfig/sp5100/portmirrorconfig/update"
            response = rest_interface_module.post_request(url, data._asdict()) 

        if data.result == "Pass":
            assert response.status_code == 200, f'{method} ERROR in Port_Mirror config {data._asdict}'
            if response.status_code != 200:
                logger.error(response.message)
            logger.info(f' GETTING Port_Mirror-config (after {method} method) ... ')

            read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/portmirrorconfig/get/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.ethIfIndex}")
            input_data = json.loads(read_data.text)
            logger.info(f'data after read input_data {input_data}')
            #*********************************************************
            if method == 'POST':
                assert (input_data["phyIfMirrorBoth"]== data.phyIfMirrorBoth and
                        input_data["phyIfMirrorRx"] == data.phyIfMirrorRx and 
                        input_data["phyIfMirrorTx"] == data.phyIfMirrorTx),f'IN Everythig is ok Port_Mirror config(after {method}'
                logger.info(f'every thing ok after Port_Mirror config(after {method} ')

            else:  # method==DELETE
                assert (input_data["phyIfMirrorBoth"]== -1 and
                        input_data["phyIfMirrorRx"] == -1 and 
                        input_data["phyIfMirrorTx"] == -1),f'GET ERROR in Port_Mirror config (after {method})'
        else:
            assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in Port_Mirror config {data._asdict}'


def test_Port_Mirror_config(rest_interface_module, node_id):

    # bridge_config(rest_interface_module, node_id, Bridge_conf(1, 'PROVIDER_MSTP_EDGE', 100, 30, maxAge=6, maxHops=1, priority=12288), method='POST')
    for dest in range(1,7):
        if dest!=24:
            i=1
        else: 
            i=-1    
        if dest<=19:
            j=1
        else:
            j=-1    
        Port_Mirror_config(rest_interface_module, node_id, Port_Mirror(1, dest, dest+i, -1, -1, "Pass"), method='POST')
        Port_Mirror_config(rest_interface_module, node_id, Port_Mirror(2, dest, -1, dest+i, -1, "Pass"), method='POST')
        Port_Mirror_config(rest_interface_module, node_id, Port_Mirror(3, dest, -1, -1, dest+i, "Pass"), method='POST')
        Port_Mirror_config(rest_interface_module, node_id, Port_Mirror(5, dest, -1, -1, -1, "Pass"), method='POST')
        
        Port_Mirror_config(rest_interface_module, node_id, Port_Mirror(4, dest, -1, dest+(2*i), dest+i, "Pass"), method='POST')
        Port_Mirror_config(rest_interface_module, node_id, Port_Mirror(5, dest, -1, -1, -1, "Pass"), method='POST')

        Port_Mirror_config(rest_interface_module, node_id, Port_Mirror(6, dest, dest+i, -1, -1, "Pass"), method='POST')
        Port_Mirror_config(rest_interface_module, node_id, Port_Mirror(7, dest+(3*j), -1, dest+i, -1, "Pass"), method='POST')
        Port_Mirror_config(rest_interface_module, node_id, Port_Mirror(8, dest+(4*j), -1, -1, dest+i, "Pass"), method='POST')
        Port_Mirror_config(rest_interface_module, node_id, Port_Mirror(9, dest, -1, -1, -1, "Pass"), method='POST')

        if dest<=22:
            i=1
        else: 
            i=-1      
        Port_Mirror_config(rest_interface_module, node_id, Port_Mirror(10, dest, dest+i, dest+(2*i), -1, "Fail"), method='POST')
        Port_Mirror_config(rest_interface_module, node_id, Port_Mirror(11, dest, dest+(2*i), -1, dest+i, "Fail"), method='POST') 
        
        for port_bridge_group in range(1,7):
            switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port_bridge_group,index=4), method='POST')
            if dest!=port_bridge_group:
                Port_Mirror_config(rest_interface_module, node_id, Port_Mirror(12, dest, -1, -1, port_bridge_group, "Fail"), method='POST')
                Port_Mirror_config(rest_interface_module, node_id, Port_Mirror(13, dest, -1, port_bridge_group, -1, "Fail"), method='POST')
                Port_Mirror_config(rest_interface_module, node_id, Port_Mirror(14, dest, port_bridge_group, -1, -1, "Fail"), method='POST')
            
            switch_config(rest_interface_module, node_id, Switch_conf()._replace(ethIfIndex=port,index=9), method='DELETE')
    
    bridge_config(rest_interface_module, node_id, Bridge_conf(1, 'PROVIDER_MSTP_EDGE', 100, 30, maxAge=6, maxHops=1, priority=12288), method='DELETE')

        # Port_Mirror_config(rest_interface_module, node_id, Port_Mirror_DATA[0]._replace(ethIfIndex=dest,phyIfMirrorRx=origin), method='POST')
        # Port_Mirror_config(rest_interface_module, node_id, Port_Mirror_DATA[0]._replace(ethIfIndex=dest,phyIfMirrorTx=origin), method='POST')
        # Port_Mirror_config(rest_interface_module, node_id, Port_Mirror_DATA[0]._replace(ethIfIndex=dest,phyIfMirrorBoth=origin,phyIfMirrorTx=origin+3, result="Fail"), method='POST')
        # Port_Mirror_config(rest_interface_module, node_id, Port_Mirror_DATA[0]._replace(ethIfIndex=dest,phyIfMirrorBoth=origin,phyIfMirrorRx=origin+4, result="Fail"), method='POST')

        # Port_Mirror_config(rest_interface_module, node_id, Port_Mirror_DATA[0]._replace(ethIfIndex=dest), method='DELETE')
        

        
                


        






