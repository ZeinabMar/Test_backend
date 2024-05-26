import pytest
import json
import logging

logger = logging.getLogger(__name__)

# board_IP = input("Please Enter your Board IP:")

board_ip = "192.168.9.127"#board_IP #"192.168.9.128" #f"{board_IP}"#"


def join_oid(url_base, *indexes):
    suffix_url = ""
    list_indexes = [i for i in indexes]
    list_indexes = [i for i in list_indexes[0]]
    for  item in list_indexes:
        suffix_url = suffix_url+"/"+str(item[1])
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
    logger.info(f"TRY GETTTING ALL IN ORDER TO BECOME UPDATE ...")
    read_data = rest_interface_module.get_request(url)
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

    for key1 in dict_source.keys():
        for key2 in dict_replace.keys():
            if key1==key2:
                dict[key1]=dict_replace[key2]
    if Method == "set":            
        data.expected_result_Set = dict_source
    else :   
        data.expected_result_Get = dict_source
    return data      


class RestInterface:
    def __init__(self, host, username, password, client_version, contenttype, authenticate_url) -> None:
        self.host = host
        self.username = username
        self.password = password
        self.client_version = client_version
        self.contenttype = contenttype
        if authenticate_url == None:
            authenticate_url = '/authenticate'
        self.r = self.authenticate(authenticate_url)

    def authenticate(self, authenticate_url):
        self.data = {'username': self.username, 'password': self.password}
        self.header = {'client-version': self.client_version, 'Content-Type': self.contenttype}
        self.authen = self.host + authenticate_url
        logger.info("rest post request URL {}".format(authenticate_url))
        self.r = requests.post(self.authen, data=json.dumps(self.data), headers=self.header, verify=False)
        logger.info("result: status={}, response={}".format(self.r.status_code, self.r.text))
        return self.r

    def get_request(self, req):
        logger.info("rest get request URL={}".format(req))
        token = json.loads(self.r.text)['token']
        cookie = self.r.cookies.get_dict()
        headers = {'Authorization': 'Bearer {}'.format(token), 'Content-Type': self.contenttype}
        req1 = self.host + req
        response = requests.get(req1, headers=headers, cookies=cookie, verify=False)
        logger.info("result: status={}, response={}".format(response.status_code, response.text))
        return response
