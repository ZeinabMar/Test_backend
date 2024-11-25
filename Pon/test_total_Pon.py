import time
import pytest
import logging
from conftest import *
from config import *
from Pon.test_Smoke_Pon import test_Smoke
from Pon.test_dba_profile import test_DBA_Profile
from Pon.test_tcont_profile import test_Tcont_Management
# from Pon.test_gem_profile import test_Gem_Management 
# from Pon.test_OLT_Service import test_OLT_Service
# from Pon.test_ONU_remote_Service import test_ONU_remote_Service
# from Pon.test_onu_auto_learn import test_onu_authentication
# from Pon.test_FEC_Management import test_FEC_Management
# from Pon.test_ONUs_Capability import test_ONUs_Capability
# from Pon.test_Pon_Initial_Information import test_Pon_Initial_Information
# from Pon.test_ONUs_Initial_Information import test_ONUs_Initial_Information
# from Pon.test_Onu_Type_Profile import test_Onu_Type_Profile
# from Pon.test_Add_Edit_Onus import test_Add_Edit_Onus
# from Pon.test_Pon_Optical_Module_Management import test_Pon_Optical_Module_Managment
# from Pon.test_Service_Profile_Tcont import test_Tcont_Service_Profile
# from Pon.test_Service_Profile_Definition import test_Service_Profile_Definition
# from Pon.test_Service_Profile_Tcont import test_Tcont_Service_Profile
# from Pon.test_Service_Profile_Gem import test_Gem_Service_Profile
# from Pon.test_Service_Profile_OLT import test_Olt_Service_Profile
# from Pon.test_Service_Profile_Onu_Remote import test_Remote_Service_Profile
# from Pon.test_Pon_Protection import test_Pon_Protection
# from Pon.test_IPTV_Configuration import test_IPTV_Configuration
# from Pon.test_Batch_Config_Service_Profile import test_Batch_Config
# from Pon.test_AES_encryption_Management import test_AES_encryption_Management


pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]

