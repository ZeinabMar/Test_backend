
from pytest_sina_framework import SecretText

DICT__SERVER = {
    'type': "NMS_Server",
    'server_ip': "192.168.9.130",
    'server_host': "https://192.168.1.65",
    'nms_username': "root",
    'nms_password': SecretText("root"),
    'authenticate_url': "/api/usermanagement/user/login",
    'rest_client-version': "",
    'rest_Content-Type': "application/json",
}

DICT__ENV = {
    'olt_nms': DICT__SERVER
}


