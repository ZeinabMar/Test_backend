import paramiko
import logging
import time
import socket
from clilib import CliInterface
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def copy_log_to_server(name_of_test,ip,user,password):
    cli_interface_module = CliInterface(f"{ip}", f"{user}", f"{password}", ssh_port=22, colored_output=True)
    Name_Of_Log = ["i2c", "daemon", "katana", "maple", "snmp", "cli"]
    for name_of_log in Name_Of_Log:
        time.sleep(3)
        detail_result = cli_interface_module.exec(f"scp -r /sp5100/metadata/log/{name_of_log}.log test@192.168.1.109:/home/test/{name_of_log}_{name_of_test}.log")  
        time.sleep(2)  
        if detail_result.find("can't be established")!=-1:  
            cli_interface_module.exec("yes")  
            cli_interface_module.exec("test") 
        elif detail_result.find("test@192.168.1.109's password")!=-1:  
            cli_interface_module.exec("test") 
        else:
            logger.info("Oh sorry")    
   

