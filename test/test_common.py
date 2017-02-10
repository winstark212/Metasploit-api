json_obj = {'25': {'status': 'running', 'info': 'Scanning http://192.168.0.1:80/ (13/13)', 'description': 'Scanning', 'created_at': 1473149500, 'username': 'metasploit', 'result': '', 'workspace': 'scan_local_network_2', 'error': '', 'progress': 92, 'path': '/opt/metasploit/apps/pro/tasks/task_pro.webscan_25.txt', 'size': 195934}}

print json_obj[str(25)]["status"]