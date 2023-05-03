import pytest
import logging
import json
from config import *
# from pytest-check import check


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("nms")]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

Static_Rout = namedtuple('Static_Rout', ['routeIndex', 'routingDstIp', 'routingNetmask', 
                     'routingPath', 'shelfId', 'slotId', 'result', 'nodeId'])
Static_Rout.__new__.__defaults__ = (None, None, None, None, 1, 1, "Pass", None)
Static_Rout_DATA = (
    Static_Rout(1, "192.168.45.0", "255.255.255.0", "192.168.78.45", 1, 1, "Pass"),
    Static_Rout(3, "192.168.45.0", "255.255.255.0", "192.168.78.45", 1, 1, "Fail"),
    Static_Rout(1, "192.168.46.0", "255.255.255.0", "192.168.78.45", 1, 1, "Fail"),#duplication data -10032
    Static_Rout(2, "192.168.46.0", "255.255.255.0", "192.168.78.45", 1, 1, "Pass"),
    Static_Rout(1),
    Static_Rout(2)
)

def Static_Route_config(rest_interface_module, node_id, Static_Rout_data=Static_Rout(), method='POST'):
    data = Static_Rout_data._replace(nodeId=node_id)
    logger.info(f"TRY TO {method} Static_Rout CONFIG ...")
    if method == 'add':
        url = "/api/gponconfig/sp5100/staticrouteconfig/add"
        response = rest_interface_module.post_request(url, data._asdict())  
    else:  # method==DELETE
        url = f"/api/gponconfig/sp5100/staticrouteconfig/delete/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.routeIndex}"
        response = rest_interface_module.delete_request(url)

    read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/staticrouteconfig/get/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.routeIndex}")
    input_data = json.loads(read_data.text)
    if data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in Static_Rout config {data._asdict}'
        if response.status_code != 200:
            logger.error(response.message)
        logger.info(f' GETTING Static_Rout-config (after {method} method) ... ')

        if method == 'add':
            assert (str(input_data["routeIndex"]) == str(data.routeIndex) and
                    str(input_data["routingDstIp"]) == str(data.routingDstIp) and 
                    str(input_data["routingNetmask"]) == str(data.routingNetmask) and
                    str(input_data["routingPath"]) == str(data.routingPath)),f'IN Everythig is ok Static_Rout config(after {method}'
            logger.info(f'every thing ok after Static_Rout config(after {method}')

        else:  # method==DELETE
            assert (str(input_data["routeIndex"]) == str(data.routeIndex) and
                    input_data["routingDstIp"] == None and 
                    input_data["routingNetmask"] == None and
                    input_data["routingPath"] == None), f'GET ERROR in Static_Rout config (after {method})'
    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in Static_Rout config {data._asdict}'


def test_Static_Route_config(rest_interface_module, node_id):
    
    Static_Route_config(rest_interface_module, node_id, Static_Rout_DATA[0], method='add')
    Static_Route_config(rest_interface_module, node_id, Static_Rout_DATA[1], method='add')
    Static_Route_config(rest_interface_module, node_id, Static_Rout_DATA[2], method='add')
    Static_Route_config(rest_interface_module, node_id, Static_Rout_DATA[3], method='add')
    Static_Route_config(rest_interface_module, node_id, Static_Rout_DATA[4], method='DELETE')
    Static_Route_config(rest_interface_module, node_id, Static_Rout_DATA[5], method='DELETE')



            
                    


        