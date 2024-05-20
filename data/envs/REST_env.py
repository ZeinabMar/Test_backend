
from pytest_sina_framework import SecretText

DICT__SERVER = {
    'type': "NMS_Server",
    'server_ip': "192.168.9.127",
    'server_host': "https://192.168.5.212",
    'nms_username': "root",
    'nms_password': SecretText("root"),
    'authenticate_url': "/api/usermanagement/user/login",
    'rest_client-version': "",
    'rest_Content-Type': "application/json",
}

DICT__SIB_SERVER_1 = {
    'type': "RaspberryPi",
    'ssh_ip': "192.168.2.136",
    'ssh_password': SecretText("1234"),
    'ssh_username': "root",
    'ssh_port': "22"
}

DICT__SIB_SERVER_2 = {
    'type': "RaspberryPi",
    'ssh_ip': "192.168.2.136",
    'ssh_password': SecretText("1234"),
    'ssh_username': "root",
    'ssh_port': "22"
}
DICT__SIB_SERVER_3 = {
    'type': "RaspberryPi",
    'ssh_ip': "192.168.2.136",
    'ssh_password': SecretText("1234"),
    'ssh_username': "root",
    'ssh_port': "22"
}

DICT__ENV = {
    'server_olt_1': DICT__SIB_SERVER_1,
    'server_olt_2': DICT__SIB_SERVER_2,
    'server_olt_3': DICT__SIB_SERVER_3,
    'olt_nms': DICT__SERVER,
}




