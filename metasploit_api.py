# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'winstark'

from common.logger import Logger
from common.configuration import settings
from common.msfrpc import MsfRpcClient
from common.network_connector import NetworkConnection
import sys
import json

class MetasploitAPI:
    """
    Interact with webservice
    """
    def __init__(self):
        """
        Manager server connection object
        """
        self.server = settings.config["tool"]["address"].encode("utf8")
        self.port = settings.config["tool"]["port"]
        self.token = settings.config["tool"]["token"].encode("utf8")
        self.uri_base = "/rest_api/v2"
        # Manager server connection object
        if settings.config["tool"]["proxy_connect"] == "1":
            self.manager_server = NetworkConnection(settings.config["tool"]["address"],
                                                    settings.config["tool"]["port"],
                                                    is_https=settings.config["tool"]["using_https"],
                                                    proxies=settings.config["tool"]["http_proxy"]
                                                    )
        else:
            self.manager_server = NetworkConnection(settings.config["tool"]["address"],
                                                    settings.config["tool"]["port"],
                                                    is_https=settings.config["tool"]["using_https"]
                                                    )

        self.headers = {"token": self.token, "Content-Type": "application/json"}
        if self.check_service() is True:
            self.client = MsfRpcClient(self, server=self.server, port=self.port, token=self.token)
            Logger.info("Metasploit service ready!")
        else:
            Logger.error(">> MetasploitAPI >> CAN NOT LOGIN TO METASPLOIT SERVICE")
            sys.exit()

    def check_service(self):
        """
        Check service status
        return true if metasploit service available
        """
        response = self.manager_server.connect("GET", self.uri_base + "/base/", headers=self.headers)
        if response.status_code != 200:
            return False
        return True

    def workspace_add(self, worksapce):
        """Add new workspace"""
        try:
            self.client.msfpro.workspace_add(workspace=worksapce)
        except Exception, ex:
            Logger.error("Metasploiapi >> workspace_add >> error: " + str(ex))
            return False
        return True

    def start_discover(self, task):
        """Start discovery network"""
        try:
            task_id = self.client.msfpro.start_discover(task=task)
        except Exception, ex:
            Logger.error("Metasploiapi >> start_discover >> error: " + str(ex))
            return None
        return task_id["task_id"]

    def start_exploit(self, task):
        """Start exploit network"""
        try:
            task_id = self.client.msfpro.start_exploit(task=task)
        except Exception, ex:
            Logger.error("Metasploiapi >> start_exploit >> error: " + str(ex))
            return None
        return task_id["task_id"]

    def stop(self, task_id):
        """Stop task with task_id"""
        try:
            response = self.client.msfpro.task_stop(task_id=task_id)
        except Exception, ex:
            Logger.error("MetasploiApi >> stop >> error: " + str(ex))
            return None
        return response

    def get_status(self, task_id):
        try:
            response = self.client.msfpro.task_status(task_id=task_id)
        except Exception, ex:
            Logger.error("MetasploiApi >> get_status >> error: " + str(ex))
            return None
        return response

    def get_workspace_id(self, workspace_name):
        res = self.manager_server.connect("GET",uri=self.uri_base +"/workspaces/", headers=self.headers)
        if res.status_code != 200:
            return 1
        else:
            for obj in res.json():
                if obj["name"] == workspace_name:
                    return obj["id"]

    def get_report(self, workspace_id):
        report =  {
                "workspace":{},
                "hosts": {}
            }


        uri = {
            "workspace":self.uri_base + "/workspaces/"+ str(workspace_id),
            "hosts": self.uri_base + "/workspaces/"+ str(workspace_id) +"/hosts/",
        }
        res_workspace = self.manager_server.connect("GET", uri["workspace"], headers=self.headers)
        res_hosts = self.manager_server.connect("GET", uri["hosts"], headers=self.headers)
        if res_workspace.status_code != 200 or res_hosts.status_code != 200:
            return report
        report["workspace"] = res_workspace.json()
        report["hosts"] = res_hosts.json()
        i = 0
        for index in res_hosts.json():
            query_notes =    uri["hosts"] + str(index["id"]) + "/notes/"
            query_services = uri["hosts"] + str(index["id"]) + "/services/"
            query_sessions = uri["hosts"] + str(index["id"]) + "/sessions"

            report["hosts"][i]["notes"] = self.manager_server.connect("GET", uri=query_notes, headers=self.headers).json()
            report["hosts"][i]["sessions"] = self.manager_server.connect("GET", uri=query_sessions, headers=self.headers).json()
            report["hosts"][i]["services"] = self.manager_server.connect("GET", uri=query_services, headers=self.headers).json()
            j = 0
            for obj in report["hosts"][i]["services"]:
                query_vulns = query_services + str(obj["id"]) + "/vulns"
                query_web_sites = query_services + str(obj["id"]) + "/web_sites/"
                report["hosts"][i]["services"][j]["vulns"] = self.manager_server.connect("GET", uri=query_vulns, headers=self.headers).json()
                report["hosts"][i]["services"][j]["web_sites"] = self.manager_server.connect("GET", uri=query_web_sites, headers=self.headers).json()
                k = 0
                for objs in report["hosts"][i]["services"][j]["web_sites"]:
                    query_web_pages = query_web_sites + str(objs["id"]) + "/web_pages"
                    query_web_vulns = query_web_sites + str(objs["id"]) + "/web_vulns"
                    query_web_forms = query_web_sites + str(objs["id"]) + "/web_forms"

                    report["hosts"][i]["services"][j]["web_sites"][k]["web_pages"] = self.manager_server.connect("GET", uri=query_web_pages, headers=self.headers).json()
                    report["hosts"][i]["services"][j]["web_sites"][k]["web_forms"] = self.manager_server.connect("GET",uri=query_web_forms,headers=self.headers).json()
                    report["hosts"][i]["services"][j]["web_sites"][k]["web_vulns"] = self.manager_server.connect("GET",uri=query_web_vulns,headers=self.headers).json()
                    k+=1

                j+=1
            i+=1






        return report







