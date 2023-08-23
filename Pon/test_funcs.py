import pytest
import logging
import json


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



dba_general_data = [{
        "id": None,
        "nodeId": None,
        "shelfId": 1,
        "slotId": 1,
        "dbaId": None,
        "name": "dba_test",
        "dbaType": 3,
        "fixedBwValue": 250,
        "assureBwValue": 500,
        "maxBwValue": 1000,
        "result": "Pass"
    }]


def set_dba_profile(rest_interface_module, node_id, DBA_data=dba_general_data):
    for data in DBA_data:
        logger.info(f"DBA TEST-DATA --> {data}")
        data["nodeId"] = node_id
        data["shelfId"] = 1
        data["slotId"] = 1
        logger.info(f"dataaaaa first  {data}")
        r = rest_interface_module.post_request("/api/gponconfig/dbaProfile/add", data)
        if data["result"] == "Pass":
            assert r.status_code == 200
            read_data = rest_interface_module.get_request("/api/gponconfig/dbaProfile/getall/?nodeId={}&shelfId=1&slotId=1".format(data["nodeId"]))
            logger.info(f"dataaaaa {read_data}")
            output_data = list(filter(lambda dic: dic["name"] == data["name"], json.loads(read_data.text)))
            assert output_data[0]["dbaType"] == data["dbaType"]
        else:
            assert r.status_code == 500


def delete_dba_profile(rest_interface_module, node_id, DBA_data=dba_general_data):
    for dba_id, data in enumerate(DBA_data):
        logger.info(f"DEL DBA TEST-DATA --> {data}")
        data["nodeId"] = node_id
        data["shelfId"] = 1
        data["slotId"] = 1
        response = rest_interface_module.delete_request(f"/api/gponconfig/dbaProfile/delete/{node_id}/1/1/{dba_id+1}")
        if data["result"] == "Pass":
            assert 200 == response.status_code
            read_data = rest_interface_module.get_request("/api/gponconfig/dbaProfile/getall/?nodeId={}&shelfId=1&slotId=1".format(data["nodeId"]))
            if read_data.text:
                output_data = list(filter(lambda dic: dic["name"] == data["name"], json.loads(read_data.text)))
                assert len(output_data) == 0
        else:
            assert 500 == response.status_code


onu_general_data = [{
	"adminState": "ENABLE",
	"autoLearn": "ENABLE",
	"ifIndex": 1,
	"ponOnuAutoDiscovery": "ENABLE",
	"portId": 1,
	"shelfId": 1,
	"slotId": 1,
    "result": "Pass"
}]


def onu_auto_learn(rest_interface_module, node_id, ONU_data=onu_general_data):
    for data in ONU_data:
        logger.info(f"ONU TEST-DATA --> {data}")
        data["nodeId"] = node_id
        response = rest_interface_module.post_request("/api/gponconfig/pon/saveprimaryinfo/add", data)
        if data["result"] == "Pass":
            assert 200 == response.status_code
            read_data = rest_interface_module.get_request("/api/gponconfig/onu/getallauthenticated")
            input_data = list(filter(lambda dic: dic["ifIndex"] == data["ifIndex"], json.loads(read_data.text)))
            assert input_data[0]["onuState"] == "OPERATION_STATE"
        else:
            assert 500 == response.status_code


add_dba_data = [
    {"name": "dba_test", "dbaType": 1, "fixedBwValue": 32000, "assureBwValue": None, "maxBwValue": None, "result": "Pass"},
    {"name": "dba_test1", "dbaType": 1, "fixedBwValue": 32000, "assureBwValue": None, "maxBwValue": None, "result": "Pass"},
    {"name": "dba_test2", "dbaType": 2, "fixedBwValue": None, "assureBwValue": 128000, "maxBwValue": None, "result": "Pass"},
    {"name": "dba_test3", "dbaType": 3, "fixedBwValue": None, "assureBwValue": 256000, "maxBwValue": 512000, "result": "Pass"},
    {"name": "dba_test5-1", "dbaType": 5, "fixedBwValue": 250, "assureBwValue": 500, "maxBwValue": 1000, "result": "Pass"},
    {"name": "dba_test5-2", "dbaType": 5, "fixedBwValue": 6000, "assureBwValue": 14000, "maxBwValue": 22000, "result": "Pass"},
    {"name": "dba_test5-3", "dbaType": 5, "fixedBwValue": 750000, "assureBwValue": 1000000, "maxBwValue": 1200000, "result": "Pass"},
    {"name": "dba_test5-4", "dbaType": 5, "fixedBwValue": 750000, "assureBwValue": 500000, "maxBwValue": 1200000, "result": "Fail"},
    {"name": "dba_test5-5", "dbaType": 5, "fixedBwValue": 900000, "assureBwValue": 1000000, "maxBwValue": 1200000, "result": "Fail"},
]


def test_add_dba_profile(rest_interface_module, node_id):

    set_dba_profile(rest_interface_module, node_id, add_dba_data)

    delete_dba_profile(rest_interface_module, node_id, add_dba_data)


def test_onu_authentication(rest_interface_module, node_id):
    onu_auto_learn(rest_interface_module, node_id)


tcont_general_data = [
    {
    "bwProfileId": 1,
    "bwProfileName": "dbatest",
    "name": "tcont-test",
    "onuId": 1,
    "portId": 1,
    "tcontId": "1",
    "result": "Pass"
    }]

def tcont_add_profile(rest_interface_module, node_id, TCONT_data=tcont_general_data):
    for data in TCONT_data:
        logger.info(f"TCONT TEST-DATA --> {data}")
        data["nodeId"] = node_id
        data["shelfId"] = 1
        data["slotId"] = 1
        response = rest_interface_module.post_request("/api/gponconfig/tcont/add", data)
        if data["result"] == "Pass":
            assert response.status_code == 200
            read_data = rest_interface_module.get_request(f"/api/gponconfig/tcont/getall?nodeId={node_id}&shelfId=1&slotId=1&portId={data['portId']}&onuId={data['onuId']}")
            input_data = list(filter(lambda dic: dic["name"] == data["name"], json.loads(read_data.text)))
            assert int(input_data[0]["tcontId"]) == int(data["tcontId"])
        else:
            assert 500 == response.status_code

def tcont_delete_profile(rest_interface_module, node_id, TCONT_data=tcont_general_data):
    for data in TCONT_data:
        logger.info(f"DEL TCONT TEST-DATA --> {data}")
        response = rest_interface_module.delete_request(f"/api/gponconfig/tcont/delete/{node_id}/1/1/{data['portId']}/{data['onuId']}/{data['tcontId']}")
        if data["result"] == "Pass":
            assert 200 == response.status_code
            read_data = rest_interface_module.get_request(f"/api/gponconfig/tcont/getall?nodeId={node_id}&shelfId=1&slotId=1&portId={data['portId']}&onuId={data['onuId']}")
            if read_data.text:
                output_data = list(filter(lambda dic: dic["name"] == data["name"], json.loads(read_data.text)))
                assert len(output_data) == 0
        else:
            assert 500 == response.status_code
dba_data_for_tcont = [
    {"name": "dba1_type1", "dbaType": 1, "fixedBwValue": 32000, "assureBwValue": None, "maxBwValue": None, "result": "Pass"},
    {"name": "dba2_type2", "dbaType": 2, "fixedBwValue": None, "assureBwValue": 128000, "maxBwValue": None, "result": "Pass"},
    {"name": "dba3_type3", "dbaType": 3, "fixedBwValue": None, "assureBwValue": 256000, "maxBwValue": 521000, "result": "Pass"},
    {"name": "dba4_type5", "dbaType": 5, "fixedBwValue": 32000, "assureBwValue": 64000, "maxBwValue": 128000, "result": "Pass"},
    {"name": "dba5_type5", "dbaType": 5, "fixedBwValue": 75000, "assureBwValue": 400000, "maxBwValue": 500000, "result": "Pass"},
    {"name": "dba6_type5", "dbaType": 5, "fixedBwValue": 250, "assureBwValue": 500, "maxBwValue": 1000, "result": "Pass"},
]


tcont_data = [
    {"bwProfileId": 1, "bwProfileName": "dba1_type1", "name": "tcont_valid1", "onuId": 1, "portId": 1, "tcontId": 8, "result": "Pass"},
    {"bwProfileId": 2, "bwProfileName": "dba2_type2", "name": "tcont_valid2", "onuId": 1, "portId": 1, "tcontId": 4, "result": "Pass"},
    {"bwProfileId": 3, "bwProfileName": "dba3_type3", "name": "tcont_valid3", "onuId": 1, "portId": 1, "tcontId": 6, "result": "Pass"},
    {"bwProfileId": 4, "bwProfileName": "dba4_type5", "name": "tcont_valid4", "onuId": 1, "portId": 1, "tcontId": 2, "result": "Pass"},
    {"bwProfileId": 5, "bwProfileName": "dba5_type5", "name": "tcont_valid5", "onuId": 1, "portId": 1, "tcontId": 5, "result": "Pass"},
    {"bwProfileId": 6, "bwProfileName": "dba6_type5", "name": "tcont_valid6", "onuId": 1, "portId": 1, "tcontId": 1, "result": "Pass"},
    {"bwProfileId": 6, "bwProfileName": "dba6_type5", "name": "tcont_duplicate", "onuId": 1, "portId": 1, "tcontId": 1, "result": "Fail"},
    {"bwProfileId": 1, "bwProfileName": "dba_invalid", "name": "tcont_invalid_dba", "onuId": 1, "portId": 1, "tcontId": 1, "result": "Fail"},
    {"bwProfileId": 1, "bwProfileName": "dba1_type1", "name": "tcont_disable_pon", "onuId": 1, "portId": 5, "tcontId": 1, "result": "Fail"},
    {"bwProfileId": 1, "bwProfileName": "dba1_type1", "name": "tcont_invalid_id", "onuId": 1, "portId": 5, "tcontId": 9, "result": "Fail"},
]


def test_tcont_profile(rest_interface_module, node_id):

    set_dba_profile(rest_interface_module, node_id, DBA_data=dba_data_for_tcont)

    tcont_add_profile(rest_interface_module, node_id, TCONT_data=tcont_data)

    tcont_delete_profile(rest_interface_module, node_id, TCONT_data=tcont_data)

    delete_dba_profile(rest_interface_module, node_id, DBA_data=dba_data_for_tcont)


gem_general_data = [
    {
    "gemId": "1",
    "name": "gem-test",
    "onuId": 1,
    "portId": 1,
    "tcontId": 1,
    "tcontName": "tcont-test",
    "result": "Pass"
    }]


def gem_add_profile(rest_interface_module, node_id, GEM_data=gem_general_data):
    for data in GEM_data:
        logger.info(f"GEM TEST-DATA --> {data}")
        data["nodeId"] = node_id
        data["shelfId"] = 1
        data["slotId"] = 1
        response = rest_interface_module.post_request("/api/gponconfig/gem/add", data)
        if data["result"] == "Pass":
            assert response.status_code == 200
            read_data = rest_interface_module.get_request(f"/api/gponconfig/gem/getall?nodeId={node_id}&shelfId=1&slotId=1&portId={data['portId']}&onuId={data['onuId']}")
            input_data = list(filter(lambda dic: dic["name"] == data["name"], json.loads(read_data.text)))
            assert int(input_data[0]["gemId"]) == int(data["gemId"])
        else:
            assert 500 == response.status_code

def gem_delete_profile(rest_interface_module, node_id, GEM_data=gem_general_data):
    for data in GEM_data:
        logger.info(f"DEL GEM TEST-DATA --> {data}")
        response = rest_interface_module.delete_request(f"/api/gponconfig/gem/delete/{node_id}/1/1/{data['portId']}/{data['onuId']}/{data['gemId']}")
        if data["result"] == "Pass":
            assert 200 == response.status_code
            read_data = rest_interface_module.get_request(f"/api/gponconfig/gem/getall?nodeId={node_id}&shelfId=1&slotId=1&portId={data['portId']}&onuId={data['onuId']}")
            if read_data.text:
                output_data = list(filter(lambda dic: dic["name"] == data["name"], json.loads(read_data.text)))
                assert len(output_data) == 0
        else:
            assert 500 == response.status_code



tcont_data_for_gem = [
    {"bwProfileId": 1, "bwProfileName": "dba1_type1", "name": "tcont_valid8", "onuId": 1, "portId": 1, "tcontId": 8, "result": "Pass"},
    {"bwProfileId": 2, "bwProfileName": "dba2_type2", "name": "tcont_valid4", "onuId": 1, "portId": 1, "tcontId": 4, "result": "Pass"},
    {"bwProfileId": 3, "bwProfileName": "dba3_type3", "name": "tcont_valid6", "onuId": 1, "portId": 1, "tcontId": 6, "result": "Pass"},
    {"bwProfileId": 4, "bwProfileName": "dba4_type5", "name": "tcont_valid2", "onuId": 1, "portId": 1, "tcontId": 2, "result": "Pass"},
]

gem_data = [
    {"gemId": "1","name": "gem1","onuId": 1,"portId": 1,"tcontId": 8,"tcontName": "tcont_valid8","result": "Pass"},
    {"gemId": "2","name": "gem2","onuId": 1,"portId": 1,"tcontId": 6,"tcontName": "tcont_valid6","result": "Pass"},
    {"gemId": "3","name": "gem3","onuId": 1,"portId": 1,"tcontId": 4,"tcontName": "tcont_valid4","result": "Pass"},
    {"gemId": "4","name": "gem4", "onuId": 1,"portId": 1,"tcontId": 2,"tcontName": "tcont_valid2","result": "Pass"},
    {"gemId": "5","name": "gem5","onuId": 1,"portId": 1,"tcontId": 8,"tcontName": "tcont_valid8","result": "Pass"},
    {"gemId": "6","name": "gem6","onuId": 1,"portId": 1,"tcontId": 6,"tcontName": "tcont_valid6","result": "Pass"},
    {"gemId": "28","name": "gem28","onuId": 1,"portId": 1,"tcontId": 4,"tcontName": "tcont_valid4","result": "Pass"},
    {"gemId": "29","name": "gem29","onuId": 1,"portId": 1,"tcontId": 2,"tcontName": "tcont_valid2","result": "Pass"},
    {"gemId": "30","name": "gem30","onuId": 1,"portId": 1,"tcontId": 8,"tcontName": "tcont_valid8","result": "Pass"},
    {"gemId": "15","name": "gem_invalid_tcont","onuId": 1,"portId": 1,"tcontId": 3,"tcontName": "tcont_invalid","result": "Fail"},
    ]


def test_gem_profile(rest_interface_module, node_id):


    set_dba_profile(rest_interface_module, node_id, DBA_data=dba_data_for_tcont)

    tcont_add_profile(rest_interface_module, node_id, TCONT_data=tcont_data_for_gem)

    gem_add_profile(rest_interface_module, node_id, GEM_data=gem_data)

    gem_delete_profile(rest_interface_module, node_id, GEM_data=gem_data)

    tcont_delete_profile(rest_interface_module, node_id, TCONT_data=tcont_data_for_gem)

    delete_dba_profile(rest_interface_module, node_id, DBA_data=dba_data_for_tcont)


service_general_data = [{
    "servicePortId": 1,
    "portId": 1,
    "onuId": 1,
    "gemId": 1,
    "userVlan": 200,
    "innerVlan": 0,
    "vlanPriority": 0,
    "result": "Pass"
}]


def service_add_profile(rest_interface_module, node_id, SERVICE_data=service_general_data):
    for data in SERVICE_data:
        logger.info(f"SERVICE TEST-DATA --> {data}")
        data["nodeId"] = node_id
        data["shelfId"] = 1
        data["slotId"] = 1
        data["innerVlan"] = 0
        data["vlanPriority"] = 0
        response = rest_interface_module.post_request("/api/gponconfig/service/add", data)
        if data["result"] == "Pass":
            assert response.status_code == 200
            read_data = rest_interface_module.get_request(f"/api/gponconfig/service/getall?nodeId={node_id}&shelfId=1&slotId=1&portId={data['portId']}&onuId={data['onuId']}")
            input_data = list(filter(lambda dic: dic["servicePortId"] == data["servicePortId"], json.loads(read_data.text)))
            assert int(input_data[0]["userVlan"]) == int(data["userVlan"])
        else:
            assert 500 == response.status_code


def service_delete_profile(rest_interface_module, node_id, SERVICE_data=service_general_data):
    for data in SERVICE_data:
        logger.info(f"DEL SERVICE TEST-DATA --> {data}")
        response = rest_interface_module.delete_request(f"/api/gponconfig/service/delete/{node_id}/1/1/{data['portId']}/{data['onuId']}/{data['servicePortId']}")
        if data["result"] == "Pass":
            assert 200 == response.status_code
            read_data = rest_interface_module.get_request(f"/api/gponconfig/service/getall?nodeId={node_id}&shelfId=1&slotId=1&portId={data['portId']}&onuId={data['onuId']}")
            if read_data.text:
                output_data = list(filter(lambda dic: dic["servicePortId"] == data["servicePortId"], json.loads(read_data.text)))
                assert len(output_data) == 0
        else:
            assert 500 == response.status_code


gem_data_for_other_TCs=[
    {"gemId": "1", "name": "gem_test1", "onuId": 1, "portId": 1,"tcontId": 1, "tcontName": "tcont-test","result": "Pass"},
    {"gemId": "2", "name": "gem2", "onuId": 1, "portId": 1, "tcontId": 1, "tcontName": "tcont-test", "result": "Pass"}]


service_data = [
    {"servicePortId": 3, "portId": 1, "onuId": 1, "gemId": 1, "userVlan": 20, "innerVlan": 0, "vlanPriority": 0, "result": "Pass"},
    {"servicePortId": 1, "portId": 1, "onuId": 1, "gemId": 2, "userVlan": 200, "innerVlan": 0, "vlanPriority": 0, "result": "Pass"},
    {"servicePortId": 2, "portId": 1, "onuId": 1, "gemId": 1, "userVlan": 400, "innerVlan": 0, "vlanPriority": 0, "result": "Pass"},
    {"servicePortId": 4, "portId": 1, "onuId": 1, "gemId": 2, "userVlan": 1600, "innerVlan": 0, "vlanPriority": 0, "result": "Pass"},
    {"servicePortId": 5, "portId": 1, "onuId": 1, "gemId": 15, "userVlan": 200, "innerVlan": 0, "vlanPriority": 0, "result": "Fail"},
    {"servicePortId": 1, "portId": 1, "onuId": 2, "gemId": 1, "userVlan": 200, "innerVlan": 0, "vlanPriority": 0, "result": "Fail"},
    ]


def test_service_profile(rest_interface_module, node_id):

    set_dba_profile(rest_interface_module, node_id, DBA_data=dba_data_for_tcont)

    tcont_add_profile(rest_interface_module, node_id, TCONT_data=tcont_general_data)

    gem_add_profile(rest_interface_module, node_id, GEM_data=gem_data_for_other_TCs)

    service_add_profile(rest_interface_module, node_id, SERVICE_data=service_data)

    service_delete_profile(rest_interface_module, node_id, SERVICE_data=service_data)

    gem_delete_profile(rest_interface_module, node_id, GEM_data=gem_data_for_other_TCs)

    tcont_delete_profile(rest_interface_module, node_id, TCONT_data=tcont_general_data)

    delete_dba_profile(rest_interface_module, node_id, DBA_data=dba_data_for_tcont)



remote_service_general_data = [
    {"portId": 1, "onuId": 1, "rmServiceId": 1, "onuPortType": "ETH_UNI",
     "onuPortId": 1, "vlanMode": "ACCESS", "gemId": 1, "pvId": 750, "priority": 1, "result": "Pass"}
]


def remote_service_add_profile(rest_interface_module, node_id, REMOTE_SERVICE_data=remote_service_general_data):
    for data in REMOTE_SERVICE_data:
        logger.info(f"REMOTE_SERVICE TEST-DATA --> {data}")
        data["nodeId"] = node_id
        data["shelfId"] = 1
        data["slotId"] = 1
        data["innerVlan"] = 0
        data["vlanPriority"] = 0
        response = rest_interface_module.post_request("/api/gponconfig/sp5100/rmonu/service/add", data)
        if data["result"] == "Pass":
            assert response.status_code == 200
            read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/rmonu/service/getall?nodeId={node_id}&shelfId=1&slotId=1&onuId={data['onuId']}&portId={data['portId']}")
            input_data = list(filter(lambda dic: dic["rmServiceId"] == data["rmServiceId"], json.loads(read_data.text)))
            assert str(input_data[0]["vlanMode"]) == str(data["vlanMode"])
        else:
            assert 500 == response.status_code

def remote_service_delete_profile(rest_interface_module, node_id, REMOTE_SERVICE_data=remote_service_general_data):
    for data in REMOTE_SERVICE_data:
        logger.info(f"DEL REMOTE_SERVICE TEST-DATA --> {data}")
        response = rest_interface_module.delete_request(f"/api/gponconfig/sp5100/rmonu/service/delete/{node_id}/1/1/{data['portId']}/{data['onuId']}/{data['rmServiceId']}")
        if data["result"] == "Pass":
            assert 200 == response.status_code
            read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/rmonu/service/getall?nodeId={node_id}&shelfId=1&slotId=1&onuId={data['onuId']}&portId={data['portId']}")
            if read_data.text:
                output_data = list(filter(lambda dic: dic["rmServiceId"] == data["rmServiceId"], json.loads(read_data.text)))
                assert len(output_data) == 0
        else:
            assert 500 == response.status_code


remote_service_data = [
    {"portId": 1, "onuId": 1, "rmServiceId": 1, "onuPortType": "VEIP", "onuPortId": 1, "vlanMode": "ACCESS", "gemId": 1, "pvId": 50, "vlanList": None, "priority": 3, "result": 'Pass'},
    {"portId": 1, "onuId": 1, "rmServiceId": 2, "onuPortType": "VEIP", "onuPortId": 1, "vlanMode": "TRUNK", "gemId": 2, "pvId": None, "vlanList": "60", "priority": 2, "result": 'Pass'},
    {"portId": 1, "onuId": 1, "rmServiceId": 3, "onuPortType": "VEIP", "onuPortId": 1, "vlanMode": "HYBRID", "gemId": 1, "pvId": 10, "vlanList": "20", "priority": 1, "result": 'Pass'},
    {"portId": 1, "onuId": 1, "rmServiceId": 4, "onuPortType": "ETH_UNI", "onuPortId": 1, "vlanMode": "XLATE", "gemId": 2, "pvId": "60", "vlanList": "70", "priority": 1, "result": 'Pass'},
    {"portId": 1, "onuId": 1, "rmServiceId": 5, "onuPortType": "ETH_UNI", "onuPortId": 1, "vlanMode": "TRANSPARENT", "gemId": 1, "pvId": None, "vlanList": None, "priority": 1, "result": 'Pass'},
    {"portId": 1, "onuId": 1, "rmServiceId": 1, "onuPortType": "ETH_UNI", "onuPortId": 1, "vlanMode": None, "gemId": 1, "pvId": 750, "vlanList": "500", "priority": 1, "result": 'Fail'},
]


def test_remote_service_profile(rest_interface_module, node_id):

    set_dba_profile(rest_interface_module, node_id, DBA_data=dba_data_for_tcont)

    tcont_add_profile(rest_interface_module, node_id, TCONT_data=tcont_general_data)

    gem_add_profile(rest_interface_module, node_id, GEM_data=gem_data_for_other_TCs)

    remote_service_add_profile(rest_interface_module, node_id, REMOTE_SERVICE_data=remote_service_data)

    remote_service_delete_profile(rest_interface_module, node_id, REMOTE_SERVICE_data=remote_service_data)

    gem_delete_profile(rest_interface_module, node_id, GEM_data=gem_data_for_other_TCs)

    tcont_delete_profile(rest_interface_module, node_id, TCONT_data=tcont_general_data)

    delete_dba_profile(rest_interface_module, node_id, DBA_data=dba_data_for_tcont)



bridge_general_data = [{
    "bridgeId": 1,
    "bridgeProtocol": "IEEE",
    "ageingTime": 0,
    "forwardTime": 0,
    "helloTime": 0,
    "maxAge": 0,
    "maxHops": 0,
    "priority": 0,
    "id": 1,
    "result": "Pass"
}]


def set_bridge(rest_interface_module, node_id, BRIDGE_data=bridge_general_data):
    for data in BRIDGE_data:
        logger.info(f"BRIDGE TEST-DATA --> {data}")
        data["nodeId"] = node_id
        data["shelfId"] = 1
        data["slotId"] = 1
        response = rest_interface_module.post_request("/api/gponconfig/sp5100/bridgeconfig/add", data)
        if data["result"] == "Pass":
            assert response.status_code == 200
            read_data = rest_interface_module.get_request(f"/api/gponconfig/sp5100/bridgeconfig/getall?nodeId={node_id}&shelfId=1&slotId=1")
            input_data = list(filter(lambda dic: dic["bridgeId"] == data["bridgeId"], json.loads(read_data.text)))
            assert str(input_data[0]["bridgeProtocol"]) == str(data["bridgeProtocol"])
        else:
            assert response.status_code == 500


def test_set_bridge(rest_interface_module, node_id):
    set_bridge(rest_interface_module, node_id)
