# -*- coding: utf-8 -*-

__author__ = 'winstark'
import time
from metasploit_runner import MetasploitRunner
from webservice_api import WebServiceAPI
from thread_pool import MyThreadPool
from common.logger import Logger
from common.configuration import settings
import sys


class MetasploitObserver:
    def __init__(self):
        if settings.check_config() is False:
            Logger.error("Metasploit_observer >> observe >> error config ")
            sys.exit()
        self.web_api = WebServiceAPI()
        self.thread = MyThreadPool(settings.config["application"]["num_thread"])
        self.notify = {}
        self.time_wait = settings.config["application"]["time_wait"]

    def observe(self):
        while True:
            new_task = self.web_api.get_new_scan(self.web_api.tool_name)
            if type(new_task) is not type([]):
                time.sleep(self.time_wait)
                Logger.error("Metasploit_observer >> observe >> response not type demand")
                continue
            try:
                for task in new_task:
                    if "id" in task:
                        # update status
                        self.thread.add_task(self.create_scan(task))
            except Exception, ex:
                message = u" Error appear when scanning   "
                Logger.error("Metasploit_observer >> observe >> error : " + str(ex))
                self.web_api.post_notify(message, 1)
            time.sleep(self.time_wait)
        self.thread.wait_completion()

    def create_scan(self, task):
        task["status"] = 1
        message = u" Scanning..." + task["url"]
        self.web_api.post_notify(message, 0)
        self.web_api.put(task)
        pw_recover = MetasploitRunner(task)
        pw_recover.run()

pw_recovery_observer = MetasploitObserver()
pw_recovery_observer.observe()

