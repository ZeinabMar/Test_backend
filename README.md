# test_sp5100_rest
        1) git clone git@gitlab.sinacomsys.local:quality-assurance/test-infrastructure/pytest-sina-framework.git
        2) cd /pytest_sina_framework
        3) python -m pip install --editable ./pytest-sina-framework

git clone any library required for your Test code from Test Infrastructure git server

        1) git clone git@gitlab.sinacomsys.local:quality-assurance/test-infrastructure/restlib.git
        2) cd /snmplib
        3) python3 -m pip install -e .

example run code :

        1) cd ../test_sp5100_rest
        2) python3 -m pytest -s /home/zeinab/test_sp5100/test_sp5100_rest/Switch/test_bridge_definition.py       
