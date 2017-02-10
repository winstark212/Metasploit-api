from unittest import TestCase


class TestMsfProManager(TestCase):
    def test_workspaces(self):
        from common.msfrpc import MsfRpcClient
        client = MsfRpcClient(self, token='0f065b3c0f06331f2cbd311f359f3d21')
        # name is unquie
        workspace = {'name': 'scan_local_network_6', 'boundary': '192.168.10.1/24', 'description': '',
                     'limit_to_network': 'false'}
        response = client.msfpro.workspace_add(workspace=workspace)
        print response

    def test_start_discover(self):
        from common.msfrpc import MsfRpcClient
        client = MsfRpcClient(self, token='0f065b3c0f06331f2cbd311f359f3d21')
        task = {'ips': ['192.168.0.1/24'], 'workspace': 'scan_local_network_2'}
        print client.msfpro.start_discover(task=task)

    def test_start_exploit(self):
        from common.msfrpc import MsfRpcClient
        client = MsfRpcClient(self, token='0f065b3c0f06331f2cbd311f359f3d21')
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
        print client.msfpro.start_exploit(task=task)

    def test_task_status(self):
        from common.msfrpc import MsfRpcClient
        client = MsfRpcClient(self, token='0f065b3c0f06331f2cbd311f359f3d21')
        print client.msfpro.task_status('5')

    def test_task_stop(self):
        from common.msfrpc import MsfRpcClient
        client = MsfRpcClient(self, token='0f065b3c0f06331f2cbd311f359f3d21')
        print client.msfpro.task_stop('5')

    def test_report_list(self):
        from common.msfrpc import MsfRpcClient
        client = MsfRpcClient(self, token='0f065b3c0f06331f2cbd311f359f3d21')
        print client.msfpro.report_list('scan_local_network_2')

    def test_start_report(self):
        from common.msfrpc import MsfRpcClient
        client = MsfRpcClient(self, token='0f065b3c0f06331f2cbd311f359f3d21')
        config = {
            'workspace': 'scan_local_network_2',
            'name': 'default',
            'report_type':'audit',
            'created_by': 'metasploit',
            'file_formats': ['xml']
        }
        print client.msfpro.start_report(config=config)

    def test_report_download(self):
        from common.msfrpc import MsfRpcClient
        client = MsfRpcClient(self, token='0f065b3c0f06331f2cbd311f359f3d21')
        print client.msfpro.report_download(report_id='2')

    def test_report_download_by_task(self):
        from common.msfrpc import MsfRpcClient
        client = MsfRpcClient(self, token='0f065b3c0f06331f2cbd311f359f3d21')
        print client.msfpro.report_download_by_task(task_id='3')

    def test_start_export(self):
        from common.msfrpc import MsfRpcClient
        client = MsfRpcClient(self, token='0f065b3c0f06331f2cbd311f359f3d21')
        config ={
                "workspace": "testmeta_2-117",
                "name": "	reportABC",
                "report_type": "audit",

                "file_formats": ["pdf"]
}
        print client.msfpro.start_report(config=config)
