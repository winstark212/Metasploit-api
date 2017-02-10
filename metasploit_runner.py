# -*- coding: utf-8 -*-
_author_ = "winstark"
import time
import json
import datetime
from common.configuration import settings
from common.logger import Logger
import metasploit_api
import webservice_api


class MetasploitRunner:
    def __init__(self, new_task):
        self.new_task = new_task
        self.web_api = webservice_api.WebServiceAPI()
        self.metasploit_api = metasploit_api.MetasploitAPI()
        self.time_wait = settings.config["application"]["time_wait"]
        self.start_id = new_task["start_id"]

    def run(self):
        try:
            self.new_task["status"] = 2
            self.new_task["start_time"] = str(datetime.datetime.now())
            if self.check_stop() is True:
                return True
            # start scan
            target = self.new_task["url"]
            task_name = self.web_api.get_task(self.new_task["task"]) + "-" + str(self.new_task["id"])
            workspace = {'name': task_name, 'boundary': target, 'description': '', 'limit_to_network': 'false'}
            Logger.info(target)
            task_discover = {'ips': [target], 'workspace': task_name}
            task_exploit = {
                "workspace": task_name,
                "DS_WHITELIST_HOSTS": target,
                "DS_MinimumRank": "great",
                "DS_EXPLOIT_SPEED": 5,
                "DS_EXPLOIT_TIMEOUT": 2,
                "DS_LimitSessions": "true",
                "DS_MATCH_VULNS": "true",
                "DS_MATCH_PORTS": "true"
            }
            res_workspace = self.metasploit_api.workspace_add(worksapce=workspace)
            workspace_id = self.metasploit_api.get_workspace_id(task_name)
            if res_workspace is True:
                taskid_discover = self.metasploit_api.start_discover(task=task_discover)
                if taskid_discover is not None:
                    status_discover = self.metasploit_api.get_status(taskid_discover)
                    while status_discover[str(taskid_discover)]["status"] == "running":
                        Logger.info('Discovering progress %: ' + str(status_discover[str(taskid_discover)]["progress"]))
                        if self.check_stop() is True:
                            self.metasploit_api.stop(str(taskid_discover))
                            time.sleep(3)
                            return True
                        # self.new_task["report"] = self.get_scan_result(target)
                        self.new_task["percent"] = (int(status_discover[str(taskid_discover)]["progress"])) / 2
                        self.web_api.put(self.new_task)
                        status_discover = self.metasploit_api.get_status(taskid_discover)
                        time.sleep(self.time_wait)
                        self.new_task["report"] = self.convert_utf8(
                            self.metasploit_api.get_report(workspace_id=workspace_id))

                        """Start exploit"""
                taskid_exploit = self.metasploit_api.start_exploit(task=task_exploit)
                if taskid_exploit is not None:
                    status_exploit = self.metasploit_api.get_status(taskid_exploit)
                    while status_exploit[str(taskid_exploit)]["status"] == "running":
                        Logger.info('Exploiting progress %: ' + str(status_exploit[str(taskid_exploit)]["progress"]))
                        if self.check_stop() is True:
                            self.metasploit_api.stop(str(taskid_exploit))
                            time.sleep(3)
                            return True
                        # self.new_task["report"] = self.get_scan_result(target)
                        self.new_task["percent"] = (100 + int(status_exploit[str(taskid_exploit)]["progress"])) / 2
                        self.web_api.put(self.new_task)
                        status_exploit = self.metasploit_api.get_status(taskid_exploit)
                        time.sleep(self.time_wait)
                self.new_task["percent"] = 100
                self.new_task["report"] = self.convert_utf8(self.metasploit_api.get_report(workspace_id=workspace_id))
                self.new_task["finish_time"] = str(datetime.datetime.now())
                self.new_task["status"] = 5
                self.web_api.put(self.new_task)
                message = u"Finished scanning.  " + str(self.new_task["url"])
                self.web_api.post_notify(message, 1)
        except Exception, ex:
            Logger.error("metasploit_runner >> run >> exception " + str(ex))
            self.new_task["status"] = 4
            self.web_api.put(self.new_task)
            message = u"Error appear when scanning:  " + self.new_task["url"]
            self.web_api.post_notify(message, 1)
        return True

    def check_stop(self):
        # check stop scan
        task = self.web_api.get_scan(self.new_task)
        current_id = task["start_id"]
        """Check stopped"""
        if current_id != self.start_id:
            self.new_task["status"] = 3
            self.web_api.put(self.new_task)
            self.web_api.post_notify(message=unicode(u"Stopped scanning task : " + str(self.new_task["id"])), status=1)
            Logger.log("Stopped task " + str(self.new_task["id"]))
            return True
        return False

    def convert_utf8(self, data):
        if isinstance(data, dict):
            return {self.convert_utf8(key): self.convert_utf8(value) for key, value in data.iteritems()}
        elif isinstance(data, list):
            return [self.convert_utf8(element) for element in data]
        elif isinstance(data, unicode):
            return data.encode('utf-8')
        else:
            return data
