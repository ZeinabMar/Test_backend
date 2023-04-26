import pytest
import logging
import json
from config import *
from Switch.bridge_funcs import bridge_config
from collections import namedtuple
# from pytest-check import check


pytestmark = [pytest.mark.env_name("OLT_env"), pytest.mark.rest_dev("nms")]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

Port_Storm = namedtuple('Port_Storm', ['index' ,'ethIfIndex', 'phyIfStormBroadcast', 'phyIfStormDLF', 
                        'phyIfStormMulticast', 'result', 'shelfId', 'slotId', 'nodeId'])
Port_Storm.__new__.__defaults__ = (None, None, "-1", "-1", "-1", "Pass", 1, 1, None)
Port_Storm_DATA = (
    Port_Storm(1, None, "100", "54", "38", "Pass"),
    Port_Storm(2, None, "12", "15", "78", "Pass"),
    Port_Storm(3, None, "120", "15", "78", "Fail"),
    Port_Storm(4, None, "12", "150", "78", "Fail"),
    Port_Storm(5, None, "12", "15", "780", "Fail"),
    Port_Storm(6, None, "-1", "-1", "-1", "Pass")
)

def Port_Storm_config(rest_interface_module, node_id, Port_Storm_data=Port_Storm(), method='POST'):
    data = Port_Storm_data._replace(nodeId=node_id)
    logger.info(f"TRY TO {method} Port_Storm CONFIG ...")
    if method == 'POST' or method == 'DELETE':
        url = "/api/gponconfig/sp5100/portstormcontrolconfig/update"
        response = rest_interface_module.post_request(url, data._asdict())
   
    read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/portstormcontrolconfig/get/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.ethIfIndex}")
    input_data = json.loads(read_data.text)

    if data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in Port_Storm config {data._asdict}'
        if response.status_code != 200:
            logger.error(response.message)
        logger.info(f' GETTING Port_Storm-config (after {method} method) ... ')
        if method == 'POST':
            assert (str(input_data["ethIfIndex"]) == str(data.ethIfIndex) and
                    str(input_data["phyIfStormBroadcast"]) == str(data.phyIfStormBroadcast)+".000000" and
                    str(input_data["phyIfStormDLF"]) == str(data.phyIfStormDLF)+".000000" and
                    str(input_data["phyIfStormMulticast"]) == str(data.phyIfStormMulticast)+".000000"),f'GET ERROR in Port_Storm config (after {method})'
            logger.info(f'{data.ethIfIndex} every thing ok after Port_Storm config(after {method} ')

        else:  # method==DELETE
            assert (str(input_data["phyIfStormBroadcast"]) == "-1.000000" and 
                    str(input_data["phyIfStormDLF"]) == "-1.000000" and
                    str(input_data["phyIfStormMulticast"]) == "-1.000000"), f'GET ERROR in Port_Storm config (after {method})'
    else:
        assert response.status_code in range(400, 505), f'{method} ERROR in Port_Storm config {data._asdict}'


def test_Port_Storm_config(rest_interface_module, node_id):
    bridge_config(rest_interface_module, node_id, Bridge_conf(), method='POST')
    for port in range(1,25):   
        switch_config(rest_interface_module, node_id, Switch_conf._replace(ethIfIndex=port,index=9), method='POST')

    for port in range(1,7):
        for storm in Port_Storm_DATA:
            if storm.index==6:
                Port_Storm_config(rest_interface_module, node_id, storm._replace(ethIfIndex=port), method='DELETE')
            else:
                Port_Storm_config(rest_interface_module, node_id, storm._replace(ethIfIndex=port), method='POST')

    for port in range(1,25):   
        switch_config(rest_interface_module, node_id, Switch_conf._replace(ethIfIndex=port,index=10), method='DELETE')
    bridge_config(rest_interface_module, node_id, Bridge_conf(), method='DELETE')


