import pytest
import logging
import json
from config import *
# from pytest-check import check

pytestmark = [pytest.mark.env_name("OLT_env"), pytest.mark.rest_dev("nms")]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


Qos_Manage = namedtuple('Qos_Manage', ['qosIndex', 'qosState', 'shelfId', 'slotId', 'result', 'nodeId'])
Qos_Manage.__new__.__defaults__ = (1, -1, 1, 1, "Pass", None)
Qos_Manage_DATA = (
    Qos_Manage(1, 1, 1, 1),
    Qos_Manage(1, -1, 1, 1),
    Qos_Manage(1, -1, 1, 1, "FAIL"),#invalis repeated data
    Qos_Manage(1, 0, 1, 1, "FAIL"),#invalis
    Qos_Manage(2, 1, 1, 1, "FAIL")#invalid
)

def Qos_Manage_config(rest_interface_module, node_id, QoS_MANAGE_data=Qos_Manage(), method='POST'):
    data = QoS_MANAGE_data._replace(nodeId=node_id)
    logger.info(f"TRY TO {method} QoS_MANAGE CONFIG ...")
    if method == 'POST':
        url = "/api/gponconfig/sp5100/qosmanagement/update"
        response = rest_interface_module.post_request(url, data._asdict())

    read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/qosmanagement/get/{data.nodeId}/{data.shelfId}/{data.slotId}")
    input_data = json.loads(read_data.text)
    if data.result == "Pass":
        assert response.status_code == 200, f'{method} ERROR in QoS_MANAGE config {data._asdict}'
        if response.status_code != 200:
            logger.error(response.message)
        logger.info(f' GETTING QoS_MANAGE-config (after {method} method) ... ')
        # read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/qosmanagement/get/{data.nodeId}/{data.shelfId}/{data.slotId}")
        # input_data = json.loads(read_data.text)
        if method == 'POST':
            assert str(input_data["qosState"]) == str(data.qosState) ,f'IN Everythig is ok QoS_MANAGE config(after {method}'
            logger.info(f'every thing ok after QoS_MANAGE config(after {method}')
            # check.equal(str(input_data[0]["ethIfIndex"]) ,str(data.ethIfIndex), f'IN {data.ethIfIndex} Everythig is ok switch config(after {method}')

        else:  # method==DELETE
            # check.equal(str(input_data[0]["ethIfIndex"]) ,None ,f'IN {data.ethIfIndex} Everythig is ok switch config(after {method}')
            assert input_data["qosState"] == -1, f'GET ERROR in QoS_MANAGE config (after {method})'
    else:
        assert response.status_code in range(400, 505), f'{method} SET INCORRECT DATA in QoS_MANAGE config {data._asdict}'



def test_Qos_Manage_config(rest_interface_module, node_id):
    for qos in Qos_Manage_DATA:
        Qos_Manage_config(rest_interface_module, node_id, qos, method='POST')
    # Qos_Manage_config(rest_interface_module, node_id, qos, method='DELETE')
