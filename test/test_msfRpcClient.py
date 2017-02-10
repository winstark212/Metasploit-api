
def test_login():
       from test_metasploit_api import MsfRpcClient
       client = MsfRpcClient()
       # print client.msfpro.workspace_add({'name':'scan_local_network','boundary':'192.168.0.1/24', 'description':'','limit_to_network':'false'})
       print client.msfpro.task_list
       # print client.msfpro.start_discover({'ips':['192.168.0.1/24'], 'workspace':'scan_local_network'})

test_login()


