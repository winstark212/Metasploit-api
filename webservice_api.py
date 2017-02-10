# !/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'winstark'

from common.configuration import *
from common.logger import Logger
from common.network_connector import NetworkConnection
from common.configuration import settings
import json
import datetime


class WebServiceAPI:
    def __init__(self):
        # Manager server connection object
        if settings.config["server_infor"]["proxy_connect"] == "1":
            self.manager_server = NetworkConnection(settings.config["server_infor"]["address"],
                                                    settings.config["server_infor"]["port"],
                                                    is_https=settings.config["server_infor"]["using_https"],
                                                    proxies=settings.config["server_infor"]["http_proxy"]
                                                    )
        else:
            self.manager_server = NetworkConnection(settings.config["server_infor"]["address"],
                                                    settings.config["server_infor"]["port"],
                                                    is_https=settings.config["server_infor"]["using_https"]
                                                    )
        self.tool_name = settings.config["tool"]["name"]
        self.token = ""
        self.login()
        if self.token is not "":
            self.headers = {"one-token": self.token, "Content-Type": "application/json"}
        else:
            Logger.error(">> WebServiceAPI >> CAN NOT LOGIN TO MANAGER SERVER")
            sys.exit()

    def login(self):
        data = {"email":
                    settings.config["user"]["email"],
                "password":
                    settings.config["user"]["password"]
                }
        try:
            r = self.manager_server.connect("POST", "/auth/login/", data=json.dumps(data))
            Logger.info("Before login")
            if r.status_code == 200:
                user_info = r.json()
                if "one-token" in user_info:
                    self.token = user_info["one-token"]
                    self.headers = {"one-token": self.token, "Content-Type": "application/json"}
                    Logger.info("Login Successful!")
                return r

        except Exception, ex:
            Logger.error(" web_service_api >>  login >> error " + str(ex))

    def get_new_scan(self, tool_name):
        if tool_name is not None:
            uri = "/scans/new/?tool=" + str(tool_name)
            response = self.manager_server.connect("GET", uri, headers=self.headers)
            if response.status_code == 200:
                return response.json()
        else:
            Logger.error("web_service_api >> get_newscan >> error: cannot found tool_name")

    def put(self, data):

        # if "id" in data:
        uri = "/scans/" + str(data["id"]) + "/"
        response = self.manager_server.connect("PUT", uri, headers=self.headers, data=json.dumps(data))
        if response.status_code == 401:
            self.login()
            return self.manager_server.connect("PUT", uri, headers=self.headers, data=json.dumps(data))
        return response

    def post_notify(self, message, status):

        data = {
            "name": "Acunetix scanner",
            "message": message,
            "status": status,
            "time": str(datetime.datetime.now())
        }
        uri = "/notify/"
        response = self.manager_server.connect("POST", uri, headers=self.headers, data=json.dumps(data))
        if response.status_code == 401:
            self.login()
            return self.manager_server.connect("POST", uri, headers=self.headers, data=json.dumps(data))
        return response

    def get_scan(self, info):
        uri = "/scans/" + str(info["id"]) + "/"
        r = self.manager_server.connect("GET", uri, headers=self.headers)
        status_code = r.status_code
        if status_code == 401:
            self.login()
            r = self.manager_server.connect("GET", uri, headers=self.headers)
            status_code = r.status_code
        if status_code != 200:
            return []
        return r.json()

    def get_task(self,task_id):
        uri = "/tasks/" + str(task_id) + "/"
        r = self.manager_server.connect("GET", uri, headers=self.headers)
        status_code = r.status_code
        if status_code == 401:
            self.login()
            r = self.manager_server.connect("GET", uri, headers=self.headers)
            status_code = r.status_code
        if status_code != 200:
            return []
        return r.json()["name"]
