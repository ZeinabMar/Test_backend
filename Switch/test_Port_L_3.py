import pytest
import logging
import json
from conftest import *
from config import *
# from pytest-check import check


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

Port_L3 = namedtuple('Port_L3', ['index', 'ifIndex', 'l3IfIpAddress', 'l3IfNetmask', 'l3IfArpAgeingTimeOut',
                     'l3IfArpReachableTime', 'shelfId', 'slotId', 'result', 'nodeId'])
Port_L3.__new__.__defaults__ = (None, None, None, None, -1, -1, 1, 1, "Pass", None)
Port_L3_DATA = (
    Port_L3(1, 1, "192.168.66.2", "255.255.255.0", 22500, 1345, 1, 1, "Pass"),
    Port_L3(2, 1, "192.168.66.2", "255.255.255.0", 6450, 1789, 1, 1, "Pass"),
    Port_L3(3, 2, "192.168.66.3", "255.255.255.0", 22500, 1345, 1, 1, "Fail"),

)

Port_L3_DELETE = (
    Port_L3(4, 1),
    Port_L3(5, 2)

)

def Port_L3_config(rest_interface_module, node_id, Port_L3_data=Port_L3(), method='POST'):
    data = Port_L3_data._replace(nodeId=node_id)
    logger.info(f"TRY TO {method} Port_L3 CONFIG IN {data.index} NUMBER OF DATA...")
    if method == 'POST':
        url = "/api/gponconfig/sp5100/portl3/update"
        response = rest_interface_module.post_request(url, data._asdict())
    else:  # method==DELETE
        url = f"/api/gponconfig/sp5100/portl3/delete/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.ifIndex}"
        response = rest_interface_module.delete_request(url)

    read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/portl3/get/{data.nodeId}/{data.shelfId}/{data.slotId}/{data.ifIndex}")
    input_data = json.loads(read_data.text)
    if data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in Port_L3 config {data._asdict}'
        if response.status_code != 200:
            logger.error(response.message)
        logger.info(f' GETTING Port_L3-config (after {method} method) ... ')

        if method == 'POST':
            assert (str(input_data["l3IfIpAddress"]) == str(data.l3IfIpAddress) and
                    str(input_data["l3IfNetmask"]) == str(data.l3IfNetmask) and 
                    input_data["l3IfArpAgeingTimeOut"] == data.l3IfArpAgeingTimeOut and
                    input_data["l3IfArpReachableTime"] == data.l3IfArpReachableTime and
                    input_data["ifIndex"] == data.ifIndex),f'IN Everythig is ok Port_L3 config(after {method}'
            logger.info(f'every thing ok after Port_L3 config(after {method}')

        else:  # method==DELETE
            assert (len(input_data["l3IfIpAddress"]) == 0 and
                    len(input_data["l3IfNetmask"]) == 0 and 
                    input_data["l3IfArpAgeingTimeOut"] == -1 and
                    input_data["l3IfArpReachableTime"] == -1), f'GET ERROR in Port_L3 config (after {method})'
    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in Port_L3 config {data._asdict}'


def test_Port_L3_config(rest_interface_module, node_id):

    for portl3 in Port_L3_DATA:
        response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/portl3/getall?nodeId={node_id}&shelfId=1&slotId=1")
        Port_L3_config(rest_interface_module, node_id, portl3, method='POST')
    for portl3_del in Port_L3_DELETE:
        response = getall_and_update_condition(rest_interface_module,f"/api/gponconfig/sp5100/portl3/getall?nodeId={node_id}&shelfId=1&slotId=1")
        Port_L3_config(rest_interface_module, node_id, portl3_del, method='DELETE') 


            

                    


        