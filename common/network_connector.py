__author__ = 'winstark'
import time
import requests
from requests.exceptions import RequestException
from urlparse import urlparse
from logger import Logger
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class NetworkConnection:
    def __init__(self, server, port, is_https=False, proxies=None):
        self.server = server
        self.port = port
        self.verify = False
        self.is_https = is_https
        self.proxy = proxies
        self.error = RequestError()

    def build_url(self, uri):
        url = self.server
        if self.is_https:
            if url.find("https://") == -1:
                url = "https://" + url
        else:
            if url.find("http://") == -1:
                url = "http://" + url
        url_parsed = urlparse(url)
        if url_parsed.port is None:
            if self.port is not "":
                new_url = url_parsed.netloc + ":" + str(self.port)
                url = url_parsed._replace(netloc=new_url)
                url = url.geturl()
        return '{0}{1}'.format(url, uri)

    def connect(self, method, uri, headers=None, data=None, files=None, stream=None):
        repeat_times = 3
        count = 0
        error_message = ""
        response = None
        while (count < repeat_times):
            try:
                if self.is_https:
                    response = self.https_connect(method, uri, headers=headers, data=data, files=files, stream=stream)
                else:
                    response = self.http_connect(method, uri, headers=headers, data=data, files=files, stream=stream)
                if stream == True:
                    return response
                response.raise_for_status()
                return response
            except (ValueError, RequestException) as exc:
                if hasattr(exc, 'response') and hasattr(exc.response, 'status_code'):
                    return exc.response
                else:
                    Logger.error(">> NETWORK CONNECTION ERROR >> URL: " + str(self.build_url(uri)) + " : " + str(exc))
                    error_message = str(exc)
                    time.sleep(3)
                    count += 1
                    continue
        self.error.status_code = 503
        self.error.content = error_message
        return self.error

    def http_connect(self, method, uri, headers=None, data=None, files=None, stream=None):
        if headers is None:
            headers = {'content-type': 'application/json'}
        if method == 'POST':
            return requests.post(self.build_url(uri), data=data, headers=headers,
                                 proxies=self.proxy, files=files, stream=stream)
        elif method == 'PUT':
            return requests.put(self.build_url(uri), data=data, headers=headers,
                                proxies=self.proxy, files=files, stream=stream)
        elif method == 'DELETE':
            return requests.delete(self.build_url(uri), data=data, headers=headers,
                                   proxies=self.proxy, files=files, stream=stream)
        else:
            return requests.get(self.build_url(uri), params=data, headers=headers,
                                proxies=self.proxy, files=files, stream=stream)

    def https_connect(self, method, uri, headers=None, data=None, files=None, stream=None):
        if headers is None:
            headers = {'content-type': 'application/json'}
        if method == 'POST':
            return requests.post(self.build_url(uri), data=data, headers=headers,
                                 verify=self.verify, proxies=self.proxy, files=files, stream=stream)
        elif method == 'PUT':
            return requests.put(self.build_url(uri), data=data, headers=headers,
                                verify=self.verify, proxies=self.proxy, files=files, stream=stream)
        elif method == 'DELETE':
            return requests.delete(self.build_url(uri), data=data, headers=headers,
                                   verify=self.verify, proxies=self.proxy, files=files, stream=stream)
        else:
            return requests.get(self.build_url(uri), params=data, headers=headers,
                                verify=self.verify, proxies=self.proxy, files=files, stream=stream)



class RequestError():
    def __init__(self, status_code=404, content=""):
        self.error = True
        self.status_code = status_code
        self.content = content
