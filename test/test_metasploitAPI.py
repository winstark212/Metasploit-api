from unittest import TestCase
import json

class TestMetasploitAPI(TestCase):
    def test_init(self):
        from metasploit_api import MetasploitAPI
        meta = MetasploitAPI()

    def test_check_service(self):
        from metasploit_api import MetasploitAPI
        meta = MetasploitAPI()
        self.assertTrue(meta.check_service())

    def test_workspace_add(self):
        from metasploit_api import MetasploitAPI
        meta = MetasploitAPI()
        workspace = {'name': 'default', 'boundary': '192.168.10.1/24', 'description': '',
                     'limit_to_network': 'false'}
        response = meta.workspace_add(worksapce=workspace)
        self.assertFalse(response)

    def test_workspace_add_1(self):
        from metasploit_api import MetasploitAPI
        meta = MetasploitAPI()
        workspace = {'name': 'scan_local_network_5', 'boundary': '192.168.10.1/24', 'description': '',
                     'limit_to_network': 'false'}
        response = meta.workspace_add(worksapce=workspace)
        self.assertTrue(response)

    def test_start_discover(self):
        from metasploit_api import MetasploitAPI
        meta = MetasploitAPI()
        task = {'ips': ['192.168.0.1/24'], 'workspace': 'scan_local_network_2'}
        response = meta.start_discover(task=task)
        print type(response)
        self.assertTrue(type(response), dict)

    def test_start_discover_1(self):
        from metasploit_api import MetasploitAPI
        meta = MetasploitAPI()
        task = {'ips': ['192.168.0.1/24'], 'workspace': 'scan_local_network_6'}
        response = meta.start_discover(task=task)
        self.assertEqual(response, None)

    def test_start_exploit(self):
        from metasploit_api import MetasploitAPI
        msf = MetasploitAPI()
        task = {
            "workspace": "scan_local_network_2",
            "DS_WHITELIST_HOSTS": "192.168.0.1/24",
            "DS_MinimumRank": "great",
            "DS_EXPLOIT_SPEED": 5,
            "DS_EXPLOIT_TIMEOUT": 2,
            "DS_LimitSessions": "true",
            "DS_MATCH_VULNS": "true",
            "DS_MATCH_PORTS": "true"
        }
        response = msf.start_exploit(task=task)
        self.assertEqual(type(response), dict)

    def test_start_exploit_1(self):
        from metasploit_api import MetasploitAPI
        msf = MetasploitAPI()
        task = {
            "workspace": "scan_local_network_",
            "DS_WHITELIST_HOSTS": "192.168.0.1/24",
            "DS_MinimumRank": "great",
            "DS_EXPLOIT_SPEED": 5,
            "DS_EXPLOIT_TIMEOUT": 2,
            "DS_LimitSessions": "true",
            "DS_MATCH_VULNS": "true",
            "DS_MATCH_PORTS": "true"
        }
        response = msf.start_exploit(task=task)
        self.assertEqual(response, None)

    def test_stop(self):
        self.fail()

    def test_get_status(self):
        from metasploit_api import MetasploitAPI
        meta = MetasploitAPI()
        response = meta.get_status("25")
        print response

    def test_get_report(self):
        from metasploit_api import MetasploitAPI
        msf = MetasploitAPI()
        print json.dumps(msf.get_report(workspace_id=29))

    def test_get_resource(self):
        from metasploit_api import MetasploitAPI
        msf = MetasploitAPI()
        print msf.get_resource("/rest_api/v2/workspaces/25/hosts/", "/services")
