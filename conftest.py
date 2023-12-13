import pytest
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
board_ip = "192.168.9.127"


def join_oid(url_base, *indexes):
    suffix_url = ""
    list_indexes = [i for i in indexes]
    list_indexes = [i for i in list_indexes[0]]
    for  item in list_indexes:
        suffix_url = suffix_url+"/"+str(item[1])
    logger.info(f'HIIIIIIII   {suffix_url}')
    logger.info(f'looog    {list_indexes}')
    url = url_base+suffix_url        
    return url


def get_rest(rest_interface_module, feature, expected_get, url, *suffix_index):
    if len(expected_get.keys()) !=0:
            logger.info(f'*********** GETTING  IN {feature}  ********')
            url_get = join_oid(url, suffix_index)
            read_data = rest_interface_module.get_request(f"{url_get}")
            input_data = json.loads(read_data.text)
            logger.info(f'input_data {input_data}')
            for key in expected_get.keys():
                logger.info(f"IN {expected_get[key]}")
                check_set_value(rest_interface_module, expected_get[key][0], expected_get[key][1],input_data)
            logger.info(f'check is completed')


def check_set_value(rest_interface_module, set_value, result, data):
    logger.info(f'********************************check_set_value FUNCTION****************************')
    # logger.info(f"dataaaa {data}")
    # logger.info(f"resultttt {result}")
    rest_set_result = data[result]
    assert(rest_set_result==set_value),f"ERROR in SETTING {result} *******************************"    

def find_in_getall(data, item, value):
    logger.info(f"data {data}")        
    logger.info(f"item {item}")        
    for member in data:
        for key in member.keys():
            if key == item:
                logger.info(f"member[key] {member[key]}")  
                logger.info(f"value {value}")  
                if member[key] == value:
                    true_find = member
                    break
                else:
                    continue

    logger.info(f"member {true_find}")        
    return true_find


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



def getall_and_update_condition(rest_interface_module, url=None):
    logger.info(f"TRY GETTTING ALL IN ORDER TO BECOMING UPDATE ...")
    read_data = rest_interface_module.get_request(url)
    logger.info(f"dataaa {read_data}")
    assert(read_data.status_code == 200)  


def get_check(rest_interface_module, data=None, url=None):
    logger.info(f' GETTING ONUs INITIAL INFORMATION (after {method} method) ... ')
    read_data = rest_interface_module.get_request(url)
    input_data = json.loads(read_data.text)
    #**********************************************************************
    for key in data.keys():
        logger.info(f"{method} IN {data[key]}")
        check_set_value(rest_interface_module, data[key][0], data[key][1],input_data)
        logger.info(f'check is completed in {method} method')

def replace_dictionary(data = None, Method = "set", dict_replace=None):
    if Method == "set":
        dict_source = data.expected_result_Set
    else:
        dict_source = data.expected_result_Get 

    logger.info(f"sourceeee {dict_source}")
    for key1 in dict_source.keys():
        for key2 in dict_replace.keys():
            if key1==key2:
                dict[key1]=dict_replace[key2]
    if Method == "set":            
        data.expected_result_Set = dict_source
    else :   
        data.expected_result_Get = dict_source
    return data      



