import pytest
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
board_ip = "192.168.9.130"


def search_in_tree(tree, nodes):
    for item in tree:
        if item['childrenNodes']:
            search_in_tree(item['childrenNodes'], nodes)
        else:
            nodes.append({"ip": item["ip"],
                        "id": item["id"],
                        "name": item["name"],
                        "type": item["type"]})

@pytest.fixture(scope="module")
def get_zone_tree(rest_interface_module):
    r = rest_interface_module.get_request("/api/protocol/zone/getZoneTree")
    print(f"rrrr{r}")
    assert 200 == r.status_code
    tree = json.loads(r.text)
    nodes = []
    for i in range(len(tree)):
        search_in_tree(tree[i]['childrenNodes'], nodes)
    return nodes


@pytest.fixture(scope="module")
def node_id(rest_interface_module, get_zone_tree):
    """ build test data by filling the nodeId part in TESTDATA dict."""
    logger.info(f'DEVICES IN ZONE TREE : {get_zone_tree}')
    for node in get_zone_tree:
        if node["ip"] == board_ip:
            return node["id"]



