
from pytest_sina_framework import SecretText
import sys

print(sys.argv)




DICT__SERVER = {
    'type': "NMS_Server",
    'server_ip': "192.168.9.127",
    'server_host': "https://192.168.1.65",
    'nms_username': "root",
    'nms_password': SecretText("root"),
    'authenticate_url': "/api/usermanagement/user/login",
    'rest_client-version': "",
    'rest_Content-Type': "application/json",
}

DICT__SIB_SERVER_1 = {
    'type': "sib_server",
    'ssh_ip': "192.168.110.3",
    'ssh_password': SecretText("1234"),
    'ssh_username': "saat",
    'ssh_port': "22"
}

DICT__SIB_SERVER_2 = {
    'type': "sib_server",
    'ssh_ip': "192.168.120.3",
    'ssh_password': SecretText("1234"),
    'ssh_username': "saat",
    'ssh_port': "22"
}
DICT__SIB_SERVER_3 = {
    'type': "sib_server",
    'ssh_ip': "192.168.130.3",
    'ssh_password': SecretText("1234"),
    'ssh_username': "saat",
    'ssh_port': "22"
}

DICT__SIB_SERVER_4 = {
    'type': "sib_server",
    'ssh_ip': "192.168.140.3",
    'ssh_password': SecretText("1234"),
    'ssh_username': "saat",
    'ssh_port': "22"
}

DICT__SIB_SERVER_5 = {
    'type': "sib_server",
    'ssh_ip': "192.168.150.3",
    'ssh_password': SecretText("1234"),
    'ssh_username': "saat",
    'ssh_port': "22"
}

DICT__SERVER_SSH = {
    'type': "server",
    'ssh_ip': "192.168.2.218",
    'ssh_password': SecretText("1234"),
    'ssh_username': "saat",
    'ssh_port': "22"
}

DICT__ENV = {
    'olt_nms': DICT__SERVER,
    'server_olt': DICT__SERVER_SSH,
    'server_olt_1': DICT__SIB_SERVER_1,
    'server_olt_2': DICT__SIB_SERVER_2,
    'server_olt_3': DICT__SIB_SERVER_3,
    'server_olt_4': DICT__SIB_SERVER_4,
    'server_olt_5': DICT__SIB_SERVER_5,
}




