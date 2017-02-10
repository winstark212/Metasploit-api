__author__ = 'winstark'
# -*- coding: utf-8 -*-
import os
import sys
import json
from singleton import Singleton
from bcolors import bcolors


class Configuration:
    _instance = None

    def __init__(self):
        """
        Constructor functions
        :current_path: Directory of config file
        :current_path: Config file name
        :config: Dictionary contain config value
        :return:
        """
        self.current_path = os.path.normpath(os.path.join(os.path.realpath(__file__), '../../'))
        self.config_filename = 'application.json'
        self.config = {}
        self.load_config()

    def check_config(self):
        #  check config logger
        if "logger" in settings.config:
            if type(settings.config["logger"]) != type({}):
                bcolors.error("logger config is not dictionary")
                return False

            if "logs_folder" in settings.config["logger"]:
                self.logs_folder = os.path.join(settings.current_path, settings.config["logger"]["logs_folder"])
                if not os.path.exists(self.logs_folder):
                    os.makedirs(os.path.realpath(self.logs_folder))
                if not os.path.exists(self.logs_folder):
                    bcolors.error("Cannot create logs folder: " + str(self.logs_folder))
                    return False
            else:
                bcolors.error("log_folders directory is not in config")
                return False

            # Check logs_file config
            if "logs_file" in settings.config["logger"]:
                self.log_file = os.path.join(self.logs_folder, settings.config["logger"]["logs_file"])
            else:
                bcolors.error("logs_file filename is not in config")
                return False

            # Check loglevel config
            if "logs_level" in settings.config["logger"]:
                self.log_level = settings.config["logger"]["logs_level"]
            else:
                bcolors.error("loglevel filename is not in config")
                return False
        else:
            bcolors.error("bcolors config is not in config")
            return False

        # Check server_infor dictionary in config
        if "server_infor" in settings.config:
            if type(settings.config["server_infor"]) != type({}):
                bcolors.error("server_infor config is not dictionary")
                return False

            # Check Rootkit directory in config
            if "address" not in settings.config["server_infor"]:
                bcolors.error("sername address is not in config")
                return False

            # Check Rootkit filename in config
            if "port" not in settings.config["server_infor"]:
                bcolors.error("port server is not in config")
                return False
        else:
            bcolors.error_log("server infor config is not in config")
            return False

        # Check acunetix infor in config
        if "user" in settings.config:
            if type(settings.config["user"]) != type({}):
                bcolors.error("user  config is not dictionary")
                return False
            if "email" not in settings.config["user"]:
                bcolors.error(" email user is not in config")
                return False
            if "password" not in settings.config["user"]:
                bcolors.error_log(" password user is not in config")
                return False
        else:
            bcolors.error("user is not in config")
            return False

        if "tool" in settings.config:
            if type(settings.config["tool"]) != type({}):
                return False
            if "name" not in settings.config["tool"]:
                return False
            if "address" not in settings.config["tool"]:
                return False
            if "port" not in settings.config["tool"]:
                return False
            if "using_https" not in settings.config["tool"]:
                return False
            if "proxy_connect" not in settings.config["tool"]:
                return False
            if "http_proxy" not in settings.config["tool"]:
                return False
            if "token" not in settings.config["tool"]:
                return False
            if "username" not in settings.config["tool"]:
                return False

        else:
            bcolors.error("tool is not in config")
            return False

        if "application" in settings.config:
            if type(settings.config["application"]) != type({}):
                return False
            if "num_thread" not in settings.config["application"]:
                return False
            else:
                try:
                    num_thread = int(settings.config["application"]["num_thread"])
                    if num_thread < 1:
                        settings.config["application"]["num_thread"] = 1
                except ValueError:
                    bcolors.error("num_thread is invalid")
                    return False
            if "time_wait" not in settings.config["application"]:
                return False
            else:
                try:
                    time_wait = int(settings.config["application"]["time_wait"])
                    if time_wait < 1:
                        settings.config["application"]["time_wait"] = 3
                except ValueError:
                    bcolors.error("time_wait is invalid")
                    return False
        else:
            bcolors.error("application is not in config")
            return False

    def create(self, config={}):
        """
        Create a new file config
        :param config: Dictionary contain config value
        :return: New file config is created.
        """
        if len(config.keys()) == 0:
            config = {
                'bcolors': {"logs_folder": "logs", "logs_level": "all", "logs_file": "application.log"}}
        try:
            with open(os.path.join(self.current_path, self.config_filename), 'w') as f:
                json.dump(config, f)
        except Exception, err:
            sys.exit()

    def load_config(self):
        """
        Load config from file config
        :return: Dictionary contain config value is save in self.config
        """
        fconfig = os.path.join(self.current_path, self.config_filename)
        if not os.path.exists(fconfig):
            self.current_path = os.getcwd()
            fconfig = os.path.join(self.current_path, self.config_filename)
            if not os.path.exists(fconfig):
                bcolors.error("Cannot find file configuration: " + str(fconfig))
                sys.exit()
        try:
            with open(fconfig, 'r') as f:
                self.config = json.load(f)
        except Exception, ex:
            bcolors.error("Cannot load file configuration " + str(fconfig) + ": " + str(ex))
            sys.exit()


settings = Singleton(Configuration)
