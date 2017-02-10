__author__ = 'winstark'

def Singleton(klass):
    if not klass._instance:
        klass._instance = klass()
    return klass._instance


class Bcolors:
    _instance = None
    """
    Print color in terminal python
    Using:
    from bcolors import Bcolors as bcolors
    bcolors.success("This is success strings")
    """

    def __init__(self):
        self.header_color = '\033[95m'
        # self.okblue = '\033[94m'
        # self.okblue = '\033[92m'
        self.success_color = '\033[92m'
        self.warning_color = '\033[93m'
        self.error_color = '\033[91m'
        self.endc_color = '\033[0m'
        self.bold_color = '\033[1m'
        self.underline_color = '\033[4m'

    def header(self, data):
        """
        Print header strings
        :param data: string content
        :return: Content string is printed in console
        """
        print self.header_color + str(data) + self.endc_color

    def success(self, data):
        """
        Print success strings
        :param data: string content
        :return: Content string is printed in console
        """
        print self.success_color + str(data) + self.endc_color

    def warning(self, data):
        """
        Print warning strings
        :param data: string content
        :return: Content string is printed in console
        """
        print self.warning_color + str(data) + self.endc_color

    def error(self, data):
        """
        Print error strings
        :param data: string content
        :return: Content string is printed in console
        """
        print self.error_color + str(data) + self.endc_color

    def bold(self, data):
        """
        Print bold strings
        :param data: string content
        :return: Content string is printed in console
        """
        print self.bold_color + str(data) + self.endc_color

    def underline(self, data):
        """
        Print underline strings
        :param data: string content
        :return: Content string is printed in console
        """
        print self.underline_color + str(data) + self.endc_color


bcolors = Singleton(Bcolors)
