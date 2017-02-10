import os.path
import threading
from datetime import datetime
from bcolors import bcolors
from singleton import Singleton
from configuration import settings
class Logger:
    _instance = None

    def __init__(self):
        """
        Init function
        logs_folder: Logfile directory
        log_file: log filename
        log_level: Log level
        :return:
        """
        self.current_path = os.getcwd()
        self.logs_folder = settings.config["logger"]["logs_folder"]
        self.log_file = os.path.join(self.current_path,self.logs_folder, settings.config["logger"]["logs_file"])
        self.log_level = settings.config["logger"]["logs_level"]

    def log(self, data):
        """
        Write info log functions
        :param data: log string
        :return: log string is write and print if log_level is info or all
        """
        try:
            # if not self.check_config():
            #     return False
            if self.log_level.lower() != "all" and self.log_level.lower() != "info":
                return False
            threading.Lock()
            data_log = '\n[+] %s : %s' % (str(datetime.now()), str(data))
            bcolors.header(data_log)
            _writer = open(self.log_file, "a+")
            _writer.write(data_log)
            _writer.close()
            threading.RLock()
        except Exception, ex:
            bcolors.error("Cannot write  log: " + str(ex))

    def error(self, data):
        """
        Write error log functions
        :param data: log string
        :return: log string is write and print if log_level is error or all
        """
        try:
            # if not self.check_config():
            #     return False
            if self.log_level.lower() != "all" and self.log_level.lower() != "error":
                return False
            threading.Lock()
            data_log = '\n[+] %s : %s' % (str(datetime.now()), str(data))
            bcolors.error(data_log)
            _writer = open(self.log_file, "a+")
            _writer.write(data_log)
            _writer.close()
            threading.RLock()
        except Exception, ex:
            bcolors.error("Cannot write error log: " + str(ex))

    def info(self, data):
        """
        Write error log functions
        :param data: log string
        :return: log string is write and print if log_level is error or all
        """
        try:
            # if not self.check_config():
            #     return False
            if self.log_level.lower() != "all":
                return False
            data_log = '\n[+] %s : %s' % (str(datetime.now()), str(data))
            bcolors.success(data_log)
        except Exception, ex:
            bcolors.error("Cannot write info log: " + str(ex))


Logger = Singleton(Logger)
