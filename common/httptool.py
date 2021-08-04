import requests

import json

class Runrequst:
    """
    created by yanghai
    """
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def send_get(self, params):
        """
        method for the http/https get
        :param params:
        :return:
        """
        response = requests.get(url=self.url, params=params, headers=self.headers).json()
        return json.dumps(response, sort_keys=True, indent=4)

    def send_post(self, data):
        """
        method for the http/https post
        :param data:
        :return:
        """
        response = requests.post(url=self.url, headers=self.headers, json=data).json()
        return json.dumps(response, sort_keys=True, indent=4)

    def run_requst(self, params=None, data=None, method='POST'):
        """
        call the request based on the context of the params, data and method
        :param params:
        :param data:
        :param method:
        :return:
        """
        response = None
        if method == 'GET':
            response = self.send_get(params)
        else:
            response = self.send_post(data)
        return response